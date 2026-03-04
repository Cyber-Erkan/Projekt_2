class Card:
    def __init__(self, name, attack=0, block=0, heal=0):
        self.name = name
        self.attack = attack
        self.block = block
        self.heal = heal

    def __str__(self):
        return f"{self.name} (ATK: {self.attack}, BLK: {self.block}, HEAL: {self.heal})"