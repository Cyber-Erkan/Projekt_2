import random


class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.intent = None

    def is_alive(self):
        return self.hp > 0

    def choose_intent(self):
        import random
        action = random.choice(["attack", "buff"])
        if action == "attack":
            self.intent = ("attack", self.attack)
        elif action == "buff":
            self.intent = ("buff", 2)

    def act(self, player):
        if not self.is_alive():
            return
        action, value = self.intent
        if action == "attack":
            blocked = min(player.block, value)
            damage = value - blocked
            player.block -= blocked
            player.hp -= damage
            print(f"{self.name} attackerar! Skada: {damage} (blockerade {blocked})")
        elif action == "buff":
            self.attack += value
            print(f"{self.name} buffar sig själv! (+{value} attack)")