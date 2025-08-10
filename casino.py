import random as rn
import math as mt

import roulette
import blackjack
def main():
    f = open("balance.txt", "r")
    player = int(f.read())
    f.close()
    print("--------casino-sim--------")
    print(f"Your balance is {player}$")
    choice = int(input("Choose game:\n1. Roulette\n2. Blackjack\n3. Quit\n"))
    while choice != 3:
        if choice == 1:
            player = roulette.play_roulette(player)
        elif choice == 2:
            player = blackjack.play_blackjack(player)
        choice = int(input("Choose game:\n1. Roulette\n2. Blackjack\n3. Quit"))
    f = open("balance.txt", "w")
    f.write(str(player))
    return
    




if __name__ == "__main__":
    main()