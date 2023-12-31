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
        self.image_original=pygame.image.load('img/Idle__000 1.png').convert_alpha() #jobbra néz
        self.image=self.image_original
        self.image_flipped=pygame.transform.flip(self.image,True,False) #horizontálisan tükrözött kép
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,HEIGHT-100)) #képernyő aljára lett rakva
        self.speed=5 #mozgási sebesség
        self.direction="right"

    def ninja_input(self):
        keys=pygame.key.get_pressed() #ninja mozgása
        if keys[pygame.K_RIGHT]and self.rect.right<WIDTH:
            self.x_movement(self.speed)
            self.direction="right" #jobbra mozog
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.x_movement(-self.speed)
            self.direction="left" #balra mozog
        if keys[pygame.K_UP] and self.rect.bottom>HEIGHT-140:
            self.y_movement(-self.speed)
        if keys[pygame.K_DOWN] and HEIGHT-60>self.rect.bottom:
            self.y_movement(self.speed)

    def x_movement(self,dx): #dx lesz a self.speed
        self.rect.x+=dx #horizontális mozgás

    def y_movement(self,dy): #dy az a self.speed
        self.rect.y+=dy #vertikális mozgás

    def update(self):
        self.ninja_input() #objektumon belül történik az elem frissítése

        if self.direction=="left": #amilyen irányba megy, arra néz a képe
            self.image=self.image_flipped
        if self.direction=="right":
            self.image=self.image_original

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