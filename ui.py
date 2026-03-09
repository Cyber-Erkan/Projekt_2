import pygame
import sys
from main import run_game
from game_ui import run_pygame_game

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Roguelike")

font_title = pygame.font.SysFont(None, 80)
font_button = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, (70, 70, 70), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        text_surface = font_button.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


start_button = Button("Start Game", WIDTH//2 - 100, 300, 200, 60)
quit_button = Button("Quit", WIDTH//2 - 100, 400, 200, 60)


def start_screen():

    while True:

        screen.fill((30, 30, 40))

        title = font_title.render("Card Roguelike", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH//2, 150))

        screen.blit(title, title_rect)

        start_button.draw()
        quit_button.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.is_clicked(event.pos):
                    run_pygame_game()  # startar ert spel

                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start_screen()