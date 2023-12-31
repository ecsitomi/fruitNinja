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

        #jobbra mozgás animálása
        NINJA_FW_1=pygame.image.load('img/Run__001.png').convert_alpha()
        NINJA_FW_2=pygame.image.load('img/Run__002.png').convert_alpha()
        NINJA_FW_3=pygame.image.load('img/Run__005.png').convert_alpha()
        self.ninja_fw=[NINJA_FW_1,NINJA_FW_2,NINJA_FW_3]

        #balra mozgás animálása
        NINJA_BW_1=pygame.image.load('img/Run__001_b.png').convert_alpha()
        NINJA_BW_2=pygame.image.load('img/Run__002_b.png').convert_alpha()
        NINJA_BW_3=pygame.image.load('img/Run__005_b.png').convert_alpha()
        self.ninja_bw=[NINJA_BW_1,NINJA_BW_2,NINJA_BW_3]

        self.ninja_index=0 #melyik kép a listából
        self.ninja_forward=True #melyik irányba megy
        self.image=self.ninja_fw[self.ninja_index] #maga az adott kép

        self.image_original=pygame.image.load('img/Idle__000 1.png').convert_alpha() #jobbra néz
        self.image_flipped=pygame.transform.flip(self.image_original,True,False) #horizontálisan tükrözött kép
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,HEIGHT-100)) #képernyő aljára lett rakva
        self.speed=5 #mozgási sebesség

    def ninja_input(self):
        keys=pygame.key.get_pressed() #ninja mozgása

        if keys[pygame.K_RIGHT]and self.rect.right<WIDTH:
            self.x_movement(self.speed)
            self.ninja_forward=True
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.x_movement(-self.speed)
            self.ninja_forward=False

        if keys[pygame.K_UP] and self.rect.bottom>HEIGHT-140: #fel
            self.y_movement(-self.speed)
        if keys[pygame.K_DOWN] and HEIGHT-60>self.rect.bottom: #le
            self.y_movement(self.speed)

        if not any(keys): #ha nincs lenyomott billentyű
            if self.ninja_forward: #álló helyzetben milyen kép legyen
                self.image=self.image_original
            else:
                self.image=self.image_flipped

    def x_movement(self,dx): #dx lesz a self.speed
        self.rect.x+=dx #horizontális mozgás
        self.x_movement_animation()

    def x_movement_animation(self): #mozgás animáció indexe
        if self.ninja_index<len(self.ninja_fw)-1:
            self.ninja_index+=0.2
        else:
            self.ninja_index=0

        if self.ninja_forward: #true
            self.image=self.ninja_fw[int(self.ninja_index)] #azért int hogy egész szám legyen
        else:
            self.image=self.ninja_bw[int(self.ninja_index)] #ez a balra mozgás

    def y_movement(self,dy): #dy az a self.speed
        self.rect.y+=dy #vertikális mozgás

    def update(self):
        self.ninja_input() #objektumon belül történik az elem frissítése

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