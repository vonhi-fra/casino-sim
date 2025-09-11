# blackjack_web/blackjack/bot_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Player, Game
from core.blackjack.game import WebBlackjackGame
from bot.blackjack_bot import BlackjackBot
from decimal import Decimal
import json
import time

def bot_play(request, player_id):
    """Widok do gry bota"""
    player = get_object_or_404(Player, id=player_id)
    bot = BlackjackBot()
    
    if request.method == 'POST':
        if 'start_bot' in request.POST:
            return _start_bot_game(request, player, bot)
        elif 'auto_play' in request.POST:
            return _auto_play_round(request, player, bot)
    
    # Sprawdź czy jest aktywna gra
    if 'active_game' in request.session:
        game_data = request.session['active_game']
        return render(request, 'blackjack/bot_game.html', {
            'player': player,
            'game_state': game_data['game_state'],
            'bet_amount': game_data['bet_amount'],
            'bot_active': True
        })
    
    return render(request, 'blackjack/bot_setup.html', {
        'player': player,
        'suggested_bet': bot.get_betting_strategy(float(player.balance))
    })

def _start_bot_game(request, player, bot):
    """Rozpocznij grę z botem"""
    bet_amount = Decimal(request.POST.get('bet_amount', bot.get_betting_strategy(float(player.balance))))
    
    if bet_amount > player.balance:
        return render(request, 'blackjack/bot_setup.html', {
            'player': player,
            'error': 'Insufficient balance!',
            'suggested_bet': bot.get_betting_strategy(float(player.balance))
        })
    
    game = WebBlackjackGame()
    game_state = game.start_game(float(bet_amount))
    
    # Dodaj rekomendację bota
    if game_state['status'] == 'playing':
        bot_action = bot.get_optimal_action(
            player_cards=game_state['player_cards'],
            dealer_up_card=game_state['dealer_visible'],
            can_double=game_state.get('can_double', False),
            can_split=game_state.get('can_split', False),
            player_balance=float(player.balance),
            current_bet=float(bet_amount)
        )
        
        bot_explanation = bot.explain_decision(
            player_cards=game_state['player_cards'],
            dealer_up_card=game_state['dealer_visible'],
            action=bot_action,
            player_balance=float(player.balance),
            current_bet=float(bet_amount)
        )
        
        game_state['bot_recommendation'] = bot_action
        game_state['bot_explanation'] = bot_explanation
    
    request.session['active_game'] = {
        'game_state': game_state,
        'bet_amount': float(bet_amount),
        'game_data': game.to_dict(),
        'bot_active': True
    }
    
    if game_state['status'] == 'blackjack':
        return _finish_bot_game(request, player, game_state, bet_amount, 'blackjack', game)
    
    return render(request, 'blackjack/bot_game.html', {
        'player': player,
        'game_state': game_state,
        'bet_amount': bet_amount,
        'bot_active': True
    })

def _auto_play_round(request, player, bot):
    """Automatyczne rozegranie rundy przez bota"""
    if 'active_game' not in request.session:
        return redirect('bot_play', player_id=player.id)
    
    game_session = request.session['active_game']
    original_bet = Decimal(str(game_session['bet_amount']))
    
    game = WebBlackjackGame()
    game.from_dict(game_session['game_data'])
    
    moves_history = []
    
    # Bot gra automatycznie do końca
    while True:
        current_state = game_session['game_state']
        
        if current_state['status'] not in ['playing', 'split_done', 'next_hand', 'hand_bust_next']:
            break
        
        # Pobierz rekomendację bota
        bot_action = bot.get_optimal_action(
            player_cards=current_state.get('player_cards', current_state.get('all_hands', [{}])[current_state.get('current_hand', 0)].get('cards', [])),
            dealer_up_card=current_state['dealer_visible'],
            can_double=current_state.get('can_double', False),
            can_split=current_state.get('can_split', False),
            player_balance=float(player.balance),
            current_bet=float(original_bet)
        )
        
        bot_explanation = bot.explain_decision(
            player_cards=current_state.get('player_cards', current_state.get('all_hands', [{}])[current_state.get('current_hand', 0)].get('cards', [])),
            dealer_up_card=current_state['dealer_visible'],
            action=bot_action,
            player_balance=float(player.balance),
            current_bet=float(original_bet)
        )
        
        moves_history.append({
            'action': bot_action,
            'explanation': bot_explanation,
            'hand_before': current_state.get('player_cards', []).copy(),
            'total_before': current_state.get('player_total', 0)
        })
        
        # Wykonaj akcję
        result = None
        if bot_action == 'hit':
            result = game.hit()
        elif bot_action == 'stand':
            result = game.stand()
        elif bot_action == 'double':
            if current_state.get('can_double', False) and player.balance >= original_bet:
                result = game.double_down()
            else:
                result = game.hit()  # Fallback
        elif bot_action == 'split':
            if current_state.get('can_split', False) and player.balance >= original_bet:
                result = game.split()
            else:
                result = game.hit()  # Fallback
        
        if result is None:
            break
        
        # Aktualizuj sesję
        request.session['active_game'] = {
            'game_state': result,
            'bet_amount': float(original_bet),
            'game_data': game.to_dict(),
            'bot_active': True,
            'moves_history': moves_history
        }
        request.session.modified = True
        
        game_session = request.session['active_game']
        
        if result.get('game_over'):
            return _finish_split_bot_game(request, player, result, original_bet, game, moves_history)
    
    return render(request, 'blackjack/bot_game.html', {
        'player': player,
        'game_state': game_session['game_state'],
        'bet_amount': original_bet,
        'bot_active': True,
        'moves_history': moves_history
    })

def _finish_bot_game(request, player, game_state, bet_amount, game_result, game_instance):
    """Zakończ grę bota (standardowy blackjack)"""
    payout = Decimal('0')
    if game_result == 'win':
        payout = bet_amount * 2
    elif game_result == 'blackjack':
        payout = bet_amount + (bet_amount * Decimal('1.5'))
    elif game_result == 'draw':
        payout = bet_amount
    
    balance_change = payout - bet_amount
    player.balance += balance_change
    player.save()
    
    Game.objects.create(
        player=player,
        bet_amount=bet_amount,
        player_cards=game_state.get('player_cards', []),
        dealer_cards=game_state.get('dealer_cards', [game_state.get('dealer_visible', '')]),
        result=game_result,
        payout=payout
    )
    
    if 'active_game' in request.session:
        del request.session['active_game']
    
    return render(request, 'blackjack/bot_result.html', {
        'player': player,
        'game_state': game_state,
        'result': game_result,
        'payout': payout,
        'bet_amount': bet_amount,
        'moves_history': request.session.get('active_game', {}).get('moves_history', [])
    })

def _finish_split_bot_game(request, player, game_state, original_bet_amount, game_instance, moves_history):
    """Zakończ grę split bota"""
    original_bet = Decimal(str(original_bet_amount))
    total_payout = Decimal('0')
    
    if 'hand_results' in game_state:
        hand_results = game_state['hand_results']
        total_bet = sum(Decimal(str(hand['bet'])) for hand in hand_results)
        
        for hand in hand_results:
            if hand['result'] == 'win':
                total_payout += Decimal(str(hand['bet'])) * 2
            elif hand['result'] == 'draw':
                total_payout += Decimal(str(hand['bet']))
        
        if total_payout > total_bet:
            main_result = 'win'
        elif total_payout == total_bet:
            main_result = 'draw'
        else:
            main_result = 'lose'
            
        display_bet = total_bet
    else:
        game_result = game_state.get('result', 'lose')
        
        if 'doubled_bet' in game_state:
            bet_for_calculation = Decimal(str(game_state['doubled_bet']))
        else:
            bet_for_calculation = original_bet
            
        if game_result == 'win':
            total_payout = bet_for_calculation * 2
        elif game_result == 'draw':
            total_payout = bet_for_calculation
        
        main_result = game_result
        display_bet = bet_for_calculation
    
    balance_change = total_payout - display_bet
    player.balance += balance_change
    player.save()
    
    Game.objects.create(
        player=player,
        bet_amount=display_bet,
        player_cards=game_state.get('all_hands', [{}])[0].get('cards', []) if game_state.get('all_hands') else game_state.get('player_cards', []),
        dealer_cards=game_state.get('dealer_cards', []),
        result=main_result,
        payout=total_payout
    )
    
    if 'active_game' in request.session:
        del request.session['active_game']
    
    return render(request, 'blackjack/bot_result.html', {
        'player': player,
        'game_state': game_state,
        'result': main_result,
        'payout': total_payout,
        'bet_amount': display_bet,
        'split_results': game_state.get('hand_results', []),
        'moves_history': moves_history
    })

def bot_statistics(request, player_id):
    """Wyświetl statystyki gier gracza"""
    player = get_object_or_404(Player, id=player_id)
    games = Game.objects.filter(player=player).order_by('-created_at')
    
    if games:
        total_games = games.count()
        wins = games.filter(result='win').count()
        losses = games.filter(result='lose').count()
        draws = games.filter(result='draw').count()
        blackjacks = games.filter(result='blackjack').count()
        
        total_bet = sum(game.bet_amount for game in games)
        total_payout = sum(game.payout for game in games)
        net_result = total_payout - total_bet
        
        win_rate = (wins + blackjacks) / total_games * 100 if total_games > 0 else 0
        
        stats = {
            'total_games': total_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'blackjacks': blackjacks,
            'win_rate': round(win_rate, 1),
            'total_bet': total_bet,
            'total_payout': total_payout,
            'net_result': net_result,
            'avg_bet': round(total_bet / total_games, 2) if total_games > 0 else 0
        }
    else:
        stats = None
    
    return render(request, 'blackjack/bot_statistics.html', {
        'player': player,
        'games': games[:20],  # Ostatnie 20 gier
        'stats': stats
    })