import random
from cards import Card   # 🔥 importerar Card från cards.py


class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        return None

    @staticmethod
    def create_starting_deck():
        cards = []

        for _ in range(5):
            cards.append(Card(name="Attack", attack=6))

        for _ in range(5):
            cards.append(Card(name="Block", block=5))

        for _ in range(3):
            cards.append(Card(name="Heal", heal=4))

        deck = Deck(cards)
        deck.shuffle()
        return deck