import pygame, sys, random
from deck import Deck
from player import Player
from enemy import Enemy

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# ----- UI-klasser -----
class CardUI:
    WIDTH, HEIGHT = 120, 180
    def __init__(self, card, x, y):
        self.card = card
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def draw(self):
        # hover-effekt
        draw_rect = self.rect.copy()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            draw_rect.y -= 20
        pygame.draw.rect(screen, (230,230,230), draw_rect)
        pygame.draw.rect(screen, (0,0,0), draw_rect, 2)

        y_offset = 10
        screen.blit(font.render(self.card.name, True, (0,0,0)), (draw_rect.x + 10, draw_rect.y + y_offset))
        y_offset += 40

        if self.card.attack > 0:
            screen.blit(font.render(f"ATK: {self.card.attack}", True, (0,0,0)), (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25
        if self.card.block > 0:
            screen.blit(font.render(f"BLK: {self.card.block}", True, (0,0,0)), (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25
        if self.card.heal > 0:
            screen.blit(font.render(f"HEAL: {self.card.heal}", True, (0,0,0)), (draw_rect.x + 10, draw_rect.y + y_offset))
            y_offset += 25
        screen.blit(font.render(f"COST: {self.card.cost}", True, (0,0,0)), (draw_rect.x + 10, draw_rect.y + 140))

class EnemyUI:
    WIDTH, HEIGHT = 120, 120
    def __init__(self, enemy, x, y):
        self.enemy = enemy
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def draw(self):
        if not self.enemy.is_alive():
            return
        pygame.draw.rect(screen, (180,80,80), self.rect)
        # namn
        screen.blit(font.render(self.enemy.name, True, (255,255,255)), (self.rect.x + 10, self.rect.y - 40))
        # HP bar
        hp_ratio = self.enemy.hp / self.enemy.max_hp
        pygame.draw.rect(screen, (80,80,80), (self.rect.x, self.rect.y - 10, self.WIDTH, 10))
        pygame.draw.rect(screen, (200,50,50), (self.rect.x, self.rect.y - 10, self.WIDTH * hp_ratio, 10))
        # intent
        if self.enemy.intent:
            action, value = self.enemy.intent
            text = ""
            if action == "attack":
                text = f"⚔ {value}"
            elif action == "buff":
                text = f"💪 +{value}"
            text_surface = font.render(text, True, (255,255,0))
            screen.blit(text_surface, (self.rect.x, self.rect.y - 60))

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self):
        pygame.draw.rect(screen, (70,70,70), self.rect)
        pygame.draw.rect(screen, (200,200,200), self.rect, 2)
        text_surface = font.render(self.text, True, (255,255,255))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ----- Hjälpfunktioner -----
def draw_hand(player):
    card_uis = []
    start_x = 50
    spacing = 140
    y = HEIGHT - 200
    for i, card in enumerate(player.hand):
        card_ui = CardUI(card, start_x + i*spacing, y)
        card_ui.draw()
        card_uis.append(card_ui)
    return card_uis

def draw_enemies(enemies):
    enemy_uis = []
    start_x = 300
    spacing = 200
    y = 150
    for i, enemy in enumerate(enemies):
        enemy_ui = EnemyUI(enemy, start_x + i*spacing, y)
        enemy_ui.draw()
        enemy_uis.append(enemy_ui)
    return enemy_uis

def draw_player_ui(player):
    # HP bar
    bar_w, bar_h = 300, 20
    hp_ratio = player.hp / player.max_hp
    pygame.draw.rect(screen, (80,80,80), (50, HEIGHT-350, bar_w, bar_h))
    pygame.draw.rect(screen, (50,200,50), (50, HEIGHT-350, bar_w * hp_ratio, bar_h))
    screen.blit(font.render(f"HP: {player.hp}/{player.max_hp}", True, (255,255,255)), (50, HEIGHT-380))
    # Energy bar
    energy_ratio = player.energy / 3
    pygame.draw.rect(screen, (80,80,80), (50, HEIGHT-310, bar_w, bar_h))
    pygame.draw.rect(screen, (50,50,255), (50, HEIGHT-310, bar_w*energy_ratio, bar_h))
    screen.blit(font.render(f"Energy: {player.energy}/3", True, (255,255,255)), (50, HEIGHT-340))

# ----- Huvudloop -----
def run_pygame_game():
    deck = Deck.create_starting_deck()
    player = Player(deck)
    enemies = [Enemy("Goblin", 20, 5), Enemy("Slime", 15, 4)]
    for e in enemies:
        e.choose_intent()
    player.draw_hand(5)

    end_turn_button = Button("End Turn", WIDTH-180, HEIGHT-400, 150, 50)
    selected_card = None

    running = True
    while running:
        screen.fill((40,120,40))
        enemy_uis = draw_enemies(enemies)
        card_uis = draw_hand(player)
        draw_player_ui(player)
        end_turn_button.draw()
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # End Turn
                if end_turn_button.is_clicked(mouse_pos):
                    player.discard_hand()
                    player.draw_hand(5)
                    player.start_turn()
                    for e in enemies:
                        e.choose_intent()
                    # fiender agerar
                    for e in enemies:
                        e.act(player)
                    continue

                # Klicka kort
                for i, card_ui in enumerate(card_uis):
                    if card_ui.rect.collidepoint(mouse_pos):
                        card = player.hand[i]
                        if card.attack > 0:
                            selected_card = i
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