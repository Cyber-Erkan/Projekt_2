import pygame
import sys
from deck import Deck
from player import Player
from enemy import Enemy

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Roguelike")

font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()


class CardUI:

    WIDTH = 120
    HEIGHT = 180

    def __init__(self, card, x, y):
        self.card = card
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def draw(self):

        mouse_pos = pygame.mouse.get_pos()

    # lyft kortet om musen är över
        draw_rect = self.rect.copy()

        if self.rect.collidepoint(mouse_pos):
            draw_rect.y -= 20

        pygame.draw.rect(screen, (230, 230, 230), draw_rect)
        pygame.draw.rect(screen, (0, 0, 0), draw_rect, 2)

        y_offset = 10

        name = font.render(self.card.name, True, (0, 0, 0))
        screen.blit(name, (draw_rect.x + 10, draw_rect.y + y_offset))

        y_offset += 40

        if self.card.attack > 0:
            text = font.render(f"ATK: {self.card.attack}", True, (0, 0, 0))
            screen.blit(text, (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25

        if self.card.block > 0:
            text = font.render(f"BLK: {self.card.block}", True, (0, 0, 0))
            screen.blit(text, (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25

        if self.card.heal > 0:
            text = font.render(f"HEAL: {self.card.heal}", True, (0, 0, 0))
            screen.blit(text, (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25

        cost = font.render(f"COST: {self.card.cost}", True, (0, 0, 0))
        screen.blit(cost, (draw_rect.x + 10, draw_rect.y + 140))


def draw_hand(player):

    card_spacing = 140
    start_x = WIDTH // 2 - (len(player.hand) * card_spacing) // 2

    card_uis = []

    for i, card in enumerate(player.hand):

        x = start_x + i * card_spacing
        y = HEIGHT - 220

        card_ui = CardUI(card, x, y)
        card_ui.draw()

        card_uis.append(card_ui)

    return card_uis

def draw_enemies(enemies):

    enemy_uis = []

    start_x = 300
    spacing = 200

    for i, enemy in enumerate(enemies):

        x = start_x + i * spacing
        y = 200

        enemy_ui = EnemyUI(enemy, x, y)
        enemy_ui.draw()

        enemy_uis.append(enemy_ui)

    return enemy_uis

def draw_player_ui(player):
    # HP bar
    bar_width = 300
    bar_height = 20
    hp_ratio = player.hp / player.max_hp

    pygame.draw.rect(screen, (80,80,80), (50, HEIGHT-350, bar_width, bar_height))
    pygame.draw.rect(screen, (50,200,50), (50, HEIGHT-350, bar_width * hp_ratio, bar_height))
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (255,255,255))
    screen.blit(hp_text, (50, HEIGHT-380))

    # Energy bar
    pygame.draw.rect(screen, (80,80,80), (50, HEIGHT-310, bar_width, bar_height))
    pygame.draw.rect(screen, (50,50,255), (50, HEIGHT-310, bar_width * (player.energy/3), bar_height))
    energy_text = font.render(f"Energy: {player.energy}/3", True, (255,255,255))
    screen.blit(energy_text, (50, HEIGHT-340))

class EnemyUI:

    WIDTH = 120
    HEIGHT = 120

    def __init__(self, enemy, x, y):
        self.enemy = enemy
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def draw(self):
        if not self.enemy.is_alive():
            return

        pygame.draw.rect(screen, (180,80,80), self.rect)

    # namn
        name = font.render(self.enemy.name, True, (255,255,255))
        screen.blit(name, (self.rect.x + 10, self.rect.y - 40))

    # health bar
        bar_width = self.WIDTH
        bar_height = 10
        hp_ratio = self.enemy.hp / self.enemy.max_hp
        pygame.draw.rect(screen, (80,80,80), (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, (200,50,50), (self.rect.x, self.rect.y - 10, bar_width * hp_ratio, bar_height))

    # enemy intent – rita bara om den finns
        if self.enemy.intent:
            action, value = self.enemy.intent
            intent_text = ""
            if action == "attack":
                intent_text = f"⚔ {value}"
            elif action == "buff":
                intent_text = f"💪 +{value}"
        # skapa text_surface först
            text_surface = font.render(intent_text, True, (255,255,0))
            screen.blit(text_surface, (self.rect.x, self.rect.y - 60))

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, (70,70,70), self.rect)
        pygame.draw.rect(screen, (200,200,200), self.rect, 2)
        text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    

def run_pygame_game():

    end_turn_button = Button("End Turn", WIDTH-180, HEIGHT-400, 150, 50)
    deck = Deck.create_starting_deck()
    player = Player(deck)

    enemies = [
        Enemy("Goblin", 20, 5),
        Enemy("Slime", 15, 4)
    ]

    player.draw_hand(5)
    selected_card = None

    running = True

    while running:

        screen.fill((40, 120, 40))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Sätt här, nu finns variabeln

        # Klicka på End Turn
                if end_turn_button.is_clicked(mouse_pos):
                    player.discard_hand()
                    player.draw_hand(5)
                    player.start_turn()

            # Fiender väljer ny intent
                    for enemy in enemies:
                        enemy.choose_intent()

            # Fiender agerar
                    for enemy in enemies:
                        enemy.act(player)

                    continue  # hoppa över resten av event-hanteringen

        # Klicka kort
                for i, card_ui in enumerate(card_uis):
                    if card_ui.rect.collidepoint(mouse_pos):
                        card = player.hand[i]
                        if card.attack > 0:
                            selected_card = i
                            print("Select enemy to attack")
                        else:
                            player.play_card(i, enemies)
                            break

        # Klicka enemy
                if selected_card is not None:
                    for enemy_ui in enemy_uis:
                        if enemy_ui.rect.collidepoint(mouse_pos):
                            enemy = enemy_ui.enemy
                            card = player.hand[selected_card]

                            enemy.hp -= card.attack
                            player.energy -= card.cost
                            player.deck.discard_card(card)
                            player.hand.pop(selected_card)
                            selected_card = None
                            break


        screen.fill((40,120,40))

        enemy_uis = draw_enemies(enemies)
        card_uis = draw_hand(player)
        draw_player_ui(player)
        end_turn_button.draw()

        pygame.display.flip()
        clock.tick(60)