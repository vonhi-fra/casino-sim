from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Player, Game
from core.blackjack.game import WebBlackjackGame
from decimal import Decimal
import json
from core.roulette.game import RouletteGame

def home(request):
    players = Player.objects.all()
    return render(request, 'blackjack/home.html', {'players': players})

def create_player(request):
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
    player = get_object_or_404(Player, id=player_id)
    
    if 'active_game' in request.session and request.method == 'GET':
        game_data = request.session['active_game']
        return render(request, 'blackjack/game_active.html', {
            'player': player,
            'game_state': game_data['game_state'],
            'bet_amount': game_data['bet_amount']
        })
    
    if request.method == 'POST':
        if 'bet_amount' in request.POST:
            return _start_new_game(request, player)
        
        elif 'action' in request.POST:
            return _handle_player_action(request, player)
    
    return render(request, 'blackjack/play_game.html', {'player': player})

def _start_new_game(request, player):
    bet_amount = Decimal(request.POST['bet_amount'])
    
    if bet_amount > player.balance:
        return render(request, 'blackjack/play_game.html', {
            'player': player,
            'error': 'Insufficient balance!'
        })
    
    game = WebBlackjackGame()
    game_state = game.start_game(float(bet_amount))
    
    request.session['active_game'] = {
        'game_state': game_state,
        'bet_amount': float(bet_amount),
        'game_data': game.to_dict()
    }
    
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
    
    game = WebBlackjackGame()
    game.from_dict(game_session['game_data'])
    
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
    
    request.session['active_game'] = {
        'game_state': result,
        'bet_amount': float(original_bet),
        'game_data': game.to_dict()
    }
    request.session.modified = True
    
    if result.get('game_over'):
        return _finish_split_game(request, player, result, original_bet, game)
    
    return render(request, 'blackjack/game_active.html', {
        'player': player,
        'game_state': result,
        'bet_amount': original_bet
    })


def _finish_split_game(request, player, game_state, original_bet_amount, game_instance):
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
    
    return render(request, 'blackjack/game_result.html', {
        'player': player,
        'game_state': game_state,
        'result': main_result,
        'payout': total_payout,
        'bet_amount': display_bet,
        'split_results': game_state.get('hand_results', [])
    })

def _finish_game(request, player, game_state, bet_amount, game_result, game_instance):
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
    
    return render(request, 'blackjack/game_result.html', {
        'player': player,
        'game_state': game_state,
        'result': game_result,
        'payout': payout,
        'bet_amount': bet_amount
    })
def play_roulette(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    roulette = RouletteGame()
    
    if 'roulette_bets' in request.session and request.method == 'GET':
        bets = request.session['roulette_bets']
        return render(request, 'blackjack/roulette_betting.html', {
            'player': player,
            'bet_types': roulette.get_bet_types(),
            'current_bets': bets,
            'total_bet': sum(bet['amount'] for bet in bets)
        })
    
    if request.method == 'POST':
        if 'add_bet' in request.POST:
            return _add_roulette_bet(request, player, roulette)
        
        elif 'remove_bet' in request.POST:
            return _remove_roulette_bet(request, player)
        
        elif 'spin' in request.POST:
            return _spin_roulette(request, player, roulette)
    
    return render(request, 'blackjack/roulette_betting.html', {
        'player': player,
        'bet_types': roulette.get_bet_types(),
        'current_bets': [],
        'total_bet': 0
    })

def _add_roulette_bet(request, player, roulette):
    bet_type = request.POST.get('bet_type')
    bet_amount = Decimal(request.POST.get('bet_amount', '0'))
    bet_number = request.POST.get('bet_number')
    
    if bet_amount <= 0 or bet_amount > player.balance:
        return render(request, 'blackjack/roulette_betting.html', {
            'player': player,
            'bet_types': roulette.get_bet_types(),
            'current_bets': request.session.get('roulette_bets', []),
            'total_bet': sum(bet['amount'] for bet in request.session.get('roulette_bets', [])),
            'error': 'Invalid bet amount!'
        })
    
    if bet_type == 'number':
        try:
            bet_number = int(bet_number)
            if bet_number < 0 or bet_number > 36:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'blackjack/roulette_betting.html', {
                'player': player,
                'bet_types': roulette.get_bet_types(),
                'current_bets': request.session.get('roulette_bets', []),
                'total_bet': sum(bet['amount'] for bet in request.session.get('roulette_bets', [])),
                'error': 'Number must be between 0 and 36!'
            })
    else:
        bet_number = None
    
    if 'roulette_bets' not in request.session:
        request.session['roulette_bets'] = []
    
    new_bet = {
        'type': bet_type,
        'amount': float(bet_amount),
        'number': bet_number,
        'display_name': roulette.get_bet_types()[bet_type]['name']
    }
    
    if bet_type == 'number':
        new_bet['display_name'] = f"Number {bet_number}"
    
    request.session['roulette_bets'].append(new_bet)
    request.session.modified = True
    
    current_bets = request.session['roulette_bets']
    total_current_bet = sum(bet['amount'] for bet in current_bets)
    
    return render(request, 'blackjack/roulette_betting.html', {
        'player': player,
        'bet_types': roulette.get_bet_types(),
        'current_bets': current_bets,
        'total_bet': total_current_bet,
        'success': f'Added ${bet_amount} bet on {new_bet["display_name"]}'
    })

def _remove_roulette_bet(request, player):
    bet_index = int(request.POST.get('bet_index', -1))
    
    if 'roulette_bets' in request.session and 0 <= bet_index < len(request.session['roulette_bets']):
        removed_bet = request.session['roulette_bets'].pop(bet_index)
        request.session.modified = True
        
        success_msg = f'Removed ${removed_bet["amount"]} bet on {removed_bet["display_name"]}'
    else:
        success_msg = None
    
    roulette = RouletteGame()
    current_bets = request.session.get('roulette_bets', [])
    
    return render(request, 'blackjack/roulette_betting.html', {
        'player': player,
        'bet_types': roulette.get_bet_types(),
        'current_bets': current_bets,
        'total_bet': sum(bet['amount'] for bet in current_bets),
        'success': success_msg
    })

def _spin_roulette(request, player, roulette):
    if 'roulette_bets' not in request.session or not request.session['roulette_bets']:
        return render(request, 'blackjack/roulette_betting.html', {
            'player': player,
            'bet_types': roulette.get_bet_types(),
            'current_bets': [],
            'total_bet': 0,
            'error': 'No bets placed!'
        })
    
    bets_data = request.session['roulette_bets']
    total_bet_amount = sum(Decimal(str(bet['amount'])) for bet in bets_data)
    
    if total_bet_amount > player.balance:
        return render(request, 'blackjack/roulette_betting.html', {
            'player': player,
            'bet_types': roulette.get_bet_types(),
            'current_bets': bets_data,
            'total_bet': float(total_bet_amount),
            'error': 'Insufficient balance!'
        })
    
    player.balance -= total_bet_amount
    
    game_result = roulette.play_round(bets_data)
    
    player.balance += game_result['total_payout']
    player.save()
    
    from .models import RouletteGameModel, RouletteBet
    
    roulette_game = RouletteGameModel.objects.create(
        player=player,
        total_bet=game_result['total_bet'],
        winning_number=game_result['winning_number'],
        winning_color=game_result['winning_color'],
        total_payout=game_result['total_payout'],
        bets_data=bets_data
    )
    
    for bet_result in game_result['bet_results']:
        RouletteBet.objects.create(
            game=roulette_game,
            bet_type=bet_result['type'],
            bet_amount=bet_result['amount'],
            bet_number=bet_result.get('number'),
            won=bet_result['won'],
            payout=bet_result['payout']
        )
    
    del request.session['roulette_bets']
    
    return render(request, 'blackjack/roulette_result.html', {
        'player': player,
        'game_result': game_result,
        'net_result': game_result['total_payout'] - game_result['total_bet']
    })
