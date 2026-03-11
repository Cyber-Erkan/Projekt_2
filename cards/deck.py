import random
from cards.cards import Card


class Deck:

    def __init__(self, cards=None):
        self.draw_pile = cards if cards else []
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw_card(self):

        if len(self.draw_pile) == 0:
            self.reshuffle_discard()

        if len(self.draw_pile) > 0:
            return self.draw_pile.pop()

        return None

    def draw_cards(self, amount):

        cards = []

        for _ in range(amount):
            card = self.draw_card()

            if card:
                cards.append(card)

        return cards

    def discard_card(self, card):
        self.discard_pile.append(card)

    def reshuffle_discard(self):

        if len(self.discard_pile) == 0:
            return

        print("Reshuffling discard pile")

        self.draw_pile = self.discard_pile
        self.discard_pile = []

        random.shuffle(self.draw_pile)

    def draw_size(self):
        return len(self.draw_pile)

    @staticmethod
    def create_starting_deck():

        cards = []

        for _ in range(5):
            cards.append(Card("Attack", attack=6, cost=1))

        for _ in range(5):
            cards.append(Card("Block", block=5, cost=1))

        cards.append(Card("Heal", heal=4, cost=1))

        deck = Deck(cards)
        deck.shuffle()

        return deck