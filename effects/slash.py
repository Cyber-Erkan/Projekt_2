import pygame

class SlashEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 12  # antal frames effekten syns

    def update(self):
        self.timer -= 1

    def draw(self, screen):
        size = 60 - self.timer * 4
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.x - size, self.y - size),
            (self.x + size, self.y + size),
            6
        )

    def alive(self):
        return self.timer > 0