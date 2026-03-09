import random
from cards import Card



class Deck:
    def __init__(self, cards=None):
        self.draw_pile = cards if cards is not None else []
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw_cards(self, amount):
        drawn = []

        for _ in range(amount):
            card = self.draw_card()
            if card:
                drawn.append(card)

        return drawn

    def draw_card(self):

        if len(self.draw_pile) == 0:
            self.reshuffle_discard()

        if len(self.draw_pile) > 0:
            return self.draw_pile.pop()

        return None

    def discard_card(self, card):
        self.discard_pile.append(card)

    def reshuffle_discard(self):
        if len(self.discard_pile) == 0:
            return

        print("Shufflar discard pile till ny draw pile!")

        self.draw_pile = self.discard_pile
        self.discard_pile = []
        random.shuffle(self.draw_pile)
    def show_discard(self):

        print("\nDiscard pile:")

        if not self.discard_pile:
            print("Tom")
            return

        for card in self.discard_pile:
            print(card)


    def draw_size(self):
        return len(self.draw_pile)

    @staticmethod
    def create_starting_deck():
        cards = []

        for _ in range(5):
            cards.append(Card(name="Attack", attack=6, cost=1))

        for _ in range(5):
            cards.append(Card(name="Block", block=5, cost=1))

        for _ in range(1):
            cards.append(Card(name="Heal", heal=4, cost=1))

        deck = Deck(cards)
        deck.shuffle()
        return deck