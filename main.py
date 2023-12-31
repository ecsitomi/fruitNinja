import pygame
#from pygame.sprite import _Group

#állandó értékek
WIDTH=1280
HEIGHT=620
BG_COLOR=(255,255,255)
FPS=60

class Ninja(pygame.sprite.Sprite): #sprite osztály
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('img/Idle__000 1.png').convert_alpha()
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,HEIGHT-100))

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