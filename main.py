import pygame
import random
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

        #támadások animálása
        NINJA_ATTACK_1=pygame.image.load('img/Jump_Attack__002.png').convert_alpha()
        NINJA_ATTACK_2=pygame.image.load('img/Jump_Attack__009.png').convert_alpha()
        NINJA_ATTACK_3=pygame.image.load('img/Jump_Attack__007.png').convert_alpha()
        self.ninja_attack=[NINJA_ATTACK_1,NINJA_ATTACK_2,NINJA_ATTACK_3]

        self.ninja_index=0 #melyik kép a listából

        self.image_original=pygame.image.load('img/Idle__000 1.png').convert_alpha() #jobbra néző állókép
        self.image_flipped=pygame.transform.flip(self.image_original,True,False) #balra néző állókép
        
        self.image=self.ninja_fw[self.ninja_index] #maga az adott kép
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,HEIGHT-100)) #képernyő aljára lett rakva

        self.ninja_speed=5 #mozgási sebesség
        self.ninja_forward=True #melyik irányba megy
        self.attack_mode=False #támad-e?

    def ninja_input(self):
        keys=pygame.key.get_pressed() #ninja mozgása

        if keys[pygame.K_SPACE]: #támadás
            self.attack_mode=True
            self.attack_animation()

        if keys[pygame.K_RIGHT] and self.rect.right<WIDTH: #jobbra
            self.x_movement(self.ninja_speed)
            self.ninja_forward=True
        if keys[pygame.K_LEFT] and self.rect.left>0: #ballra
            self.x_movement(-self.ninja_speed)
            self.ninja_forward=False

        if keys[pygame.K_UP] and self.rect.bottom>HEIGHT-140: #fel
            self.y_movement(-self.ninja_speed)
        if keys[pygame.K_DOWN] and HEIGHT-60>self.rect.bottom: #le
            self.y_movement(self.ninja_speed)

        if not any(keys): #ha nincs lenyomott billentyű
            if self.ninja_forward: #álló helyzetben milyen kép legyen
                self.image=self.image_original
            else:
                self.image=self.image_flipped

    def x_movement(self,dx): #dx lesz a self.ninja_speed
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

    def attack_animation(self): #támadás animálásának indexei
        if self.ninja_index<len(self.ninja_fw)-1:
            self.ninja_index+=0.1
        else:
            self.ninja_index=0
        self.image=self.ninja_attack[int(self.ninja_index)]

    def y_movement(self,dy): #dy az a self.ninja_speed
        self.rect.y+=dy #vertikális mozgás

    def update(self):
        self.ninja_input() #objektumon belül történik az elem frissítése

class Fruit(pygame.sprite.Sprite):
    def __init__(self, fruit_type): #fruit type határozza meg mi fog leesni
        super().__init__()

        self.fruit_speed=5

        if fruit_type=='pear': #körte
            self.image=pygame.image.load('img/pear.png').convert_alpha() #körte kép
        elif fruit_type=='banana': #banán
            self.image=pygame.image.load('img/banana.png').convert_alpha() #banán kép
        else: #eper
            self.image=pygame.image.load('img/strawberry.png').convert_alpha() #eper kép

        self.rect=self.image.get_rect(center=(random.randint(20,WIDTH-20),-20)) #honnan induljon le, képernyő fölött kezd, véletlen a horizonton

    def fruit_movement(self,dy): #gyömölcs esésének metódusa
        self.rect.y+=dy

    def destroy(self):
        if self.rect.top>HEIGHT:
            self.kill() #törli magát ha a teteje több mint a képernyő magassága

    def update(self): #gyümölcs magának a frissítése
        self.fruit_movement(self.fruit_speed) #gyümölcs sebességével esik
        self.destroy()


pygame.init() #inicializálja magát a pygame
screen=pygame.display.set_mode((WIDTH,HEIGHT)) #meghatározza az ablakot
pygame.display.set_caption('Fruit Ninja') #főcím
clock=pygame.time.Clock() #időzítő

ninja=pygame.sprite.GroupSingle() #példányosítom a ninját
ninja.add(Ninja())

fruit_group=pygame.sprite.Group() #lehet sima group mert több objektumot tárol egyszerre
fruit_timer=pygame.USEREVENT+1 #gyümölcsökhöz időzítő
fruit_sec=1000 #időzítőhöz idő - 1 ms
pygame.time.set_timer(fruit_timer,fruit_sec) #maga az időzítő elindul

running=True #futás
while running:
    for event in pygame.event.get(): #események
        if event.type==pygame.QUIT: #kilépés
            running=False
        if event.type==fruit_timer:
           fruit_group.add(Fruit(random.choice(['pear','banana','strawberry']))) 


    screen.fill(BG_COLOR) #háttérszín

    ninja.draw(screen) #ninja megjelenítése
    ninja.update() #frissítése

    fruit_group.draw(screen) #gyümölcsök megjelenítése
    fruit_group.update() #frissítése

    pygame.display.update() #frissítés
    clock.tick(FPS) #másodpercenként mennyi kép

pygame.quit()