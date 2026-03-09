import msvcrt
from os import system
from deck import Deck
from player import Player
from enemy import Enemy

def get_input():
    key = msvcrt.getch().decode("utf-8")
    return key

def next_level():
    print("Level klar! (dummy funktion)")


def all_enemies_dead(enemies):
    return all(not e.is_alive() for e in enemies)


def enemy_turn(enemies, player):

    print("\n--- Fiendernas tur ---")

    for enemy in enemies:
        enemy.act(player)

    print("Spelarens HP:", player.hp)


def show_enemies(enemies):

    print("\nFiender:")

    for enemy in enemies:
        if enemy.is_alive():
            print(f"{enemy.name} HP: {enemy.hp}")
            enemy.show_intent()


def end_turn(player, enemies):

    player.discard_hand()

    player.start_turn()   # reset energy här
    player.draw_hand(3)

    for enemy in enemies:
        enemy.choose_intent()

    enemy_turn(enemies, player)


def run_game():

    deck = Deck.create_starting_deck()
    player = Player(deck)

    enemies = [
        Enemy("Goblin", 20, 5),
        Enemy("Slime", 15, 4)
    ]

    player.draw_hand(5)

    for enemy in enemies:
        enemy.choose_intent()

    while True:

        if player.hp <= 0:
            print("\nDu dog!")

            restart = input("Starta om? (y/n): ")

            if restart.lower() == "y":
                return
            else:
                exit()

        if all_enemies_dead(enemies):
            next_level()
            return
        system("cls")  # rensa skärmen
        print("\n--- Din tur ---")

        player.start_turn()

        show_enemies(enemies)
        player.show_hand()

        print("\nSpela kort (nummer), 'e' = end turn, 'd' = discard pile, 'q' = quit")

        choice = get_input()
        print(choice)

        if choice == "q":
            exit()
        if choice == "d":
            player.deck.show_discard()
            continue
        if choice == "e":
            end_turn(player, enemies)
            continue

        try:
            index = int(choice) - 1
            player.play_card(index, enemies)

        except:
            print("Fel input")


def main():

    while True:
        run_game()


if __name__ == "__main__":
    main()