import card

class Hand():
    __slots__ = ["cards", "bet"]
    def __init__(self, bet = 0, cards = []):
        self.cards = cards
        self.bet = bet
    def __str__(self):
        value = str(self.bet) + "$"
        return value
    def split(self):
        if len(self.cards) != 2 or self.cards[0] != self.cards[1]:
            return ValueError("Can't split this!")
        hand_1 = Hand(self, self.bet, self.cards[0])
        hand_2 = Hand(self, self.bet, self.cards[1])
        return hand_1, hand_2


        