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
    choice = int(input("Choose game:\n1. Roulette\n2. Blackjack\n"))
    if choice == 1:
        player = roulette.play_roulette(player)
    elif choice == 2:
        player = blackjack.play_blackjack(player)
    f = open("balance.txt", "w")
    f.write(str(player))
    




if __name__ == "__main__":
    main()