from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Player, Game
from core.blackjack.game import WebBlackjackGame
from decimal import Decimal
import json

def home(request):
    """Strona główna - lista graczy"""
    players = Player.objects.all()
    return render(request, 'blackjack/home.html', {'players': players})

def create_player(request):
    """Tworzenie nowego gracza"""
    if request.method == 'POST':
        nickname = request.POST['nickname']
        balance = request.POST.get('balance', 10000)
        
        player = Player.objects.create(
            nickname=nickname,
            balance=Decimal(balance)
        )
        return redirect('play_game', player_id=player.id)
    
    return render(request, 'blackjack/create_player.html')

def play_game(request, player_id):
    """Główna funkcja gry blackjack"""
    player = get_object_or_404(Player, id=player_id)
    
    # Sprawdź czy jest aktywna gra w session
    if 'active_game' in request.session and request.method == 'GET':
        game_data = request.session['active_game']
        return render(request, 'blackjack/game_active.html', {
            'player': player,
            'game_state': game_data['game_state'],
            'bet_amount': game_data['bet_amount']
        })
    
    if request.method == 'POST':
        # Rozpoczęcie nowej gry
        if 'bet_amount' in request.POST:
            return _start_new_game(request, player)
        
        # Akcje gracza (hit/stand/double)
        elif 'action' in request.POST:
            return _handle_player_action(request, player)
    
    # GET - pokaż formularz zakładu
    return render(request, 'blackjack/play_game.html', {'player': player})

def _start_new_game(request, player):
    """Rozpoczyna nową grę blackjack"""
    bet_amount = Decimal(request.POST['bet_amount'])
    
    if bet_amount > player.balance:
        return render(request, 'blackjack/play_game.html', {
            'player': player,
            'error': 'Insufficient balance!'
        })
    
    # Stwórz nową grę
    game = WebBlackjackGame()
    game_state = game.start_game(float(bet_amount))
    
    # Zapisz w session
    request.session['active_game'] = {
        'game_state': game_state,
        'bet_amount': float(bet_amount),
        'game_data': game.to_dict()
    }
    
    # Jeśli blackjack - od razu zakończ
    if game_state['status'] == 'blackjack':
        return _finish_game(request, player, game_state, bet_amount, 'blackjack', game)
    
    return render(request, 'blackjack/game_active.html', {
        'player': player,
        'game_state': game_state,
        'bet_amount': bet_amount
    })

def _handle_player_action(request, player):
    if 'active_game' not in request.session:
        return redirect('play_game', player_id=player.id)
    
    action = request.POST.get('action', 'NONE')
    game_session = request.session['active_game']
    original_bet = Decimal(str(game_session['bet_amount']))
    
    # Przywróć grę
    game = WebBlackjackGame()
    game.from_dict(game_session['game_data'])
    
    # Wykonaj akcję
    result = None
    if action == 'hit':
        result = game.hit()
    elif action == 'stand':
        result = game.stand()
    elif action == 'double':
        result = game.double_down()
    elif action == 'split':
        result = game.split()
    
    if result is None:
        return redirect('play_game', player_id=player.id)
    
    # ✅ Zapisz CAŁY obiekt z powrotem do sesji
    request.session['active_game'] = {
        'game_state': result,
        'bet_amount': float(original_bet),
        'game_data': game.to_dict()
    }
    request.session.modified = True   # <-- kluczowe!
    
    # Koniec gry
    if result.get('game_over'):
        return _finish_split_game(request, player, result, original_bet, game)
    
    # Gra trwa dalej
    return render(request, 'blackjack/game_active.html', {
        'player': player,
        'game_state': result,
        'bet_amount': original_bet
    })


def _finish_split_game(request, player, game_state, original_bet_amount, game_instance):
    """Kończy grę ze split i oblicza wyniki dla wszystkich rąk"""
    original_bet = Decimal(str(original_bet_amount))
    total_payout = Decimal('0')
    
    # Jeśli to split - oblicz wyniki dla każdej ręki
    if 'hand_results' in game_state:
        hand_results = game_state['hand_results']
        total_bet = sum(Decimal(str(hand['bet'])) for hand in hand_results)
        
        for hand in hand_results:
            if hand['result'] == 'win':
                total_payout += Decimal(str(hand['bet'])) * 2
            elif hand['result'] == 'draw':
                total_payout += Decimal(str(hand['bet']))
        
        # Główny wynik gry
        if total_payout > total_bet:
            main_result = 'win'
        elif total_payout == total_bet:
            main_result = 'draw'
        else:
            main_result = 'lose'
            
        display_bet = total_bet
    else:
        # Pojedyncza ręka lub bust
        game_result = game_state.get('result', 'lose')
        
        # Sprawdź czy to double down
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
    
    # Aktualizuj balans gracza
    balance_change = total_payout - display_bet
    player.balance += balance_change
    player.save()
    
    # Zapisz grę do bazy danych
    Game.objects.create(
        player=player,
        bet_amount=display_bet,
        player_cards=game_state.get('all_hands', [{}])[0].get('cards', []) if game_state.get('all_hands') else game_state.get('player_cards', []),
        dealer_cards=game_state.get('dealer_cards', []),
        result=main_result,
        payout=total_payout
    )
    
    # Usuń grę z session
    if 'active_game' in request.session:
        del request.session['active_game']
    
    return render(request, 'blackjack/game_result.html', {
        'player': player,
        'game_state': game_state,
        'result': main_result,
        'payout': total_payout,
        'bet_amount': display_bet,
        'split_results': game_state.get('hand_results', [])
    })

def _finish_game(request, player, game_state, bet_amount, game_result, game_instance):
    """Kończy grę i zapisuje wyniki"""
    # Oblicz wypłatę
    payout = Decimal('0')
    if game_result == 'win':
        payout = bet_amount * 2
    elif game_result == 'blackjack':
        payout = bet_amount + (bet_amount * Decimal('1.5'))  # 3:2 za blackjack
    elif game_result == 'draw':
        payout = bet_amount
    
    # Aktualizuj balans gracza
    balance_change = payout - bet_amount
    player.balance += balance_change
    player.save()
    
    # Zapisz grę do bazy danych
    Game.objects.create(
        player=player,
        bet_amount=bet_amount,
        player_cards=game_state.get('player_cards', []),
        dealer_cards=game_state.get('dealer_cards', [game_state.get('dealer_visible', '')]),
        result=game_result,
        payout=payout
    )
    
    # Usuń grę z session
    if 'active_game' in request.session:
        del request.session['active_game']
    
    return render(request, 'blackjack/game_result.html', {
        'player': player,
        'game_state': game_state,
        'result': game_result,
        'payout': payout,
        'bet_amount': bet_amount
    })