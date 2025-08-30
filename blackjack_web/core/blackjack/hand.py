class Hand:
    """Klasa reprezentująca rękę kart"""
    
    def __init__(self, cards=None, bet=0):
        self.cards = cards if cards is not None else []
        self.bet = bet
    
    def add_card(self, card):
        """Dodaje kartę do ręki"""
        self.cards.append(card)
    
    def get_cards(self):
        """Zwraca listę kart"""
        return self.cards
    
    def get_bet(self):
        """Zwraca stawkę"""
        return self.bet
    
    def double(self):
        """Podwaja stawkę"""
        self.bet *= 2
    
    def count_hand(self):
        """Oblicza wartość ręki (z obsługą asów)"""
        total = 0
        aces = 0
        
        for card in self.cards:
            worth = card.get_worth()
            total += worth
            if card.get_symbol() == "A":
                aces += 1
        
        # Obsługa asów - zmień 11 na 1 jeśli przekraczamy 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        return total
    
    def get_cards_display(self):
        """Zwraca karty jako stringi do wyświetlenia"""
        return [str(card) for card in self.cards]
    
    def can_split(self):
        """Sprawdza czy można splitować (dwie karty o tej samej wartości)"""
        if len(self.cards) != 2:
            return False
        return self.cards[0].get_symbol() == self.cards[1].get_symbol()
    
    def __str__(self):
        return f"Hand: {self.get_cards_display()}, Total: {self.count_hand()}, Bet: ${self.bet}"