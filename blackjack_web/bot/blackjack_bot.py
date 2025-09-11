class BlackjackBot:

    def __init__(self):
        self.hard_strategy = {
            5: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            6: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            7: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            8: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            9: {2: 'hit', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            10: {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'hit', 11: 'hit'},
            11: {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'double', 11: 'double'},
            12: {2: 'hit', 3: 'hit', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            13: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            14: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            15: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            16: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            17: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            18: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            19: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            20: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            21: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
        }
        
        self.soft_strategy = {
            13: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,2
            14: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,3
            15: {2: 'hit', 3: 'hit', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,4
            16: {2: 'hit', 3: 'hit', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,5
            17: {2: 'hit', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,6
            18: {2: 'stand', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'stand', 8: 'stand', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,7
            19: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,8
            20: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,9
            21: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,10
        }
        
        self.pairs_strategy = {
            'A,A': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'split', 9: 'split', 10: 'split', 11: 'split'},
            '2,2': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '3,3': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '4,4': {2: 'hit', 3: 'hit', 4: 'hit', 5: 'split', 6: 'split', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '5,5': {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'hit', 11: 'hit'},
            '6,6': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '7,7': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '8,8': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'split', 9: 'split', 10: 'split', 11: 'split'},
            '9,9': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'stand', 8: 'split', 9: 'split', 10: 'stand', 11: 'stand'},
            '10,10': {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
        }

    def normalize_card_value(self, card_str):

        symbol = card_str[0] if len(card_str) > 1 else card_str
        
        if symbol == 'A':
            return 11
        elif symbol in ['J', 'Q', 'K']:
            return 10
        else:
            try:
                return int(symbol) if len(symbol) == 1 else int(card_str[:-1])
            except:
                return 10

    def calculate_hand_value(self, cards):
        total = 0
        aces = 0
        
        for card in cards:
            value = self.normalize_card_value(card)
            if value == 11:
                aces += 1
                total += 11
            else:
                total += value
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        return total, aces > 0

    def is_pair(self, cards):
        if len(cards) != 2:
            return False
        
        card1_symbol = cards[0][0] if len(cards[0]) > 1 else cards[0]
        card2_symbol = cards[1][0] if len(cards[1]) > 1 else cards[1]
        
        if card1_symbol in ['J', 'Q', 'K']:
            card1_symbol = '10'
        if card2_symbol in ['J', 'Q', 'K']:
            card2_symbol = '10'
            
        return card1_symbol == card2_symbol

    def get_pair_key(self, cards):
        card1_symbol = cards[0][0] if len(cards[0]) > 1 else cards[0]
        card2_symbol = cards[1][0] if len(cards[1]) > 1 else cards[1]
        
        if card1_symbol in ['J', 'Q', 'K']:
            card1_symbol = '10'
        if card2_symbol in ['J', 'Q', 'K']:
            card2_symbol = '10'
        
        return f"{card1_symbol},{card2_symbol}"

    def get_optimal_action(self, player_cards, dealer_up_card, can_double=True, can_split=True, player_balance=0, current_bet=0):

        dealer_value = self.normalize_card_value(dealer_up_card)
        if dealer_value == 11:
            dealer_value = 11
        elif dealer_value > 10:
            dealer_value = 10
        
        player_total, has_soft_ace = self.calculate_hand_value(player_cards)
        
        if can_split and len(player_cards) == 2 and self.is_pair(player_cards):
            if player_balance >= current_bet:
                pair_key = self.get_pair_key(player_cards)
                if pair_key in self.pairs_strategy:
                    action = self.pairs_strategy[pair_key].get(dealer_value, 'hit')
                    if action == 'split':
                        return 'split'
        
        if has_soft_ace and player_total <= 21:
            if player_total in self.soft_strategy:
                action = self.soft_strategy[player_total].get(dealer_value, 'hit')
                if action == 'double' and can_double and player_balance >= current_bet:
                    return 'double'
                elif action == 'double':
                    return 'hit'
                else:
                    return action
        
        if player_total in self.hard_strategy:
            action = self.hard_strategy[player_total].get(dealer_value, 'hit')
            if action == 'double' and can_double and player_balance >= current_bet:
                return 'double'
            elif action == 'double':
                return 'hit'
            else:
                return action
        
        if player_total >= 17:
            return 'stand'
        else:
            return 'hit'

    def get_betting_strategy(self, balance, min_bet=100, max_bet=1000):
        bet = max(min_bet, min(max_bet, int(balance * 0.02)))
        return min(bet, balance)

