from .card import Card
from .hand import Hand
import random

class WebBlackjackGame:
    """Główna klasa gry blackjack dla aplikacji webowej"""
    
    def __init__(self):
        self.deck = []
        self.player_hand = None
        self.dealer_hand = None
        
    def create_deck(self, num_decks=1):
        """Tworzy i tasuje talię kart"""
        faces = ["A", "J", "Q", "K"]
        colors = ["♠", "♥", "♦", "♣"]
        symbols = faces + [str(i) for i in range(2, 11)]
        
        self.deck = []
        
        # Dodaj określoną liczbę talii
        for _ in range(num_decks):
            for color in colors:
                for symbol in symbols:
                    self.deck.append(Card(symbol, color))
        
        random.shuffle(self.deck)
    
    def start_game(self, bet_amount):
        """Rozpoczyna nową grę - rozdaje początkowe karty"""
        self.create_deck(num_decks=1)  # Można zmienić liczbę talii
        
        # Rozdaj karty (gracz-dealer-gracz-dealer)
        player_cards = [self.deck.pop(), self.deck.pop()]
        dealer_cards = [self.deck.pop(), self.deck.pop()]
        
        self.player_hand = Hand(player_cards, bet_amount)
        self.dealer_hand = Hand(dealer_cards, 0)
        
        player_total = self.player_hand.count_hand()
        
        # Sprawdź blackjack
        if player_total == 21:
            return {
                'status': 'blackjack',
                'player_total': player_total,
                'player_cards': self.player_hand.get_cards_display(),
                'dealer_visible': str(self.dealer_hand.get_cards()[0]),
                'game_over': True
            }
        
        return {
            'status': 'playing',
            'player_total': player_total,
            'player_cards': self.player_hand.get_cards_display(),
            'dealer_visible': str(self.dealer_hand.get_cards()[0]),
            'can_double': True,
            'can_split': self.player_hand.can_split(),
            'game_over': False
        }
    
    def hit(self):
        """Gracz dobiera kartę"""
        if not self.player_hand or not self.deck:
            return None
            
        new_card = self.deck.pop()
        self.player_hand.add_card(new_card)
        player_total = self.player_hand.count_hand()
        
        if player_total > 21:
            return {
                'status': 'bust',
                'player_total': player_total,
                'player_cards': self.player_hand.get_cards_display(),
                'new_card': str(new_card),
                'game_over': True
            }
        
        return {
            'status': 'playing',
            'player_total': player_total,
            'player_cards': self.player_hand.get_cards_display(),
            'new_card': str(new_card),
            'can_double': False,  # Nie można doublować po hit
            'can_split': False,
            'game_over': False
        }
    
    def stand(self):
        """Gracz kończy swoją turę - dealer gra zgodnie z regułami"""
        if not self.dealer_hand or not self.deck:
            return None
        
        # Dealer dobiera karty (musi dobierać do 17, musi stanąć na 17 lub więcej)
        dealer_new_cards = []
        while self.dealer_hand.count_hand() < 17:
            new_card = self.deck.pop()
            self.dealer_hand.add_card(new_card)
            dealer_new_cards.append(str(new_card))
        
        player_total = self.player_hand.count_hand()
        dealer_total = self.dealer_hand.count_hand()
        
        # Określ wynik gry
        if dealer_total > 21:
            result = 'win'  # Dealer bust
        elif dealer_total > player_total:
            result = 'lose'  # Dealer ma więcej
        elif dealer_total < player_total:
            result = 'win'   # Gracz ma więcej
        else:
            result = 'draw'  # Remis
        
        return {
            'status': 'finished',
            'result': result,
            'player_total': player_total,
            'dealer_total': dealer_total,
            'player_cards': self.player_hand.get_cards_display(),
            'dealer_cards': self.dealer_hand.get_cards_display(),
            'dealer_new_cards': dealer_new_cards,
            'game_over': True
        }
    
    def double_down(self):
        """Podwojenie stawki - gracz dostaje dokładnie jedną kartę i automatycznie stand"""
        if not self.player_hand or len(self.player_hand.get_cards()) != 2:
            return None
        
        # Podwój stawkę
        self.player_hand.double()
        
        # Dobierz dokładnie jedną kartę
        new_card = self.deck.pop()
        self.player_hand.add_card(new_card)
        player_total = self.player_hand.count_hand()
        
        if player_total > 21:
            return {
                'status': 'bust_double',
                'player_total': player_total,
                'player_cards': self.player_hand.get_cards_display(),
                'new_card': str(new_card),
                'doubled_bet': self.player_hand.get_bet(),
                'game_over': True
            }
        
        # Po double automatycznie wykonaj stand
        result = self.stand()
        if result:
            result['doubled_bet'] = self.player_hand.get_bet()
        return result
    
    def get_payout(self, result_status, is_blackjack=False):
        """Oblicza wypłatę na podstawie wyniku"""
        bet_amount = self.player_hand.get_bet()
        
        if result_status == 'lose' or result_status == 'bust':
            return 0
        elif result_status == 'draw':
            return bet_amount  # Zwrot stawki
        elif result_status == 'win':
            if is_blackjack:
                return bet_amount + (bet_amount * 1.5)  # 3:2 za blackjack
            else:
                return bet_amount * 2  # 1:1 za zwykłą wygraną
        else:
            return bet_amount  # Default - zwrot stawki
    
    # Metody do serializacji (do sessions)
    def to_dict(self):
        """Serializuje stan gry do słownika (dla Django sessions)"""
        return {
            'deck': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in self.deck],
            'player_cards': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in self.player_hand.get_cards()] if self.player_hand else [],
            'dealer_cards': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in self.dealer_hand.get_cards()] if self.dealer_hand else [],
            'player_bet': self.player_hand.get_bet() if self.player_hand else 0
        }
    
    def from_dict(self, data):
        """Przywraca stan gry ze słownika (z Django sessions)"""
        # Przywróć deck
        self.deck = [Card(card_data['symbol'], card_data['color']) for card_data in data['deck']]
        
        # Przywróć ręce
        if data['player_cards']:
            player_cards = [Card(card_data['symbol'], card_data['color']) for card_data in data['player_cards']]
            self.player_hand = Hand(player_cards, data['player_bet'])
        
        if data['dealer_cards']:
            dealer_cards = [Card(card_data['symbol'], card_data['color']) for card_data in data['dealer_cards']]
            self.dealer_hand = Hand(dealer_cards, 0)