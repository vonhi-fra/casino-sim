import random as rd

def count_hand(hand):
    total = 0
    aces = 0
    for i in range(len(hand)):
        if hand[i][0] == "A":
            aces += 1
            total += 11
        elif hand[i][0] in ["J", "Q", "K", "1"]:
            total += 10
        else:
            total += int(hand[i][0])

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def play_blackjack(player):
    faces = ["A", "J", "Q", "K"]
    colors = ["♠", "♥", "♦", "♣"]
    symbols = faces + [str(i) for i in range(2, 11)]

    deck = 7*[symbol + color for color in colors for symbol in symbols]
    rd.shuffle(deck)
    bet = int(input("Place your bet: "))
    player-=bet
    player_cards = [deck.pop(), deck.pop()]
    banker_cards = [deck.pop(), deck.pop()]
    print(f"Banker cards: {banker_cards[0]}, Hidden")
    print(f"Your cards: {player_cards[0]}, {player_cards[1]}")
    player_sum = count_hand(player_cards)
    if player_sum == 21:
        player += int(2.5*bet)
        print(f"Blackjack! balance is now {player}$")
    print(player_sum)
    banker_sum = count_hand(banker_cards)
    decision = int(input("What do you want to do?\n1. Hit\n2. Stand\n3. Double\n4. Split\n"))
    while decision == 1:
        new_card = deck.pop()
        print(f"New card {new_card}")
        player_cards.append(new_card)
        if count_hand(player_cards) > 21:
            print(f"You lost (your sum is over 21 ({count_hand(player_cards)}))")
            return player
        decision = int(input("1. Hit\n2. Stand"))
    if decision == 2:
       player_sum = count_hand(player_cards)
    if decision == 3:
        new_card = deck.pop()
        print(f"New card {new_card}")
        player-=bet
        player_cards.append(new_card)
        player_sum = count_hand(player_cards)
        if player_sum > 21:
            print(f"You lost (your sum is over 21 ({count_hand(player_cards)}))")
    if decision == 4:
        player-=bet
        player_hand_1 = [player_cards[0], deck.pop()]
        player_hand_2 = [player_cards[1], deck.pop()]
    player_sum = count_hand(player_cards)
    print(f"Banker cards: {banker_cards[0]}, {banker_cards[1]}")
    while banker_sum <= 16:
        new_card = deck.pop()
        print(f"Bankers new card: {new_card}")
        banker_cards.append(new_card)
        banker_sum = count_hand(banker_cards)
    if decision == 3:
        if banker_sum > 21:
            player += 2*bet
            print(f"You won, balance = {player}$")
        else:
            if banker_sum > player_sum:
                print(f"You lost, balance = {player}$")
            elif banker_sum < player_sum:
                player += 4*bet
                print(f"You won, balance = {player}$")
            elif banker_sum == player_sum:
                player += 2*bet
                print(f"Draw, balance = {player}$")
    else:
        if banker_sum > 21:
            player += 2*bet
            print(f"You won, balance = {player}$")
        else:
            if banker_sum > player_sum:
                print(f"You lost, balance = {player}$")
            elif banker_sum < player_sum:
                player += 2*bet
                print(f"You won, balance = {player}$")
            elif banker_sum == player_sum:
                player += bet
                print(f"Draw, balance = {player}$")
    return player
