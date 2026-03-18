from cards.cards import Card


def attack_card():
    return Card("Attack", attack=6, cost=1)


def defend_card():
    return Card("Defend", block=5, cost=1)


def heal_card():
    return Card("Heal", heal=4, cost=1)


def big_attack_card():
    return Card("Attack +", attack=12, cost=2)


def big_defend_card():
    return Card("Defend +", block=10, cost=2)


def big_heal_card():
    return Card("Heal +", heal=8, cost=2)