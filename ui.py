import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

font = pygame.font.SysFont("arial",50)

class Button:
    def __init__(self,x,y,w,h,text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen,(70,70,70),self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,3)

        txt = font.render(self.text,True,(255,255,255))
        screen.blit(txt,txt.get_rect(center=self.rect.center))

    def clicked(self,pos):
        return self.rect.collidepoint(pos)


def start_screen():

    start_btn = Button(WIDTH/2-150, HEIGHT/2-60, 300,80,"START")
    exit_btn = Button(WIDTH/2-150, HEIGHT/2+60, 300,80,"EXIT")

    while True:

        mouse = pygame.mouse.get_pos()

        screen.fill((30,30,40))

        start_btn.draw()
        exit_btn.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_btn.clicked(mouse):
                    return "start"

                if exit_btn.clicked(mouse):
                    return "exit"

        pygame.display.update()


def start_screen_fullscreen():
    global screen, WIDTH, HEIGHT
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    start_screen()


if __name__ == "__main__":
    start_screen_fullscreen()
