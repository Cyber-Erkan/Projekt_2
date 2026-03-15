import pygame
from ui import start_screen
from game import run_game

pygame.init()

running = True

while running:

    action = start_screen()

    if action == "start":
        run_game()

    elif action == "exit":
        running = False

pygame.quit()


