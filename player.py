from cards import Card

class Player:
    def __init__(self, deck):
        self.max_hp = 30
        self.hp = 30
        self.block = 0
        self.energy = 3
        self.max_energy = 3  # <-- lägg till här
        self.deck = deck
        self.hand = []

    def start_turn(self):
        self.energy = 3

    def draw_hand(self, amount=5):
        new_cards = self.deck.draw_cards(amount)
        self.hand.extend(new_cards)

    def discard_hand(self):
        for card in self.hand:
            self.deck.discard_card(card)

        self.hand = []
        self.block = 0

