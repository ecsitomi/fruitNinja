import pygame
import random

#állandó értékek
WIDTH=1280
HEIGHT=620
BG_COLOR=(255,255,255)
FONT_COLOR=(27,131,142)
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
        
        #UGRÁS ELEMEI
        self.on_ground=True
        self.gravity=1
        self.jump_speed=-15
        self.dy=0

    def ninja_input(self):
        keys=pygame.key.get_pressed() #ninja mozgása

        if keys[pygame.K_LCTRL]: #támadás
            self.attack_mode=True
            self.attack_animation()
        else:
            self.attack_mode=False #ha nincs space nincs attack mód

        if keys[pygame.K_SPACE] and self.on_ground: #space ugrik ha a földön van
            self.jump() #lásd lentebb ugrás fizika

        if keys[pygame.K_RIGHT] and self.rect.right<WIDTH: #jobbra
            self.x_movement(self.ninja_speed)
            self.ninja_forward=True
        if keys[pygame.K_LEFT] and self.rect.left>0: #ballra
            self.x_movement(-self.ninja_speed)
            self.ninja_forward=False

        ''' nem szükséges a fel-le mozgás
        if keys[pygame.K_UP] and self.rect.bottom>HEIGHT-150: #fel
            self.y_movement(-self.ninja_speed)
            self.on_ground=True
        if keys[pygame.K_DOWN] and HEIGHT-100>self.rect.bottom: #le
            self.y_movement(self.ninja_speed)
            self.on_ground=True
        '''

        if not any(keys): #ha nincs lenyomott billentyű
            if self.ninja_forward: #álló helyzetben milyen kép legyen
                self.image=self.image_original #álló kép jobbra néz
            else:
                self.image=self.image_flipped #állókép balra néz
            rect_center=self.rect.center #lekérjük a rect adatait, mert álva kisebb
            self.rect=self.image.get_rect(center=rect_center) #és felülírjuk a mozgós rect adatokat, mert így kisebb

    #UGRÁS
    def jump(self):
        self.on_ground=False #nem vagyunk a földön
        self.dy=self.jump_speed  #minusszal kezd, a hozzáadás miatt átmegy pluszba, mint egy görbe
        
    def apply_gravity(self): #ugrásban a süllyedés
        self.dy+=self.gravity
        self.rect.y+=self.dy  #gravitáció a négyzeten... majdnem (mindig ad hozzá)

    def y_movement_collision(self): #ugrás utáni érkezés a platformra
        for pf_rect in platform_rects: #azért for mert több platform van
            if self.rect.colliderect(pf_rect):  # Ütközés vizsgálata a platformmal
                self.rect.bottom = pf_rect.top  # A ninja alja az elfogadható tartomány alsó határánál helyezkedik el
                self.dy = 0  # Zuhanás sebessége nulla
                self.on_ground = True  # Földön vagyunk

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
            self.ninja_index+=0.095
        else:
            self.ninja_index=0
        self.image=self.ninja_attack[int(self.ninja_index)]

    def y_movement(self,dy): #dy az a self.ninja_speed
        self.rect.y+=dy #vertikális mozgás

    def update(self):
        self.ninja_input() #objektumon belül történik az elem frissítése
        self.apply_gravity() #ugrás utáni zuhanás sebesség
        self.y_movement_collision() #hova érjen vissza

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

def collision_sprite(): #ütközések vizsgálata
    if ninja.sprite.attack_mode:
        if pygame.sprite.spritecollide(ninja.sprite, fruit_group, True):
            return True
    return False

def display_score(): #pontok megjelenítése
    score_surf=game_font.render('Score: '+str(score),True,FONT_COLOR) #hogyan
    score_rect=score_surf.get_rect(topleft=(WIDTH-200,10)) #hol
    screen.blit(score_surf,score_rect) #tadáám

pygame.init() #inicializálja magát a pygame
screen=pygame.display.set_mode((WIDTH,HEIGHT)) #meghatározza az ablakot
pygame.display.set_caption('Fruit Ninja') #főcím
clock=pygame.time.Clock() #időzítő

platform_surf=pygame.image.load('img/platform.png').convert_alpha() #platform képe
platform_rects=[platform_surf.get_rect(midtop=(WIDTH/2,HEIGHT-160)),
                platform_surf.get_rect(midtop=(WIDTH+250,HEIGHT-200)),
                platform_surf.get_rect(midtop=(-250,HEIGHT-230))] #platform helyei

ninja=pygame.sprite.GroupSingle() #példányosítom a ninját
ninja.add(Ninja())

fruit_group=pygame.sprite.Group() #lehet sima group mert több objektumot tárol egyszerre
fruit_timer=pygame.USEREVENT+1 #gyümölcsökhöz időzítő
fruit_sec=1000 #időzítőhöz idő - 1 ms
pygame.time.set_timer(fruit_timer,fruit_sec) #maga az időzítő elindul

score=0 #számolja a pontjainkat
game_font=pygame.font.SysFont('arial',30,bold=True) #betűtípus

running=True #futás
while running:
    for event in pygame.event.get(): #események
        if event.type==pygame.QUIT: #kilépés
            running=False
        if event.type==fruit_timer:
           fruit_group.add(Fruit(random.choice(['pear','banana','strawberry']))) 


    screen.fill(BG_COLOR) #háttérszín
    for platform_rect in platform_rects:
        screen.blit(platform_surf,platform_rect) #platform megjeleítése

    ninja.draw(screen) #ninja megjelenítése
    ninja.update() #frissítése
    pygame.draw.rect(screen,'gray',ninja.sprite.rect,2) #kirajzolja a ninja rect vonalát

    fruit_group.draw(screen) #gyümölcsök megjelenítése
    fruit_group.update() #frissítése

    if collision_sprite(): #ütközés
        score+=1
    display_score()

    pygame.display.update() #frissítés
    clock.tick(FPS) #másodpercenként mennyi kép

pygame.quit()