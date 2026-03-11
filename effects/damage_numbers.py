import pygame

class DamageNumber:
    def __init__(self, x, y, value, color=(255, 80, 80)):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.timer = 60  # antal frames talet syns

    def update(self):
        self.y -= 1  # flytta uppåt
        self.timer -= 1

    def draw(self, screen, font):
        text = font.render(str(self.value), True, self.color)
        screen.blit(text, (self.x, self.y))

    def alive(self):
        return self.timer > 0