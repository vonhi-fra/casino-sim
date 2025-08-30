from .hand import Hand
import uuid
class Player():
    __slots__ = ["nickname", "balance", "id", "hand"]

    def __init__(self, nickname, hand, balance = 10000):
        self.balance = balance
        self.nickname = nickname
        self.hand = hand
        self.id = uuid.uuid4()
    def GetNickname(self):
        return self.nickname
    def GetBalance(self):
        return self.balance
    def GetHand(self):
        return self.hand
    def GetId(self):
        return self.id
    def SetBalance(self, new_balance):
        self.balance = new_balance
    def SetHand(self, new_hand):
        self.hand = new_hand
    def ChangeHand(self, new_hand):
        self.hand = new_hand
    def __str__(self):
        nick = str(self.nickname)
        return nick