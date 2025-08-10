class Card():
    __slots__ = ["symbol", "color", "worth"]

    def __init__(self, symbol, color, worth):
        self.symbol = symbol
        self.color = color
        self.worth = worth
    def __str__(self):
        whole_card = str(self.symbol) + str(self.color)
        return whole_card
        