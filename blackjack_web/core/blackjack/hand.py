class Hand:
    
    def __init__(self, cards=None, bet=0):
        self.cards = cards if cards is not None else []
        self.bet = bet
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_cards(self):
        return self.cards
    
    def get_bet(self):
        return self.bet
    
    def double(self):
        self.bet *= 2
    
    def count_hand(self):
        total = 0
        aces = 0
        
        for card in self.cards:
            worth = card.get_worth()
            total += worth
            if card.get_symbol() == "A":
                aces += 1
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        return total
    
    def get_cards_display(self):
        return [str(card) for card in self.cards]
    
    def can_split(self):
        if len(self.cards) != 2:
            return False
        return self.cards[0].get_symbol() == self.cards[1].get_symbol()
    
    def split(self):
        if not self.can_split():
            raise ValueError("Cannot split this hand")
        
        hand1 = Hand([self.cards[0]], self.bet)
        hand2 = Hand([self.cards[1]], self.bet)
        
        return hand1, hand2
    
    def __str__(self):
        return f"Hand: {self.get_cards_display()}, Total: {self.count_hand()}, Bet: ${self.bet}"