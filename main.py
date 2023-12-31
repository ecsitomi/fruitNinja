import pygame
#from pygame.sprite import _Group

#állandó értékek
WIDTH=1280
HEIGHT=620
BG_COLOR=(255,255,255)
FPS=60

class Ninja(pygame.sprite.Sprite): #ninja osztály
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('img/Idle__000 1.png').convert_alpha()
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,HEIGHT-100))
        self.speed=5

    def ninja_input(self):
        keys=pygame.key.get_pressed() #ninja mozgása
        if keys[pygame.K_RIGHT]and self.rect.right<WIDTH:
            self.x_movement(self.speed)
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.x_movement(-self.speed)

    def x_movement(self,dx): #dx lesz a self.speed
        self.rect.x+=dx
    
    def update(self):
        self.ninja_input()

pygame.init() #inicializálja magát a pygame
screen=pygame.display.set_mode((WIDTH,HEIGHT)) #meghatározza az ablakot
pygame.display.set_caption('Fruit Ninja') #főcím
clock=pygame.time.Clock() #időzítő

ninja=pygame.sprite.GroupSingle() #példányosítom
ninja.add(Ninja())

running=True #futás
while running:
    for event in pygame.event.get(): #események
        if event.type==pygame.QUIT: #kilépés
            running=False

    screen.fill(BG_COLOR) #háttérszín
    ninja.draw(screen) #ninja megjelenítése
    ninja.update()

    pygame.display.update() #frissítés
    clock.tick(FPS)

pygame.quit()