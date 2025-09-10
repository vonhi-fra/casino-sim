from .card import Card
from .hand import Hand
import random

class WebBlackjackGame:    
    def __init__(self):
        self.deck = []
        self.player_hands = [] 
        self.dealer_hand = None
        self.current_hand = 0  
        self.split_mode = False
        
    def create_deck(self, num_decks=20):
        faces = ["A", "J", "Q", "K"]
        colors = ["♠", "♥", "♦", "♣"]
        symbols = faces + [str(i) for i in range(2, 11)]
        
        self.deck = []
        

        for _ in range(num_decks):
            for color in colors:
                for symbol in symbols:
                    self.deck.append(Card(symbol, color))
        
        random.shuffle(self.deck)
    
    def start_game(self, bet_amount):
        self.create_deck(num_decks=1)
        
        player_cards = [self.deck.pop(), self.deck.pop()]
        dealer_cards = [self.deck.pop(), self.deck.pop()]
        
        self.player_hands = [Hand(player_cards, bet_amount)]
        self.dealer_hand = Hand(dealer_cards, 0)
        self.current_hand = 0
        self.split_mode = False
        
        player_total = self.player_hands[0].count_hand()
        
        if player_total == 21:
            return {
                'status': 'blackjack',
                'player_total': player_total,
                'player_cards': self.player_hands[0].get_cards_display(),
                'dealer_visible': str(self.dealer_hand.get_cards()[0]),
                'split_mode': False,
                'current_hand': 0,
                'total_hands': 1,
                'game_over': True
            }
        
        return {
            'status': 'playing',
            'player_total': player_total,
            'player_cards': self.player_hands[0].get_cards_display(),
            'dealer_visible': str(self.dealer_hand.get_cards()[0]),
            'can_double': True,
            'can_split': self.player_hands[0].can_split(),
            'split_mode': False,
            'current_hand': 0,
            'total_hands': 1,
            'game_over': False
        }
    
    def hit(self):
        if not self.player_hands or not self.deck or self.current_hand >= len(self.player_hands):
            return None
        
        current_hand = self.player_hands[self.current_hand]
        new_card = self.deck.pop()
        current_hand.add_card(new_card)
        player_total = current_hand.count_hand()
        
        if player_total > 21:
            if self.split_mode and self.current_hand < len(self.player_hands) - 1:
                self.current_hand += 1
                next_hand = self.player_hands[self.current_hand]
                return {
                    'status': 'hand_bust_next',
                    'bust_hand': self.current_hand - 1,
                    'bust_total': player_total,
                    'current_hand': self.current_hand,
                    'player_total': next_hand.count_hand(),
                    'player_cards': next_hand.get_cards_display(),
                    'all_hands': self._get_all_hands_display(),
                    'new_card': str(new_card),
                    'split_mode': True,
                    'total_hands': len(self.player_hands),
                    'can_double': len(next_hand.get_cards()) == 2,
                    'can_split': next_hand.can_split(),
                    'dealer_visible': str(self.dealer_hand.get_cards()[0]),
                    'game_over': False
                }
            else:
                return {
                    'status': 'bust',
                    'player_total': player_total,
                    'player_cards': current_hand.get_cards_display(),
                    'all_hands': self._get_all_hands_display(),
                    'new_card': str(new_card),
                    'split_mode': self.split_mode,
                    'current_hand': self.current_hand,
                    'total_hands': len(self.player_hands),
                    'dealer_visible': str(self.dealer_hand.get_cards()[0]),
                    'game_over': True
                }
        
        return {
            'status': 'playing',
            'player_total': player_total,
            'player_cards': current_hand.get_cards_display(),
            'all_hands': self._get_all_hands_display(),
            'new_card': str(new_card),
            'can_double': len(current_hand.get_cards()) == 2 and not self.split_mode, 
            'can_split': False,  
            'split_mode': self.split_mode,
            'current_hand': self.current_hand,
            'total_hands': len(self.player_hands),
            'dealer_visible': str(self.dealer_hand.get_cards()[0]),
            'game_over': False
        }
    
    def stand(self):
        if not self.dealer_hand or not self.deck:
            return None
        
        if self.split_mode and self.current_hand < len(self.player_hands) - 1:
            self.current_hand += 1
            return {
                'status': 'next_hand',
                'current_hand': self.current_hand,
                'player_total': self.player_hands[self.current_hand].count_hand(),
                'player_cards': self.player_hands[self.current_hand].get_cards_display(),
                'all_hands': self._get_all_hands_display(),
                'split_mode': True,
                'total_hands': len(self.player_hands),
                'can_double': len(self.player_hands[self.current_hand].get_cards()) == 2,
                'can_split': self.player_hands[self.current_hand].can_split(),
                'game_over': False
            }
        
        dealer_new_cards = []
        while self.dealer_hand.count_hand() < 17:
            new_card = self.deck.pop()
            self.dealer_hand.add_card(new_card)
            dealer_new_cards.append(str(new_card))
        
        dealer_total = self.dealer_hand.count_hand()
        
        results = []
        total_payout = 0
        
        for i, hand in enumerate(self.player_hands):
            player_total = hand.count_hand()
            
            if player_total > 21:
                hand_result = 'lose' 
            elif dealer_total > 21:
                hand_result = 'win'   
            elif dealer_total > player_total:
                hand_result = 'lose'  
            elif dealer_total < player_total:
                hand_result = 'win'   
            else:
                hand_result = 'draw'  
            
            results.append({
                'hand_index': i,
                'player_total': player_total,
                'result': hand_result,
                'cards': hand.get_cards_display(),
                'bet': hand.get_bet()
            })
            
            if hand_result == 'win':
                total_payout += hand.get_bet() * 2
            elif hand_result == 'draw':
                total_payout += hand.get_bet()
        
        return {
            'status': 'finished',
            'dealer_total': dealer_total,
            'dealer_cards': self.dealer_hand.get_cards_display(),
            'dealer_new_cards': dealer_new_cards,
            'all_hands': self._get_all_hands_display(),
            'hand_results': results,
            'total_payout': total_payout,
            'split_mode': self.split_mode,
            'total_hands': len(self.player_hands),
            'game_over': True
        }
    
    def double_down(self):
        if not self.player_hands or len(self.player_hands[self.current_hand].get_cards()) != 2:
            return None
        
        self.player_hands[self.current_hand].double()
        
        new_card = self.deck.pop()
        self.player_hands[self.current_hand].add_card(new_card)
        player_total = self.player_hands[self.current_hand].count_hand()
        
        if player_total > 21:
            return {
                'status': 'bust_double',
                'player_total': player_total,
                'player_cards': self.player_hands[self.current_hand].get_cards_display(),
                'new_card': str(new_card),
                'doubled_bet': self.player_hands[self.current_hand].get_bet(),
                'game_over': True
            }
        
        result = self.stand()
        if result:
            result['doubled_bet'] = self.player_hands[self.current_hand].get_bet()
        return result
    
    def split(self):
        if not self.player_hands or self.current_hand >= len(self.player_hands):
            return None
            
        current_hand = self.player_hands[self.current_hand]
        
        if not current_hand.can_split():
            return None
        
        hand1, hand2 = current_hand.split()
        
        hand1.add_card(self.deck.pop())
        hand2.add_card(self.deck.pop())
        
        self.player_hands[self.current_hand] = hand1
        self.player_hands.insert(self.current_hand + 1, hand2)
        
        self.split_mode = True
        
        return {
            'status': 'split_done',
            'current_hand': self.current_hand,
            'player_total': hand1.count_hand(),
            'player_cards': hand1.get_cards_display(),
            'all_hands': self._get_all_hands_display(),
            'split_mode': True,
            'total_hands': len(self.player_hands),
            'can_double': len(hand1.get_cards()) == 2,
            'can_split': hand1.can_split(), 
            'game_over': False
        }
    
    def _get_all_hands_display(self):
        return [
            {
                'index': i,
                'cards': hand.get_cards_display(),
                'total': hand.count_hand(),
                'bet': hand.get_bet(),
                'is_current': i == self.current_hand,
                'is_bust': hand.count_hand() > 21
            }
            for i, hand in enumerate(self.player_hands)
        ]
        if not self.player_hands:
            return 0
            
        total_payout = 0
        for hand in self.player_hands:
            bet_amount = hand.get_bet()
            
            if result_status == 'lose' or result_status == 'bust':
                continue  
            elif result_status == 'draw':
                total_payout += bet_amount  
            elif result_status == 'win':
                if is_blackjack:
                    total_payout += bet_amount + (bet_amount * 1.5)  
                else:
                    total_payout += bet_amount * 2 
            else:
                total_payout += bet_amount  
        
        return total_payout
    
    def to_dict(self):
        return {
            'deck': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in self.deck],
            'player_hands': [
                {
                    'cards': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in hand.get_cards()],
                    'bet': hand.get_bet()
                }
                for hand in self.player_hands
            ],
            'dealer_cards': [{'symbol': card.get_symbol(), 'color': card.get_color()} for card in self.dealer_hand.get_cards()] if self.dealer_hand else [],
            'current_hand': self.current_hand,
            'split_mode': self.split_mode
        }
    
    def from_dict(self, data):
        print(f"DEBUG from_dict: data keys = {data.keys()}")
        print(f"DEBUG from_dict: player_hands data = {data.get('player_hands', [])}")
        
        self.deck = [Card(card_data['symbol'], card_data['color']) for card_data in data['deck']]
        
        self.player_hands = []
        for i, hand_data in enumerate(data['player_hands']):
            print(f"DEBUG: Creating hand {i}: cards={len(hand_data['cards'])}, bet={hand_data['bet']}")
            cards = [Card(card_data['symbol'], card_data['color']) for card_data in hand_data['cards']]
            hand = Hand(cards, hand_data['bet'])
            self.player_hands.append(hand)
            print(f"DEBUG: Hand {i} created successfully with {len(hand.get_cards())} cards")
        
        if data['dealer_cards']:
            dealer_cards = [Card(card_data['symbol'], card_data['color']) for card_data in data['dealer_cards']]
            self.dealer_hand = Hand(dealer_cards, 0)
        
        self.current_hand = data.get('current_hand', 0)
        self.split_mode = data.get('split_mode', False)
        
        if self.current_hand >= len(self.player_hands):
            self.current_hand = 0
            
        print(f"DEBUG from_dict: Restored {len(self.player_hands)} hands, current_hand={self.current_hand}")