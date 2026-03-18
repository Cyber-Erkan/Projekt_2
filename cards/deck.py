import random
from cards.card import (
    attack_card,
    defend_card,
    heal_card,
    big_attack_card,
    big_defend_card,
    big_heal_card
)

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
            cards.append(attack_card())

        for _ in range(5):
            cards.append(defend_card())

        cards.append(heal_card())

        cards.append(big_attack_card())
        cards.append(big_defend_card())
        cards.append(big_heal_card())

        deck = Deck(cards)
        deck.shuffle()

        return deck