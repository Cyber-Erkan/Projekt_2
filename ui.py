import pygame
import sys
from game_ui import run_pygame_game

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()


class Button:

    def __init__(self, x, y, w, h, text):

        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):

        pygame.draw.rect(screen, (70,70,70), self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 3)

        text = font.render(self.text, True, (255,255,255))
        screen.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def start_screen():

    start_btn = Button(WIDTH/2-150, HEIGHT/2-80, 300,100,"START")
    exit_btn = Button(WIDTH/2-150, HEIGHT/2+60, 300,100,"EXIT")

    running = True

    while running:

        screen.fill((30,30,40))

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

                if start_btn.clicked(mouse):

                    run_pygame_game()

                if exit_btn.clicked(mouse):

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