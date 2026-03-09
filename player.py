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

    def show_hand(self):

        print("\nDin hand:")
        for i, card in enumerate(self.hand):
            print(f"{i+1}: {card}")
        print(f"Draw pile: {self.deck.draw_size()} kort")
        print(f"Discard pile: {len(self.deck.discard_pile)} kort")
        print(f"\nHP: {self.hp}/{self.max_hp} | Block: {self.block} | Energy: {self.energy}")

    def play_card(self, index, enemies):

        if index < 0 or index >= len(self.hand):
            print("Ogiltigt kort")
            return

        card = self.hand[index]

        if self.energy < card.cost:
            print("Inte tillräckligt med energy!")
            return

        self.energy -= card.cost
        self.hand.pop(index)

        if card.attack > 0:

            alive_enemies = [e for e in enemies if e.is_alive()]

            print("\nVälj fiende:")

            for i, enemy in enumerate(alive_enemies):
                print(f"{i+1}: {enemy.name} (HP {enemy.hp})")
            
            choice = int(input("> ")) - 1
            target = alive_enemies[choice]

            target.hp -= card.attack
            print(f"Du gör {card.attack} skada på {target.name}")

        if card.block > 0:
            self.block += card.block
            print(f"Du får {card.block} block")

        if card.heal > 0:
            self.hp = min(self.max_hp, self.hp + card.heal)
            print(f"Du läker {card.heal} HP")

        self.deck.discard_card(card)

    def take_damage(self, damage):

        blocked = min(self.block, damage)
        damage -= blocked
        self.block -= blocked

        self.hp -= damage

        print(f"Du tog {damage} skada (blockerade {blocked})")