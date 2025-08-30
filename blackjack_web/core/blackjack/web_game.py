from .card import Card
from .hand import Hand
from .player import Player
import random

class WebBlackjackGame:
    def __init__(self):
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.game_over = False
        
    def start_new_game(self, bet_amount):
        """Rozpoczyna nową grę - rozdaje karty"""
        # Stwórz talię
        faces = ["A", "J", "Q", "K"]
        colors = ["♠", "♥", "♦", "♣"]
        symbols = faces + [str(i) for i in range(2, 11)]
        
        self.deck = []
        for _ in range(7):  # 7 talii jak w twoim kodzie
            for color in colors:
                for symbol in symbols:
                    self.deck.append(Card(symbol, color))
        
        random.shuffle(self.deck)
        
        # Rozdaj karty
        self.player_hand = Hand(bet_amount, [self.deck.pop(), self.deck.pop()])
        self.dealer_hand = Hand(0, [self.deck.pop(), self.deck.pop()])
        
        # Sprawdź blackjack
        if self.player_hand.count_hand() == 21:
            self.game_over = True
            return {
                'status': 'blackjack',
                'player_total': 21,
                'dealer_visible': self.dealer_hand.GetCards()[0],
                'player_cards': self.get_card_strings(self.player_hand.GetCards()),
                'can_double': False,
                'can_split': False
            }
        
        return {
            'status': 'playing',
            'player_total': self.player_hand.count_hand(),
            'dealer_visible': self.dealer_hand.GetCards()[0],
            'player_cards': self.get_card_strings(self.player_hand.GetCards()),
            'can_double': True,
            'can_split': self.can_split()
        }
    
    def hit(self):
        """Gracz dobiera kartę"""
        if self.game_over:
            return None
            
        new_card = self.deck.pop()
        self.player_hand.AddCard(new_card)
        
        player_total = self.player_hand.count_hand()
        
        if player_total > 21:
            self.game_over = True
            return {
                'status': 'bust',
                'player_total': player_total,
                'player_cards': self.get_card_strings(self.player_hand.GetCards()),
                'new_card': str(new_card)
            }
        
        return {
            'status': 'playing',
            'player_total': player_total,
            'player_cards': self.get_card_strings(self.player_hand.GetCards()),
            'new_card': str(new_card),
            'can_double': False,  # Nie można już doublować po hit
            'can_split': False
        }
    
    def stand(self):
        """Gracz pasuje - dealer gra"""
        if self.game_over:
            return None
            
        self.game_over = True
        
        # Dealer dobiera karty
        dealer_actions = []
        while self.dealer_hand.count_hand() < 17:
            new_card = self.deck.pop()
            self.dealer_hand.AddCard(new_card)
            dealer_actions.append(str(new_card))
        
        player_total = self.player_hand.count_hand()
        dealer_total = self.dealer_hand.count_hand()
        
        # Ustal wynik
        if dealer_total > 21:
            result = 'win'
        elif dealer_total > player_total:
            result = 'lose'
        elif dealer_total < player_total:
            result = 'win'
        else:
            result = 'draw'
        
        return {
            'status': 'finished',
            'result': result,
            'player_total': player_total,
            'dealer_total': dealer_total,
            'player_cards': self.get_card_strings(self.player_hand.GetCards()),
            'dealer_cards': self.get_card_strings(self.dealer_hand.GetCards()),
            'dealer_actions': dealer_actions
        }
    
    def double_down(self):
        """Podwojenie stawki"""
        if self.game_over or len(self.player_hand.GetCards()) != 2:
            return None
        
        self.player_hand.Double()
        new_card = self.deck.pop()
        self.player_hand.AddCard(new_card)
        
        player_total = self.player_hand.count_hand()
        
        if player_total > 21:
            self.game_over = True
            return {
                'status': 'bust_double',
                'player_total': player_total,
                'player_cards': self.get_card_strings(self.player_hand.GetCards()),
                'new_card': str(new_card)
            }
        
        # Po double automatycznie stand
        return self.stand()
    
    def can_split(self):
        """Sprawdza czy można splitować"""
        if len(self.player_hand.GetCards()) != 2:
            return False
        
        cards = self.player_hand.GetCards()
        return cards[0].GetSymbol() == cards[1].GetSymbol()
    
    def get_card_strings(self, cards):
        """Konwertuje karty na stringi do wyświetlenia"""
        return [str(card) for card in cards]
    
    def get_payout(self, bet_amount, result, is_blackjack=False):
        """Oblicza wypłatę"""
        if result == 'lose':
            return 0
        elif result == 'draw':
            return bet_amount
        elif result == 'win':
            if is_blackjack:
                return bet_amount + (bet_amount * 1.5)
            else:
                return bet_amount * 2
        else:
            return bet_amount