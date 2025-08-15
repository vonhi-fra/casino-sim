from blackjack.card import Card
from blackjack.hand  import Hand
from blackjack.player import Player
import random as rd
class Game():
    def __init__(self):
        pass

    def start(self, nickname = Player(None, None)):
        faces = ["A", "J", "Q", "K"]
        colors = ["♠", "♥", "♦", "♣"]
        symbols = faces + [str(i) for i in range(2, 11)]

        deck = 7*[symbol + color for color in colors for symbol in symbols]
        rd.shuffle(deck)
        tmp_hand = []
        bet_amount = int(input("How much do you want to bet? "))
        nickname.SetBalance(nickname.GetBalance() - bet_amount)
        dealer_tmp_hand = []
        for i in range(4):
            dealt_card = deck.pop()
            tmp_card = Card(dealt_card[0], dealt_card[1])
            if i == 0 or i == 1:
                dealer_tmp_hand.append(tmp_card)
            else:
                tmp_hand.append(tmp_card)
        dealer_hand = Hand(bet_amount, dealer_tmp_hand)
        player_hand = Hand(bet_amount, tmp_hand)
        nickname.SetHand(player_hand)
        print(f"Dealer cards: {dealer_hand.printDealerHand()}")
        print(f"Your cards: {nickname.GetHand().printHand()}; value: {nickname.GetHand().count_hand()}")
        decision = int(input("What do you want to do?\n1. Hit\n2. Stand\n3. Double\n4. Split\n"))
        while decision == 1:
            new_card = deck.pop()
            tmp_card = Card(new_card[0], new_card[1])
            print(f"New card {tmp_card}")
            nickname.GetHand().AddCard(tmp_card)
            if nickname.GetHand().count_hand() > 21:
                print(f"You lost (your sum is over 21 ({nickname.GetHand().count_hand()}))")
                return nickname
            
            decision = int(input("1. Hit\n2. Stand\n"))
        player_sum = 0
        if decision == 2:
            player_sum = nickname.GetHand().count_hand() 
        if decision == 3:
            nickname.GetHand().Double()
            nickname.SetBalance(nickname.GetBalance() - bet_amount)
            new_card = deck.pop()
            tmp_card = Card(new_card[0], new_card[1])
            nickname.GetHand().AddCard(tmp_card)
            print(f"Your hand now: {nickname.GetHand().printHand()}")
            if nickname.GetHand().count_hand() > 21:
                print(f"You lost (your sum is over 21 ({nickname.GetHand().count_hand()}))")
                return nickname
        if decision == 4:
            print("")
        print(f"Dealer's hand: {dealer_hand.printHand()}")
        while dealer_hand.count_hand() < 17:
            dealt_card = deck.pop()
            tmp_card = Card(dealt_card[0], dealt_card[1])
            dealer_hand.AddCard(tmp_card)
            print(f"Dealer's new card: {str(tmp_card)}")
        dealer_sum = dealer_hand.count_hand()

        print(f"Dealer's sum: {dealer_sum}")
        if decision == 3:
            if dealer_sum > 21:
                nickname.SetBalance(nickname.GetBalance() + 4*nickname.GetHand().GetBet())
                print(f"You won, balance = {nickname.GetBalance()}$")
            else:
                if dealer_sum > player_sum:
                    print(f"You lost, balance = {nickname.GetBalance()}$")
                elif dealer_sum < player_sum:
                    nickname.SetBalance(nickname.GetBalance() + 4*nickname.GetHand().GetBet())
                    print(f"You won, balance = {nickname.GetBalance()}$")
                elif dealer_sum == player_sum:
                    nickname.SetBalance(nickname.GetBalance() + 2*nickname.GetHand().GetBet())
                    print(f"Draw, balance = {nickname.GetBalance()}$")
        else:
            if dealer_sum > 21:
                nickname.SetBalance(nickname.GetBalance() + 2*nickname.GetHand().GetBet())
                print(f"You won, balance = {nickname.GetBalance()}$")
            else:
                if dealer_sum > player_sum:
                    print(f"You lost, balance = {nickname.GetBalance()}$")
                elif dealer_sum < player_sum:
                    nickname.SetBalance(nickname.GetBalance() + 2*nickname.GetHand().GetBet())
                    print(f"You won, balance = {nickname.GetBalance()}$")
                elif dealer_sum == player_sum:
                    nickname.SetBalance(nickname.GetBalance() + nickname.GetHand().GetBet())
                    print(f"Draw, balance = {nickname.GetBalance()}$")
        return nickname          
