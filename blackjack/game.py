import card
import hand
import player
import random as rd
def count_val(card):
    total = 0
    if card[0] in ["J", "Q", "K", "1"]:
        total+=10
    elif card[0] == "A":
        total+=11
    else:
        total+=str(card[0])
    return total

def start(nickname = player.Player(None, None, None)):
    faces = ["A", "J", "Q", "K"]
    colors = ["♠", "♥", "♦", "♣"]
    symbols = faces + [str(i) for i in range(2, 11)]

    deck = 7*[symbol + color for color in colors for symbol in symbols]
    rd.shuffle(deck)
    nickname.hand = []
    for i in range(2):
        dealt_card = deck.pop()
        tmp_card = card(dealt_card[0], dealt_card[1], count_val(dealt_card))
        nickname.hand.append(tmp_card)
