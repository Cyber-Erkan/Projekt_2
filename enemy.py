import random


class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.intent = None

    def is_alive(self):
        return self.hp > 0

    def choose_intent(self):

        action = random.choice(["attack", "buff"])

        if action == "attack":
            self.intent = ("attack", self.attack)

        if action == "buff":
            self.intent = ("buff", 2)

    def show_intent(self):

        if not self.is_alive():
            return

        action, value = self.intent

        if action == "attack":
            print(f"{self.name} tänker attackera för {value}")

        if action == "buff":
            print(f"{self.name} tänker öka sin attack med {value}")

    def act(self, player):

        if not self.is_alive():
            return

        action, value = self.intent

        if action == "attack":
            print(f"{self.name} attackerar!")
            player.take_damage(value)

        if action == "buff":
            self.attack += value
            print(f"{self.name} blir starkare! (+{value} attack)")