class Player:

    def __init__(self, deck):

        self.max_hp = 30
        self.hp = 30

        self.block = 0

        self.energy = 3
        self.max_energy = 3

        self.deck = deck
        self.hand = []

    def start_turn(self):

        self.energy = self.max_energy

    def draw_hand(self, amount=5):

        cards = self.deck.draw_cards(amount)

        self.hand.extend(cards)

    def discard_hand(self):

        for card in self.hand:
            self.deck.discard_card(card)

        self.hand = []
        self.block = 0

    def can_play(self, card):

        return self.energy >= card.cost

    def play_block(self, card):

        if not self.can_play(card):
            return False

        self.block += card.block
        self.energy -= card.cost

        self.hand.remove(card)
        self.deck.discard_card(card)

        return True

    def play_heal(self, card):

        if not self.can_play(card):
            return False

        self.hp = min(self.max_hp, self.hp + card.heal)
        self.energy -= card.cost

        self.hand.remove(card)
        self.deck.discard_card(card)

        return True

    def play_attack(self, card, enemy):

        if not self.can_play(card):
            return False

        enemy.hp -= card.attack
        self.energy -= card.cost

        self.hand.remove(card)
        self.deck.discard_card(card)

        return True