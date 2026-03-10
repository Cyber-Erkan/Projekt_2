import pygame
import sys
import math
from player import Player
from enemy import Enemy

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Card Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)

# -------------------
# BUTTON CLASS
# -------------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (70,70,70), self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# -------------------
# ANIMATION CLASSES
# -------------------
class CardAnimation:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.tx = target_x
        self.ty = target_y
        self.finished = False

    def update(self):
        dx = self.tx - self.x
        dy = self.ty - self.y
        self.x += dx * 0.2
        self.y += dy * 0.2
        if abs(dx) < 5 and abs(dy) < 5:
            self.finished = True

    def draw(self):
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, 40, 60))

class EnemyAttackAnimation:
    def __init__(self, enemy_ui):
        self.enemy_ui = enemy_ui
        self.start_y = enemy_ui.rect.y
        self.x = enemy_ui.rect.x
        self.y = enemy_ui.rect.y
        self.phase = 0
        self.finished = False

    def update(self):
        if self.phase == 0:
            self.y += 12
            if self.y >= self.start_y + 80:
                self.phase = 1
        elif self.phase == 1:
            self.y -= 12
            if self.y <= self.start_y:
                self.phase = 2
                self.finished = True

    def draw(self):
        pygame.draw.rect(screen, (200,50,50), (self.x, self.y, self.enemy_ui.rect.width, self.enemy_ui.rect.height))

class DamageText:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.timer = 60

    def update(self):
        self.y -= 1
        self.timer -= 1

    def draw(self):
        text = font.render(str(self.value), True, (255,80,80))
        screen.blit(text, (self.x, self.y))

# -------------------
# CARD UI
# -------------------
class CardUI:
    WIDTH = 100
    HEIGHT = 150
    def __init__(self, card):
        self.card = card
        self.rect = pygame.Rect(0,0,self.WIDTH,self.HEIGHT)

    def draw(self, hover=False):
        scale = 1.25 if hover else 1
        w = int(self.WIDTH*scale)
        h = int(self.HEIGHT*scale)
        rect = pygame.Rect(self.rect.centerx-w//2, self.rect.centery-h//2, w, h)
        pygame.draw.rect(screen, (230,230,230), rect)
        pygame.draw.rect(screen, (0,0,0), rect, 2)
        y_off = rect.y + 10
        name = font.render(self.card.name, True, (0,0,0))
        screen.blit(name, (rect.x+10, y_off))
        y_off += 30
        if self.card.attack>0:
            screen.blit(font.render(f"ATK: {self.card.attack}", True, (0,0,0)), (rect.x+10, y_off))
            y_off += 25
        if self.card.block>0:
            screen.blit(font.render(f"BLK: {self.card.block}", True, (0,0,0)), (rect.x+10, y_off))
            y_off += 25
        if self.card.heal>0:
            screen.blit(font.render(f"HEAL: {self.card.heal}", True, (0,0,0)), (rect.x+10, y_off))
        cost = font.render(f"COST: {self.card.cost}", True, (0,0,0))
        screen.blit(cost, (rect.x+10, rect.y+rect.height-25))

# -------------------
# ENEMY UI
# -------------------
class EnemyUI:
    WIDTH = 120
    HEIGHT = 120
    def __init__(self, enemy, x, y):
        self.enemy = enemy
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.flash_timer = 0
        self.last_hp = enemy.hp

    def update(self):
        if self.enemy.hp < self.last_hp:
            self.flash_timer = 10
        if self.flash_timer>0:
            self.flash_timer -=1
        self.last_hp = self.enemy.hp

    def draw(self):
        color = (255,80,80) if self.flash_timer>0 else (180,80,80)
        pygame.draw.rect(screen, color, self.rect)
        hp_ratio = max(self.enemy.hp,0)/self.enemy.max_hp
        pygame.draw.rect(screen, (60,60,60), (self.rect.x,self.rect.y-20,120,10))
        pygame.draw.rect(screen, (200,50,50), (self.rect.x,self.rect.y-20,120*hp_ratio,10))

# -------------------
# HAND LAYOUT
# -------------------
def layout_hand(card_uis):
    count = len(card_uis)
    center_x = WIDTH//2
    center_y = HEIGHT-120
    spread = 40
    for i, card_ui in enumerate(card_uis):
        angle = (i-(count-1)/2)*spread
        rad = math.radians(angle)
        x = center_x + math.sin(rad)*400
        y = center_y - math.cos(rad)*80
        card_ui.rect.center = (x, y)

# -------------------
# PLAYER UI
# -------------------
def draw_player_ui(player):
    hp_ratio = max(player.hp,0)/player.max_hp
    pygame.draw.rect(screen,(80,80,80),(40,HEIGHT-200,300,25))
    pygame.draw.rect(screen,(200,50,50),(40,HEIGHT-200,300*hp_ratio,25))
    screen.blit(font.render(f"HP {max(player.hp,0)}/{player.max_hp}",True,(255,255,255)),(40,HEIGHT-230))
    energy_ratio = player.energy/player.max_energy
    pygame.draw.rect(screen,(80,80,80),(40,HEIGHT-160,300,20))
    pygame.draw.rect(screen,(80,200,255),(40,HEIGHT-160,300*energy_ratio,20))
    screen.blit(font.render(f"Energy {player.energy}",True,(255,255,255)),(40,HEIGHT-185))
    block_ratio = min(player.block/player.max_hp,1)
    pygame.draw.rect(screen,(80,80,80),(40,HEIGHT-130,300,20))
    pygame.draw.rect(screen,(120,180,255),(40,HEIGHT-130,300*block_ratio,20))
    screen.blit(font.render(f"Block {player.block}",True,(255,255,255)),(40,HEIGHT-155))

# -------------------
# RUN GAME
# -------------------
def run_pygame_game(player,enemies):
    card_animations = []
    enemy_attacks = []
    damage_texts = []

    if len(player.hand)==0:
        player.draw_hand(5)

    card_uis = [CardUI(c) for c in player.hand]
    enemy_uis = []
    for i,e in enumerate(enemies):
        x = WIDTH//2 + i*200 - 100
        y = HEIGHT//3
        e.ui = EnemyUI(e,x,y)
        enemy_uis.append(e.ui)
        e.next_intent = None
        e.base_attack = e.attack
        e.max_hp = e.hp
        e.choose_intent()

    end_turn_btn = Button(WIDTH-200, HEIGHT-120, 160,60, "End Turn")
    exit_btn = Button(WIDTH-100, 20, 80,40, "Exit")
    retry_btn = Button(WIDTH//2-80, HEIGHT//2+50, 160,50, "Retry")

    selected_card = None
    targeting_enemy = False
    turn_ended = False
    running = True

    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill((30,30,40))

        # EVENTS
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if exit_btn.is_clicked(mouse):
                    pygame.quit(); sys.exit()
                if player.hp<=0 and retry_btn.is_clicked(mouse):
                    player.hp = player.max_hp
                    player.energy = player.max_energy
                    player.block = 0
                    player.hand = []
                    player.deck = player.deck.create_starting_deck()
                    for e in enemies:
                        e.hp = e.max_hp
                        e.attack = e.base_attack
                        e.choose_intent()
                    return
                if end_turn_btn.is_clicked(mouse) and player.hp>0:
                    turn_ended = True

                # CARD CLICK
                if player.hp>0 and not targeting_enemy:
                    for i,cu in enumerate(card_uis):
                        if cu.rect.collidepoint(mouse) and player.energy>=cu.card.cost:
                            card = player.hand[i]
                            if card.attack>0:
                                selected_card = i
                                targeting_enemy = True
                            elif card.block>0:
                                player.block += card.block
                                player.energy -= card.cost
                                player.deck.discard_card(card)
                                player.hand.pop(i)
                                card_uis.pop(i)
                            elif card.heal>0:
                                player.hp = min(player.max_hp, player.hp + card.heal)
                                player.energy -= card.cost
                                player.deck.discard_card(card)
                                player.hand.pop(i)
                                card_uis.pop(i)
                            break
                elif player.hp>0 and targeting_enemy:
                    for eui in enemy_uis:
                        if eui.rect.collidepoint(mouse):
                            card = player.hand[selected_card]
                            e = eui.enemy
                            e.hp -= card.attack
                            damage_texts.append(DamageText(eui.rect.centerx,eui.rect.y,card.attack))
                            card_animations.append(CardAnimation(cu.rect.centerx,cu.rect.centery,eui.rect.centerx,eui.rect.centery))
                            player.energy -= card.cost
                            player.deck.discard_card(card)
                            player.hand.pop(selected_card)
                            card_uis.pop(selected_card)
                            selected_card = None
                            targeting_enemy = False
                            break

        # END TURN
        if turn_ended:
            for e in enemies:
                if e.hp>0:
                    enemy_attacks.append(EnemyAttackAnimation(e.ui))
                    e.act(player)
                    e.choose_intent()
            player.draw_hand(5)
            card_uis = [CardUI(c) for c in player.hand]
            player.block = 0
            player.start_turn()
            turn_ended = False

        # DRAW
        for eui in enemy_uis:
            eui.update()
            eui.draw()
            # Intent
            if hasattr(eui.enemy,'next_intent') and eui.enemy.next_intent:
                action,value = eui.enemy.next_intent
                intent_text = f"ATK {value}" if action=="attack" else f"BUFF {value}"
                screen.blit(font.render(intent_text,True,(255,255,0)), (eui.rect.x, eui.rect.y-50))

        for anim in card_animations:
            anim.update()
            anim.draw()
        card_animations[:] = [a for a in card_animations if not a.finished]
        for atk in enemy_attacks:
            atk.update()
            atk.draw()
        enemy_attacks[:] = [a for a in enemy_attacks if not a.finished]
        for dmg in damage_texts:
            dmg.update()
            dmg.draw()
        damage_texts[:] = [d for d in damage_texts if d.timer>0]

        layout_hand(card_uis)
        for cu in card_uis:
            hover = cu.rect.collidepoint(mouse)
            cu.draw(hover)

        draw_player_ui(player)
        end_turn_btn.draw()
        exit_btn.draw()

        # GAME OVER
        if player.hp<=0:
            overlay = pygame.Surface((WIDTH,HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))
            screen.blit(big_font.render("GAME OVER",True,(255,0,0)),(WIDTH//2-180,HEIGHT//2-100))
            retry_btn.draw()
            exit_btn.draw()

        # VICTORY
        if all(e.hp<=0 for e in enemies):
            overlay = pygame.Surface((WIDTH,HEIGHT))
            overlay.set_alpha(160)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))
            screen.blit(big_font.render("VICTORY!",True,(255,255,0)),(WIDTH//2-150,HEIGHT//2-100))
            next_btn = Button(WIDTH//2-80, HEIGHT//2,160,60,"Next Floor")
            next_btn.draw()

        pygame.display.flip()
        clock.tick(60)