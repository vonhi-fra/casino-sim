class Card:
    """Klasa reprezentująca kartę do gry"""
    
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
    
    def get_worth(self):
        """Zwraca wartość karty"""
        if self.symbol in ["J", "Q", "K"]:
            return 10
        elif self.symbol == "A":
            return 11
        else:
            return int(self.symbol)
    
    def get_symbol(self):
        return self.symbol
    
    def get_color(self):
        return self.color
    
    def __str__(self):
        return str(self.symbol) + str(self.color)