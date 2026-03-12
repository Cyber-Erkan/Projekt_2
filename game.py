import pygame
import sys
import math

from cards.deck import Deck
from entities.player import Player
from entities.enemy import Enemy

from effects.slash import SlashEffect
from effects.damage_numbers import DamageNumber

pygame.init()

# --- Screen ---
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 70)
clock = pygame.time.Clock()

ENEMY_SIZE = (128,128)


# ---------------- CARD UI ----------------
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
        color = (180,220,240) if self.selected else (240,240,240)
        pygame.draw.rect(screen,color,self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,2)

        y = 10
        name = font.render(self.card.name,True,(0,0,0))
        screen.blit(name,(self.rect.x+10,self.rect.y+y))
        y += 30

        if self.card.attack > 0:
            atk = font.render(f"ATK {self.card.attack}",True,(0,0,0))
            screen.blit(atk,(self.rect.x+10,self.rect.y+y))
            y += 25
        if self.card.block > 0:
            blk = font.render(f"BLK {self.card.block}",True,(0,0,0))
            screen.blit(blk,(self.rect.x+10,self.rect.y+y))
            y += 25
        if self.card.heal > 0:
            heal = font.render(f"HEAL {self.card.heal}",True,(0,0,0))
            screen.blit(heal,(self.rect.x+10,self.rect.y+y))
        cost = font.render(str(self.card.cost),True,(0,0,0))
        screen.blit(cost,(self.rect.right-25,self.rect.y+10))


# ---------------- ENEMY UI ----------------
class EnemyUI:
    def __init__(self, enemy, x, y):
        self.base_x = x
        self.enemy = enemy
        self.rect = pygame.Rect(x,y,128,128)
        self.flash = 0
        self.img = None
        if enemy.name.lower() == "goblin":
            img = pygame.image.load("assets/goblin.png").convert_alpha()
            self.img = pygame.transform.scale(img,ENEMY_SIZE)
        elif enemy.name.lower() == "slime":
            img = pygame.image.load("assets/slime.png").convert_alpha()
            self.img = pygame.transform.scale(img,ENEMY_SIZE)

    def update(self):
        # Death animation
        if self.enemy.death_anim > 0:
            self.rect.y += 2
            self.enemy.death_anim -= 1
        # Attack shake
        if self.enemy.attack_anim > 0:
            offset = 20 if self.enemy.attack_anim > 10 else -20
            self.rect.x = self.base_x + offset
            self.enemy.attack_anim -= 1
        else:
            self.rect.x = self.base_x

    def draw(self):
        if self.flash > 0:
            pygame.draw.rect(screen,(255,255,255),self.rect)
            self.flash -= 1
        if self.img:
            screen.blit(self.img,(self.rect.x,self.rect.y))
        else:
            pygame.draw.rect(screen,(200,60,60),self.rect)

        # HP BAR
        ratio = max(0,self.enemy.hp) / self.enemy.max_hp
        pygame.draw.rect(screen,(255,0,0),(self.rect.x,self.rect.y-20,120,10))
        pygame.draw.rect(screen,(0,255,0),(self.rect.x,self.rect.y-20,120*ratio,10))

        # HP text
        hp_text = font.render(f"{max(0,self.enemy.hp)} / {self.enemy.max_hp}", True, (255,255,255))
        screen.blit(hp_text,(self.rect.x,self.rect.y-40))

        # Intent
        if self.enemy.intent:
            action,value = self.enemy.intent
            text = f"ATK {value}" if action=="attack" else f"BUFF {value}"
            intent = font.render(text,True,(255,255,0))
            screen.blit(intent,(self.rect.x,self.rect.y-55))


# ---------------- HAND LAYOUT ----------------
def layout_hand(card_uis):
    n = len(card_uis)
    if n==0: return
    radius = 600
    center_x = WIDTH/2
    center_y = HEIGHT + 300
    start, end = -40, 40
    angles = [start + i*(end-start)/(n-1) for i in range(n)] if n>1 else [0]
    for card, angle in zip(card_uis,angles):
        rad = math.radians(angle)
        card.target_x = center_x + radius * math.sin(rad)
        card.target_y = center_y - radius * math.cos(rad)


# ---------------- PLAYER UI ----------------
def draw_player_ui(player):
    hp_ratio = max(0,player.hp)/player.max_hp
    pygame.draw.rect(screen,(255,0,0),(40,HEIGHT-80,200,20))
    pygame.draw.rect(screen,(0,255,0),(40,HEIGHT-80,200*hp_ratio,20))
    hp_text = font.render(f"HP {max(0,player.hp)}",True,(255,255,255))
    screen.blit(hp_text,(40,HEIGHT-110))
    block_text = font.render(f"BLOCK {player.block}",True,(200,200,255))
    screen.blit(block_text,(260,HEIGHT-80))
    energy_ratio = player.energy/player.max_energy
    pygame.draw.rect(screen,(0,0,0),(40,HEIGHT-50,200,15))
    pygame.draw.rect(screen,(0,150,255),(40,HEIGHT-50,200*energy_ratio,15))
    energy_text = font.render(f"ENERGY {player.energy}",True,(255,255,255))
    screen.blit(energy_text,(40,HEIGHT-30))


# ---------------- STAGE SYSTEM ----------------
def all_enemies_dead(enemies):
    return all(not e.is_alive() for e in enemies)

def start_next_stage(stage):
    if stage==1:
        enemies = [Enemy("Goblin",20,5), Enemy("Slime",15,4)]
    elif stage==2:
        enemies = [Enemy("Goblin",25,6), Enemy("Goblin",25,6)]
    elif stage==3:
        enemies = [Enemy("Slime",35,8)]
    else:
        enemies = [Enemy("Goblin",30,7), Enemy("Slime",30,7)]
    return enemies


# ---------------- GAME LOOP ----------------
def run_game():
    deck = Deck.create_starting_deck()
    player = Player(deck)
    stage = 1
    enemies = start_next_stage(stage)
    player.draw_hand(5)

    enemy_uis = [EnemyUI(e, WIDTH/2 + (i-len(enemies)/2)*200, 200) for i,e in enumerate(enemies)]
    for e in enemies:   e.choose_intent()

    card_uis = [CardUI(c) for c in player.hand]
    damage_numbers = []
    slash_effects = []

    dragging_card = None

    end_turn_btn = pygame.Rect(WIDTH-200, HEIGHT-100, 150,50)
    exit_btn = pygame.Rect(WIDTH-140, 20, 120,40)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill((40,40,40))

        # Draw stage
        stage_text = font.render(f"Stage {stage}", True,(255,255,255))
        screen.blit(stage_text,(WIDTH/2-50,30))

        # Check game over
        if player.hp <= 0:
            over_text = big_font.render("GAME OVER",True,(255,0,0))
            screen.blit(over_text,(WIDTH/2-200,HEIGHT/2-150))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: sys.exit()
            continue

        # Layout hand
        layout_hand(card_uis)

        # Draw cards
        for card in card_uis:
            if card==dragging_card:
                card.x = mouse[0]-60
                card.y = mouse[1]-80
            else:
                if card.rect.collidepoint(mouse): card.target_y -= 40
                card.update()
            card.draw()

        # Draw enemies
        for e in enemy_uis:
            e.update()
            e.draw()

        # Draw effects
        for d in damage_numbers: d.update(); d.draw(screen,font)
        damage_numbers = [d for d in damage_numbers if d.alive()]
        for s in slash_effects: s.update(); s.draw(screen)
        slash_effects = [s for s in slash_effects if s.alive()]

        # Draw player UI
        draw_player_ui(player)

        # Draw buttons
        pygame.draw.rect(screen,(220,220,220),end_turn_btn)
        pygame.draw.rect(screen,(0,0,0),end_turn_btn,2)
        pygame.draw.rect(screen,(220,220,220),exit_btn)
        pygame.draw.rect(screen,(0,0,0),exit_btn,2)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: sys.exit()

            # Mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn.collidepoint(mouse): sys.exit()
                if end_turn_btn.collidepoint(mouse):
                    # End turn
                    for e in enemies:
                        e.act(player)
                        e.attack_anim = 20
                        damage_numbers.append(DamageNumber(WIDTH//2, HEIGHT-120, 0))
                    player.discard_hand()
                    player.start_turn()
                    player.draw_hand(5)
                    card_uis = [CardUI(c) for c in player.hand]
                    for e in enemies:
                        if e.is_alive(): e.choose_intent()
                    else:
                        e.intent = None
                    if all_enemies_dead(enemies):
                        stage += 1
                        enemies = start_next_stage(stage)
                        enemy_uis = [EnemyUI(e, WIDTH/2 + (i-len(enemies)/2)*200, 200) for i,e in enumerate(enemies)]
                    for e in enemies:
                        if e.is_alive(): e.choose_intent()
                    continue

                for card in card_uis:
                    if card.rect.collidepoint(mouse):
                        dragging_card = card
                        card.selected = True
                        break

            # Mouse up
            if event.type == pygame.MOUSEBUTTONUP and dragging_card:
                c = dragging_card.card
                played = False
                # Attack
                if c.is_attack():
                    for enemy_ui in enemy_uis:
                        if enemy_ui.rect.collidepoint(mouse) and enemy_ui.enemy.is_alive():
                            if player.play_attack(c, enemy_ui.enemy):
                                enemy_ui.flash = 10
                                slash_effects.append(SlashEffect(enemy_ui.rect.centerx, enemy_ui.rect.centery))
                                damage_numbers.append(DamageNumber(enemy_ui.rect.centerx, enemy_ui.rect.y, c.attack))
                                played = True
                                break
                # Block
                elif c.is_block():
                    if player.play_block(c): played = True
                # Heal
                elif c.is_heal():
                    if player.play_heal(c): played = True

                if played and dragging_card in card_uis:
                    card_uis.remove(dragging_card)

                dragging_card.selected = False
                dragging_card = None

        pygame.display.update()
        clock.tick(60)