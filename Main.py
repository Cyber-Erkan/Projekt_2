from deck import Deck   # 🔥 importerar Deck från deck.py


def main():
    deck = Deck.create_starting_deck()

    print("Drar 3 kort:")
    for _ in range(3):
        card = deck.draw_card()
        if card:
            print(card)


if __name__ == "__main__":
    main()