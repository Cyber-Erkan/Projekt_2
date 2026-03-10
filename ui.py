import pygame
import sys
from game_ui import run_pygame_game
from deck import Deck
from player import Player
from enemy import Enemy

pygame.init()

# Fullscreen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Card Game")

font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (70, 70, 70), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def start_screen():
    start_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100, "Start Game")
    exit_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 100, "Exit")

    running = True
    while running:
        screen.fill((40, 40, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if start_btn.is_clicked(mouse):
                    # Skapa player och enemies här
                    deck = Deck.create_starting_deck()
                    player = Player(deck)
                    player.draw_hand(5)

                    enemies = [
                        Enemy("Goblin", 30, 5),
                        Enemy("Slime", 25, 4)
                    ]
                    for e in enemies:
                        e.max_hp = e.hp  # för UI

                    run_pygame_game()
                if exit_btn.is_clicked(mouse):
                    pygame.quit()
                    sys.exit()

        start_btn.draw()
        exit_btn.draw()
        pygame.display.flip()
        clock.tick(60)

def start_screen_fullscreen():
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    start_screen()

if __name__ == "__main__":
    start_screen_fullscreen()
    run_pygame_game()