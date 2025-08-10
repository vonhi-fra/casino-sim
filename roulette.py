import random as rd
import numpy as np


def play_roulette(player):
    bets = []
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17,
            20, 22, 24, 26, 28, 29, 31, 33, 35]
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36]
    green = 0
    number_bets = int(input("How many bets do you want?"))
    print("Bet options:\n1. Red\n2. Black\n3. 1st half\n4. 2nd half\n5. Even\n6. Odd\n7. Numbers")
    print("Place your bets:\n")
    idx = 0
    while idx < number_bets:
        print(f"bets remaining {number_bets}\n")
        current_bet = [input("Put your choice(1-7): "), input("Put your bet amount: ")]
        if int(current_bet[0]) == 7:
            number = int(input("Put down your number: "))
            current_bet.append(number)
            bets.append(current_bet)
        else:
            bets.append(current_bet)
        player-=int(current_bet[1])
        idx+=1
    roll_outcome = rd.randint(0,36)
    print(f"Roll outcome {roll_outcome}", end="")
    if roll_outcome in red:
        print("(red)")
    else:
        print("(black)")
    idx = 0
    while idx < number_bets:
        if int(bets[idx][0]) == 1:
            if roll_outcome in red:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 2:
            if roll_outcome in black:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 3:
            if roll_outcome >= 1 and roll_outcome <=18:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 4:
            if roll_outcome >= 19 and roll_outcome <=36:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 5:
            if roll_outcome%2 == 0:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 6:
            if roll_outcome%2 == 1:
                player += 2*int(bets[idx][1])

        elif int(bets[idx][0]) == 7:
            if roll_outcome == bets[idx][2]:
                player += 36*int(bets[idx][1])
        idx+=1
    print(f"Your balance: {player}$")
    return player
            
            
