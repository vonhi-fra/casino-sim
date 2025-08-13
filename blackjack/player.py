from blackjack.hand import Hand
import uuid
class Player():
    __slots__ = ["nickname", "balance", "id", "hand"]

    def __init__(self, nickname, hand, balance = 10000):
        self.balance = balance
        self.nickname = nickname
        self.hand = hand
        self.id = uuid.uuid4()
        
    def __str__(self):
        nick = str(self.nickname)
        return nick