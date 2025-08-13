from blackjack.card import Card
from blackjack.hand  import Hand
from blackjack.player import Player
import random as rd
class Game():
    def __init__(self):
        pass
    def count_val(self, card):
        total = 0
        if card[0] in ["J", "Q", "K", "1"]:
            total+=10
        elif card[0] == "A":
            total+=11
        else:
            total+=int(card[0])
        return total

    def count_hand(self, hand):
        total = 0
        aces = 0
        for i in range(len(hand.cards)):
            total+=hand.cards[i].worth
            if hand.cards[i].symbol == "A":
                aces+=1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total


    def start(self, nickname = Player(None, None)):
        faces = ["A", "J", "Q", "K"]
        colors = ["♠", "♥", "♦", "♣"]
        symbols = faces + [str(i) for i in range(2, 11)]

        deck = 7*[symbol + color for color in colors for symbol in symbols]
        rd.shuffle(deck)
        tmp_hand = []
        bet_amount = int(input("How much do you want to bet? "))
        nickname.balance -= bet_amount
        dealer_tmp_hand = []
        for i in range(4):
            dealt_card = deck.pop()
            tmp_card = Card(dealt_card[0], dealt_card[1], self.count_val(dealt_card))
            if i == 0 or i == 1:
                dealer_tmp_hand.append(tmp_card)
            else:
                tmp_hand.append(tmp_card)
        dealer_hand = Hand(bet_amount, dealer_tmp_hand)
        player_hand = Hand(bet_amount, tmp_hand)
        nickname.hand = player_hand
        print(f"Dealer cards: {dealer_hand.dealer()}")
        print(f"Your cards: {nickname.hand.visible()}; value: {self.count_hand(nickname.hand)}")
        decision = int(input("What do you want to do?\n1. Hit\n2. Stand\n3. Double\n4. Split\n"))
        while decision == 1:
            new_card = deck.pop()
            tmp_card = Card(new_card[0], new_card[1], self.count_val(new_card))
            print(f"New card {tmp_card}")
            nickname.hand.cards.append(tmp_card)
            if self.count_hand(nickname.hand) > 21:
                print(f"You lost (your sum is over 21 ({self.count_hand(nickname.hand)}))")
                return nickname
            
            decision = int(input("1. Hit\n2. Stand\n"))
        player_sum = 0
        if decision == 2:
            player_sum = self.count_hand(nickname.hand)
        if decision == 3:
            nickname.hand.bet *= 2
            nickname.balance -= bet_amount
            new_card = deck.pop()
            tmp_card = Card(new_card[0], new_card[1], self.count_val(new_card))
            nickname.hand.cards.append(tmp_card)
            if self.count_hand(nickname.hand) > 21:
                print(f"You lost (your sum is over 21 ({self.count_hand(nickname.hand)}))")
                return nickname
        if decision == 4:
            print("")
        print(f"Dealer's hand: {dealer_hand.visible()}")
        while self.count_hand(dealer_hand) < 17:
            dealt_card = deck.pop()
            tmp_card = Card(dealt_card[0], dealt_card[1], self.count_val(dealt_card))
            dealer_hand.cards.append(tmp_card)
            print(f"Dealer's new card: {str(tmp_card)}")
        dealer_sum = self.count_hand(dealer_hand)

        print(f"Dealer's sum: {dealer_sum}")
        if decision == 3:
            if dealer_sum > 21:
                player += 2*nickname.hand.bet
                print(f"You won, balance = {nickname.balance}$")
            else:
                if dealer_sum > player_sum:
                    print(f"You lost, balance = {nickname.balance}$")
                elif dealer_sum < player_sum:
                    nickname.balance += 4*nickname.hand.bet
                    print(f"You won, balance = {nickname.balance}$")
                elif dealer_sum == player_sum:
                    nickname.balance += 2*nickname.hand.bet
                    print(f"Draw, balance = {nickname.balance}$")
        else:
            if dealer_sum > 21:
                nickname.balance += 2*nickname.hand.bet
                print(f"You won, balance = {nickname.balance}$")
            else:
                if dealer_sum > player_sum:
                    print(f"You lost, balance = {nickname.balance}$")
                elif dealer_sum < player_sum:
                    nickname.balance += 2*nickname.hand.bet
                    print(f"You won, balance = {nickname.balance}$")
                elif dealer_sum == player_sum:
                    nickname.balance += nickname.hand.bet
                    print(f"Draw, balance = {nickname.balance}$")
        return nickname          
