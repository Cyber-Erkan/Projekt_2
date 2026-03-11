class Card:

    def __init__(self, name, attack=0, block=0, heal=0, cost=1):

        self.name = name
        self.attack = attack
        self.block = block
        self.heal = heal
        self.cost = cost

    def is_attack(self):
        return self.attack > 0

    def is_block(self):
        return self.block > 0

    def is_heal(self):
        return self.heal > 0

    def __str__(self):

        return f"{self.name} ATK:{self.attack} BLK:{self.block} HEAL:{self.heal} COST:{self.cost}"