from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Game
from core.blackjack.game import WebBlackjackGame
from bot.blackjack_bot import BlackjackBot
from decimal import Decimal

def bot_play(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    bot = BlackjackBot()
    
    print(f"DEBUG: bot_play called, method={request.method}")
    
    if request.method == 'POST':
        print(f"DEBUG: POST data = {request.POST}")
        return _play_multiple_games(request, player, bot)
    
    return render(request, 'blackjack/bot_setup.html', {
        'player': player,
        'suggested_bet': bot.get_betting_strategy(float(player.balance))
    })

def _play_multiple_games(request, player, bot):
    print("DEBUG: _play_multiple_games started")
    
    try:
        num_games = int(request.POST.get('num_games', 10))
        bet_amount = Decimal(request.POST.get('bet_amount', 100))
        
        print(f"DEBUG: num_games={num_games}, bet_amount={bet_amount}")
        
        if num_games < 1 or num_games > 1000:
            return render(request, 'blackjack/bot_setup.html', {
                'player': player,
                'error': 'Number of games must be between 1 and 1000!',
                'suggested_bet': bot.get_betting_strategy(float(player.balance))
            })
        
        total_needed = bet_amount * num_games
        if total_needed > player.balance:
            return render(request, 'blackjack/bot_setup.html', {
                'player': player,
                'error': f'Not enough balance! Need ${total_needed} for {num_games} games of ${bet_amount}',
                'suggested_bet': bot.get_betting_strategy(float(player.balance))
            })
        
        session_stats = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'blackjacks': 0,
            'total_bet': Decimal('0'),
            'total_payout': Decimal('0'),
            'game_results': []
        }
        
        starting_balance = player.balance
        print(f"DEBUG: Starting balance: ${starting_balance}")
        
        for game_num in range(num_games):
            print(f"DEBUG: Playing game {game_num + 1}")
            
            if player.balance < bet_amount:
                print(f"DEBUG: Insufficient balance, stopping at game {game_num + 1}")
                break
            
            try:
                result = _play_single_game(player, bot, bet_amount, game_num + 1)
                
                session_stats['games_played'] += 1
                session_stats['total_bet'] += result['bet']
                session_stats['total_payout'] += result['payout']
                
                if result['result'] == 'win':
                    session_stats['wins'] += 1
                elif result['result'] == 'lose':
                    session_stats['losses'] += 1
                elif result['result'] == 'blackjack':
                    session_stats['blackjacks'] += 1
                else:
                    session_stats['draws'] += 1
                
                session_stats['game_results'].append(result)
                
                balance_change = result['payout'] - result['bet']
                player.balance += balance_change
                
                Game.objects.create(
                    player=player,
                    bet_amount=result['bet'],
                    player_cards=result.get('player_cards', []),
                    dealer_cards=result.get('dealer_cards', []),
                    result=result['result'],
                    payout=result['payout']
                )
                
            except Exception as e:
                print(f"DEBUG: Error in game {game_num + 1}: {str(e)}")
                continue
        
        player.save()
        print(f"DEBUG: Session completed. Games played: {session_stats['games_played']}")
        
        session_stats['net_result'] = session_stats['total_payout'] - session_stats['total_bet']
        session_stats['win_rate'] = ((session_stats['wins'] + session_stats['blackjacks']) / session_stats['games_played'] * 100) if session_stats['games_played'] > 0 else 0
        session_stats['balance_change'] = player.balance - starting_balance
        
        return render(request, 'blackjack/bot_multi_result.html', {
            'player': player,
            'session_stats': session_stats,
            'requested_games': num_games,
            'bet_per_game': bet_amount,
            'starting_balance': starting_balance
        })
        
    except Exception as e:
        print(f"DEBUG: Major error: {str(e)}")
        return render(request, 'blackjack/bot_setup.html', {
            'player': player,
            'error': f'Error occurred: {str(e)}',
            'suggested_bet': bot.get_betting_strategy(float(player.balance))
        })

def _play_single_game(player, bot, bet_amount, game_num, game = WebBlackjackGame()):

    game_state = game.start_game(float(bet_amount))
    
    if game_state['status'] == 'blackjack':
        payout = bet_amount + (bet_amount * Decimal('1.5'))
        return {
            'game_num': game_num,
            'result': 'blackjack',
            'bet': bet_amount,
            'payout': payout,
            'player_cards': game_state.get('player_cards', []),
            'dealer_cards': game_state.get('dealer_cards', []),
            'moves': []
        }
    
    moves_log = []
    max_moves = 20
    move_count = 0
    
    while game_state['status'] in ['playing', 'split_done', 'next_hand', 'hand_bust_next'] and move_count < max_moves:
        move_count += 1
        
        dealer_visible = game_state.get('dealer_visible', '10♠')
        if not dealer_visible:
            dealer_cards = game_state.get('dealer_cards', [])
            if dealer_cards:
                dealer_visible = dealer_cards[0]
            else:
                dealer_visible = '10♠'
        
        if game_state.get('all_hands'):
            current_hand_idx = game_state.get('current_hand', 0)
            all_hands = game_state['all_hands']
            if current_hand_idx < len(all_hands):
                player_cards = all_hands[current_hand_idx].get('cards', [])
            else:
                player_cards = game_state.get('player_cards', [])
        else:
            player_cards = game_state.get('player_cards', [])
        
        bot_action = bot.get_optimal_action(
            player_cards=player_cards,
            dealer_up_card=dealer_visible,
            can_double=game_state.get('can_double', False),
            can_split=game_state.get('can_split', False),
            player_balance=float(player.balance),
            current_bet=float(bet_amount)
        )
        
        moves_log.append(bot_action)
        
        old_state = game_state.copy()
        if bot_action == 'hit':
            game_state = game.hit()
        elif bot_action == 'stand':
            game_state = game.stand()
        elif bot_action == 'double':
            if game_state.get('can_double', False) and player.balance >= bet_amount:
                game_state = game.double_down()
            else:
                game_state = game.hit()
        elif bot_action == 'split':
            if game_state.get('can_split', False) and player.balance >= bet_amount:
                game_state = game.split()
            else:
                game_state = game.hit()
        
        if game_state is None:
            game_state = old_state
            break
            
        if game_state.get('game_over'):
            break
    
    game_result, payout = _calculate_game_result(game_state, bet_amount)
    actual_bet = game_state.get('doubled_bet', bet_amount) if 'doubled_bet' in game_state else bet_amount
    
    return {
        'game_num': game_num,
        'result': game_result,
        'bet': actual_bet,
        'payout': payout,
        'moves': moves_log,
        'player_cards': game_state.get('player_cards', []),
        'dealer_cards': game_state.get('dealer_cards', []),
        'player_total': game_state.get('player_total', 0),
        'dealer_total': game_state.get('dealer_total', 0)
    }

def _calculate_game_result(game_state, original_bet):
    if 'hand_results' in game_state:
        total_payout = Decimal('0')
        for hand in game_state['hand_results']:
            if hand['result'] == 'win':
                total_payout += Decimal(str(hand['bet'])) * 2
            elif hand['result'] == 'draw':
                total_payout += Decimal(str(hand['bet']))
        
        total_bet = sum(Decimal(str(hand['bet'])) for hand in game_state['hand_results'])
        
        if total_payout > total_bet:
            return 'win', total_payout
        elif total_payout == total_bet:
            return 'draw', total_payout
        else:
            return 'lose', total_payout
    else:
        bet_amount = Decimal(str(game_state.get('doubled_bet', original_bet)))
        
        if game_state.get('status') == 'bust' or game_state.get('status') == 'bust_double':
            return 'lose', Decimal('0')
        
        game_result = game_state.get('result', 'lose')
        
        if game_result == 'win':
            return 'win', bet_amount * 2
        elif game_result == 'draw':
            return 'draw', bet_amount
        else:
            return 'lose', Decimal('0')

def bot_statistics(request, player_id):
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
        'games': games[:20],
        'stats': stats
    })