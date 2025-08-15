class Card():
    __slots__ = ["symbol", "color", "worth"]

    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
    def GetWorth(self):
        total = 0
        if self.symbol in ["J", "Q", "K", "1"]:
            total+=10
        elif self.symbol == "A":
            total+=11
        else:
            total+=int(self.symbol)
        self.worth = total
        return total
    def GetSymbol(self):
        return self.symbol
    def GetColor(self):
        return self.color
    def __str__(self):
        whole_card = str(self.symbol) + str(self.color)
        return whole_card
        