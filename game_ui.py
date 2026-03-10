import pygame
import sys
import math
from deck import Deck
from player import Player
from enemy import Enemy

pygame.init()

# --- Screen Setup ---
# WIDTH, HEIGHT = (4096, 4096)
ENEMY_SIZE = (128, 128)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 60)
clock = pygame.time.Clock()

# --- Button Class ---
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (220,220,220), self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        text_surf = font.render(self.text, True, (0,0,0))
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- Card UI Class ---
class CardUI:
    def __init__(self, card):
        self.card = card
        self.x = WIDTH/2
        self.y = HEIGHT + 200
        self.target_x = self.x
        self.target_y = HEIGHT - 200
        self.rect = pygame.Rect(self.x, self.y, 120, 160)
        self.selected = False

    def update(self):
        self.x += (self.target_x - self.x) * 0.2
        self.y += (self.target_y - self.y) * 0.2
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        color = (240,240,240)
        if self.selected:
            color = (180, 220, 240)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        y_offset = 10
        name = font.render(self.card.name, True, (0,0,0))
        screen.blit(name, (self.rect.x + 10, self.rect.y + y_offset))
        y_offset += 30
        if self.card.attack > 0:
            atk = font.render(f"ATK {self.card.attack}", True, (0,0,0))
            screen.blit(atk, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25
        if self.card.block > 0:
            blk = font.render(f"BLK {self.card.block}", True, (0,0,0))
            screen.blit(blk, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25
        if self.card.heal > 0:
            heal = font.render(f"HEAL {self.card.heal}", True, (0,0,0))
            screen.blit(heal, (self.rect.x + 10, self.rect.y + y_offset))
        cost = font.render(str(self.card.cost), True, (0,0,0))
        screen.blit(cost, (self.rect.right - 25, self.rect.y + 10))

# --- Enemy UI Class ---
class EnemyUI:
    def __init__(self, enemy, x, y):

        self.enemy = enemy
        self.rect = pygame.Rect(x, y, 120, 120)

        self.flash = 0
        self.offset = 0

        # Load sprite
        if enemy.name.lower() == "goblin":
            self.img = pygame.image.load("assets/goblin.png").convert_alpha()
            self.img = pygame.transform.scale(self.img, ENEMY_SIZE)
        elif enemy.name.lower() == "slime":
            self.img = pygame.image.load("assets/slime.png").convert_alpha()
            self.img = pygame.transform.scale(self.img, ENEMY_SIZE)
        else:
            self.img = None

    def draw(self):
        color = (200,60,60)
        if self.flash > 0:
            color = (255,255,255)
            self.flash -= 1
        # pygame.draw.rect(screen, color, (self.rect.x, self.rect.y + self.offset, 120, 120))
        if self.img:
            screen.blit(self.img, (self.rect.x, self.rect.y + self.offset))
        else:
            pygame.draw.rect(screen, color, (self.rect.x, self.rect.y + self.offset, 120, 120))
        # HP bar
        hp_ratio = max(0, self.enemy.hp) / self.enemy.max_hp
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y - 20, 120, 10))
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 20, 120 * hp_ratio, 10))
        # Name
        name = font.render(self.enemy.name, True, (255,255,255))
        screen.blit(name, (self.rect.x, self.rect.y + 40))
        # Intent
        if self.enemy.intent:
            action, value = self.enemy.intent
            text = "ATK "+str(value) if action=="attack" else "BUFF "+str(value)
            intent = font.render(text, True, (255,255,0))
            screen.blit(intent, (self.rect.x, self.rect.y - 45))

# --- Layout Hand Function ---
def layout_hand(card_uis):
    n = len(card_uis)
    if n == 0:
        return
    radius = 600
    center_x = WIDTH / 2
    center_y = HEIGHT + 300
    start = -40
    end = 40
    angles = [start + i * (end-start)/(n-1) for i in range(n)] if n>1 else [0]
    for card, angle in zip(card_uis, angles):
        rad = math.radians(angle)
        card.target_x = center_x + radius * math.sin(rad)
        card.target_y = center_y - radius * math.cos(rad)

# --- Player UI ---
def draw_player_ui(player):
    # HP
    hp_ratio = max(0, player.hp)/player.max_hp
    pygame.draw.rect(screen, (255,0,0), (40, HEIGHT-80, 200, 20))
    pygame.draw.rect(screen, (0,255,0), (40, HEIGHT-80, 200*hp_ratio, 20))
    hp_text = font.render(f"HP {max(0, player.hp)}", True, (255,255,255))
    screen.blit(hp_text, (40, HEIGHT-110))
    # Block
    block_text = font.render(f"BLOCK {player.block}", True, (200,200,255))
    screen.blit(block_text, (260, HEIGHT-80))
    # Energy
    energy_ratio = player.energy / player.max_energy
    pygame.draw.rect(screen, (0,0,0), (40, HEIGHT-50, 200, 15))
    pygame.draw.rect(screen, (0,150,255), (40, HEIGHT-50, 200*energy_ratio, 15))
    energy_text = font.render(f"ENERGY {player.energy}", True, (255,255,255))
    screen.blit(energy_text, (40, HEIGHT-30))

# --- Run Game ---
def run_pygame_game():
    deck = Deck.create_starting_deck()
    player = Player(deck)
    enemies = [Enemy("Goblin", 20, 5), Enemy("Slime", 15, 4)]
    player.draw_hand(5)
    for e in enemies:
        e.choose_intent()

    card_uis = [CardUI(c) for c in player.hand]
    enemy_uis = [EnemyUI(enemies[0], WIDTH/2-200, 200), EnemyUI(enemies[1], WIDTH/2+80, 200)]

    end_button = Button(WIDTH-200, HEIGHT-100, 150,50,"END TURN")
    exit_button = Button(WIDTH-140,20,120,40,"EXIT")
    menu_button = Button(WIDTH/2-100, HEIGHT/2,200,60,"MAIN MENU")

    selected_card_ui = None
    running = True

    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill((40,40,40))

        # --- Game Over ---
        if player.hp <= 0:
            text = big_font.render("GAME OVER", True, (255,0,0))
            screen.blit(text, (WIDTH/2-200, HEIGHT/2-150))
            menu_button.draw()
            exit_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_button.clicked(mouse):
                        import ui  # importera först när det behövs
                        ui.start_screen_fullscreen()  # starta start screen med fullscreen
                        return
                    if exit_button.clicked(mouse):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            clock.tick(60)
            continue

        # --- Layout Hand ---
        layout_hand(card_uis)

        # --- Draw Cards ---
        for card in card_uis:
            if card.rect.collidepoint(mouse):
                card.target_y -= 40
            card.update()
            card.draw()

        # --- Draw Enemies ---
        for e in enemy_uis:
            e.draw()

        # --- Draw Player UI ---
        draw_player_ui(player)
        end_button.draw()
        exit_button.draw()

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Exit
                if exit_button.clicked(mouse):
                    pygame.quit()
                    sys.exit()

                # End Turn
                if end_button.clicked(mouse):
                    for e in enemies:
                        e.act(player)
                    player.discard_hand()
                    player.start_turn()
                    player.draw_hand(5)
                    for e in enemies:
                        e.choose_intent()
                    card_uis = [CardUI(c) for c in player.hand]
                    continue

                # Card Selection
                for card in card_uis:
                    if card.rect.collidepoint(mouse):
                        c = card.card
                        if player.energy < c.cost:
                            break
                        if c.block>0:
                            player.block += c.block
                            player.energy -= c.cost
                            player.hand.remove(c)
                            player.deck.discard_card(c)
                            card_uis.remove(card)
                        elif c.heal>0:
                            player.hp = min(player.max_hp, player.hp + c.heal)
                            player.energy -= c.cost
                            player.hand.remove(c)
                            player.deck.discard_card(c)
                            card_uis.remove(card)
                        elif c.attack>0:
                            selected_card_ui = card
                            card.selected = True

                # Attack Enemy
                for enemy_ui in enemy_uis:
                    if enemy_ui.rect.collidepoint(mouse) and selected_card_ui:
                        c = selected_card_ui.card
                        if player.energy >= c.cost:
                            enemy_ui.enemy.hp -= c.attack
                            player.energy -= c.cost
                            enemy_ui.flash = 10
                            player.hand.remove(c)
                            player.deck.discard_card(c)
                            card_uis.remove(selected_card_ui)
                            selected_card_ui = None

        pygame.display.update()
        clock.tick(60)