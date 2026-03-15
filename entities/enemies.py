from .enemy import Enemy

def Goblin():
    return Enemy(
        name="Goblin",
        hp=20,
        attack=5,
        image="assets/goblin.png"
    )

def Slime():
    return Enemy(
        name="Slime",
        hp=15,
        attack=4,
        image="assets/slime.png"
    )