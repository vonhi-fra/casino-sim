from blackjack.game import Game
from engine.utils import create_player

def main():
    decision = 5
    while decision != 4:
        decision = int(input("What do you want to do?\n1. Create player\n2. Play blackjack\n3. Play roulette\n4. Quit\n"))
        if decision == 2:
            blackjack = Game()
            blackjack.start()
        if decision == 1:
            nick = input("State your username: ")
            balance = int(input("How much do you want to deposit? "))
            user = create_player(nick, balance)
            print(f"Your id = {user.id}")
            f = open("engine/data.txt", "w")
            f.write(f"{user.id}; {user.nickname}; {user.balance}")
            f.close()
if __name__ == "__main__":
    main()