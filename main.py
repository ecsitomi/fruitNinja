import pygame, random

BG_COLOR=(255,255,255)
FONT_COLOR=(255,255,255)
FPS=60

pygame.init()
pygame.mixer.init()

#ÁLLANDÓ ÉRTÉKEK

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Fruit Ninja')
clock=pygame.time.Clock() #időzítő
GAME_TIME=61000 #játékidő
start_time=pygame.time.get_ticks() #visszaszámlálás
game_font=pygame.font.SysFont('arial',30,bold=True) #betűtípus

#háttérkép 
background = pygame.image.load('img/background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background.set_alpha(200) #háttér legyen halványabb

#vágás anime
slash_surf=pygame.image.load('img/slash.png').convert_alpha()
slash_surf=pygame.transform.scale(slash_surf,(WIDTH,HEIGHT))
slash_rect=slash_surf.get_rect(topleft=(0,0))

#hangok
pygame.mixer.set_num_channels(3)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
theme_song = pygame.mixer.Sound('sound/theme.mp3')
slash_sound = pygame.mixer.Sound('sound/slash.mp3')
jump_sound = pygame.mixer.Sound('sound/jump2.mp3')
theme_song.set_volume(0.3)
jump_sound.set_volume(2)
slash_sound.set_volume(2)
channel1.play(theme_song, loops=-1)

#ÁLLANDÓ ÉRTÉKEK VÉGE#

class Ninja(pygame.sprite.Sprite): #játékos
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

        #támadások animálása jobbra
        NINJA_ATTACK_1=pygame.image.load('img/Jump_Attack__002.png').convert_alpha()
        NINJA_ATTACK_2=pygame.image.load('img/Attack__009.png').convert_alpha()
        NINJA_ATTACK_3=pygame.image.load('img/Jump_Attack__007.png').convert_alpha()
        NINJA_ATTACK_4=pygame.image.load('img/Attack__009.png').convert_alpha()
        self.ninja_attack_fw=[NINJA_ATTACK_1,NINJA_ATTACK_2,NINJA_ATTACK_3,NINJA_ATTACK_4]

        #támadás balra
        NINJA_ATTACK_1b=pygame.transform.flip(NINJA_ATTACK_1,True,False)
        NINJA_ATTACK_2b=pygame.transform.flip(NINJA_ATTACK_2,True,False)
        NINJA_ATTACK_3b=pygame.transform.flip(NINJA_ATTACK_3,True,False)
        NINJA_ATTACK_4b=pygame.transform.flip(NINJA_ATTACK_4,True,False)
        self.ninja_attack_bw=[NINJA_ATTACK_1b,NINJA_ATTACK_2b,NINJA_ATTACK_3b,NINJA_ATTACK_4b]

        self.ninja_index=0 
        self.ninja_attack=self.ninja_attack_fw

        #idle
        self.image_original=pygame.image.load('img/Idle__000 1.png').convert_alpha() #jobbra 
        self.image_flipped=pygame.transform.flip(self.image_original,True,False) #balra 
        
        #player surf/rect
        self.image=self.ninja_fw[self.ninja_index] 
        self.rect=self.image.get_rect(midbottom=(WIDTH/2,100))
        
        #RECT MÓDOSÍTÁSOK - sajnos nem működik 
        #self.rect.inflate_ip(-50, 0) #csökkenti a rect szélességét
        #self.rect.width *= 0.7 #csökkenti ez is a rect szélességét
        #self.rect.inflate_ip(-self.rect.width * 0.3, 0)  # Csökkenti a szélességet 30%-kal
        #self.rect = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * 0.5), self.rect.height)

        #mozgás
        self.ninja_speed=12 
        self.ninja_forward=True 
        self.attack_mode=False 
        
        #UGRÁS ELEMEI
        self.on_ground=True
        self.gravity=1
        self.jump_speed=-25
        self.dy=0
        #self.jump_twice=0 #dupla ugrás, sajnos nem működik

    #IRÁNYÍTÁS
    def ninja_input(self):
        keys=pygame.key.get_pressed() 

        if keys[pygame.K_LCTRL] and self.on_ground: #támadás
            self.attack_mode=True
            self.attack_animation()
        else:
            self.attack_mode=False 

        if keys[pygame.K_SPACE] and self.on_ground: #ugrás
            self.jump() 
            channel3.play(jump_sound)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #jobbra
            self.x_movement(self.ninja_speed)
            self.ninja_forward=True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: #balra
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

        if not any(keys): #idle
            if self.ninja_forward: 
                self.image=self.image_original 
            else:
                self.image=self.image_flipped 
            rect_center=self.rect.center 
            self.rect=self.image.get_rect(center=rect_center) #

    def attack_animation(self): #támadás animálása
        if self.ninja_index<len(self.ninja_fw)-1:
            self.ninja_index+=0.1
        else:
            self.ninja_index=0

        if self.ninja_forward: #jobbra 
            self.image=self.ninja_attack_fw[int(self.ninja_index)]
        else: #balra
            self.image = self.ninja_attack_bw[int(self.ninja_index)]

    def jump(self): #ugrás
        self.on_ground=False 
        self.dy=self.jump_speed
        
    def apply_gravity(self): #gravitáció
        self.dy+=self.gravity
        if self.dy>35:
            self.dy=35
        self.rect.y+=self.dy 

    def y_movement_collision(self): #ugrás utáni érkezés a platformra
        for pf_rect in platform_rects: 
            if self.rect.colliderect(pf_rect):
                if self.rect.bottom >= pf_rect.top and self.rect.bottom <= pf_rect.top + abs(self.dy):
                    self.rect.bottom = pf_rect.top  
                    self.dy = 0  
                    self.on_ground = True  
                    
        if self.rect.colliderect(platformSMALL_rect): 
            if self.rect.bottom >= platformSMALL_rect.top and self.rect.bottom <= platformSMALL_rect.top + abs(self.dy):
                self.rect.bottom = platformSMALL_rect.top  
                self.dy = 0  
                self.on_ground = True

    #horizontális mozgás
    def x_movement(self,dx): 
        self.rect.x+=dx 
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

    def y_movement(self,dy): #vertikális mozgás
        self.rect.y+=dy 

    def hopp(self): #végtelen képernyős mozgás
        if self.rect.top > HEIGHT+50:
            self.rect.bottom = -50
        if self.rect.right < -50:
            self.rect.left = WIDTH+50
        if self.rect.left > WIDTH+50:
            self.rect.right = -50

    def update(self):
        self.ninja_input()
        self.apply_gravity() 
        self.y_movement_collision()
        self.hopp()

class Fruit(pygame.sprite.Sprite):
    def __init__(self, fruit_type): #fruit_type: körte, banán, eper
        super().__init__()

        self.fruit_speed=random.randint(5,8) #gyümölcs sebessége

        if fruit_type=='pear': #körte
            self.image=pygame.image.load('img/pear.png').convert_alpha() 
        elif fruit_type=='banana': #banán
            self.image=pygame.image.load('img/banana.png').convert_alpha() 
        else: #eper
            self.image=pygame.image.load('img/strawberry.png').convert_alpha() 

        self.rect=self.image.get_rect(center=(random.randint(20,WIDTH-20),-20)) #kiindulási hely

    def fruit_movement(self,dy): #gyümölcs mozgása
        self.rect.y+=dy

    def destroy(self): #törlés
        if self.rect.top>HEIGHT:
            self.kill() 

    def update(self): 
        self.fruit_movement(self.fruit_speed) 
        self.destroy()

def collision_sprite(): #ütközések 
    if ninja.sprite.attack_mode: 
        if pygame.sprite.spritecollide(ninja.sprite, fruit_group, True): #és ha találkozik egy gyümölcsel
            slash_anime(slash_surf,slash_rect)
            channel2.play(slash_sound)
            return True
    return False

def slash_anime(slash_surf,slash_rect): #vágás animálása
    screen.blit(slash_surf,slash_rect) 
    #slash_surf = pygame.transform.rotozoom(slash_surf, 90, 1) #forgatás - sajnos nem működik
    
def display_score(): #pontok megjelenítése
    score_surf=game_font.render('Score: '+str(score),True,FONT_COLOR) 
    score_rect=score_surf.get_rect(center=(WIDTH/2,100)) 
    screen.blit(score_surf,score_rect)

def display_time(time_left): #visszaszámlálás
    time_left_surf=game_font.render("Time left: " + str(time_left), False, FONT_COLOR)
    time_left_rect=time_left_surf.get_rect(center=(WIDTH//2,50))
    screen.blit(time_left_surf,time_left_rect)

def endgame(): #záróképernyő
    global high_score, score, new_high_score
    if score <= high_score:
        score_surf=game_font.render('Your score: '+str(score),True,FONT_COLOR) 
        score_rect=score_surf.get_rect(center=(WIDTH/2,HEIGHT/2-50)) 
        screen.blit(score_surf,score_rect) 

        high_score_surf=game_font.render('The high score: '+str(high_score),True,FONT_COLOR) 
        high_score_rect=high_score_surf.get_rect(center=(WIDTH/2,HEIGHT/2+50)) 
        screen.blit(high_score_surf,high_score_rect) 

    if score>high_score:
        score_surf=game_font.render('Your new high score: '+str(score),True,FONT_COLOR)
        score_rect=score_surf.get_rect(center=(WIDTH/2,HEIGHT/2-50))
        screen.blit(score_surf,score_rect)

        new_high_score = score

    enter_surf=game_font.render('Press ENTER to restart!',True,FONT_COLOR) 
    enter_rect=enter_surf.get_rect(center=(WIDTH/2,HEIGHT-50)) 
    screen.blit(enter_surf,enter_rect)

def restart(): #újraindítás
    global time_left, score, start_time, fruit_group, high_score, new_high_score
    if score>high_score:
        high_score=new_high_score
    start_time=pygame.time.get_ticks()
    time_left=61
    score=0
    ninja.sprite.kill()
    ninja.add(Ninja())
    fruit_group.empty()

#PLATFORMOK
platformSMALL_surf=pygame.image.load('img/platform_small.png').convert_alpha() 
platformSMALL_rect=platformSMALL_surf.get_rect(midtop=(WIDTH/2,HEIGHT/4*2))

platform_surf=pygame.image.load('img/platform.png').convert_alpha() #platform képe
platform_rects=[#platform_surf.get_rect(midtop=(WIDTH/2,HEIGHT/4*2)), #felső #kivettem mert a SMALL jobb
                platform_surf.get_rect(midtop=(WIDTH/2,HEIGHT-100)), #alsó
                platform_surf.get_rect(midtop=(WIDTH+100,HEIGHT/3*2)), #jobb
                platform_surf.get_rect(midtop=(-100,HEIGHT/3*2))] #bal

#Játékos
ninja=pygame.sprite.GroupSingle() 
ninja.add(Ninja())

#Gyümölcsök
fruit_group=pygame.sprite.Group() 
fruit_timer=pygame.USEREVENT+1 #időzítő a sima gyümölcshöz
fruit_sec=1000 #1sec
pygame.time.set_timer(fruit_timer,fruit_sec)

fruit_timer2=pygame.USEREVENT+2 #időzítő a sok gyümölcshöz
fruit_sec2=17000 #17sec
pygame.time.set_timer(fruit_timer2,fruit_sec2) 

#Pontok
score=0 
high_score=0 
new_high_score=0
time_left=61 #csak az induláshoz kell egy 0nál nagyobb érték

def start():
    screen.fill(BG_COLOR) #háttérszín
    screen.blit(background, (0, 0))

    start_surf=game_font.render('FRUIT NINJA',True,FONT_COLOR) #hogyan
    start_rect=start_surf.get_rect(center=(WIDTH/2,HEIGHT/2)) #hol
    screen.blit(start_surf,start_rect) #tadáám

    start2_surf=game_font.render(f'wasd / arrows + space + ctrl',True,FONT_COLOR) #hogyan
    start2_rect=start2_surf.get_rect(center=(WIDTH/2,HEIGHT/2+100)) #hol
    screen.blit(start2_surf,start2_rect) #tadáám

    start3_surf=game_font.render('Press ENTER to start!',True,FONT_COLOR) #hogyan
    start3_rect=start3_surf.get_rect(center=(WIDTH/2,HEIGHT-100)) #hol
    screen.blit(start3_surf,start3_rect) #tadáám

running=True #game loop
go=False #kezdőképernyő
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get(): #eseménykezelő
        if event.type==pygame.QUIT: 
            running=False
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_ESCAPE:  
                running = False
        if event.type==fruit_timer: #gyümölcs időzítő 1
           fruit_group.add(Fruit(random.choice(['pear','banana','strawberry']))) 
        if event.type==fruit_timer2: #gyümölcs időzítő 2
            for i in range(7):
                fruit_group.add(Fruit(random.choice(['pear','banana','strawberry']))) 

    if not go: #kezdőképernyő
        start()
        if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
            restart()
            go=True

    if go: #a játék
        screen.fill(BG_COLOR) 
        screen.blit(background, (0, 0)) #háttér
        if time_left>0:
            for platform_rect in platform_rects: #platformok
                screen.blit(platform_surf,platform_rect) 
            screen.blit(platformSMALL_surf,platformSMALL_rect)

            ninja.draw(screen) #ninja 
            ninja.update() 
        
        #ninja hitbox fejlesztéshez
        #pygame.draw.rect(screen,'gray',ninja.sprite.rect,2) #kirajzolja a ninja rect vonalát

            fruit_group.draw(screen) #gyümölcsök 
            fruit_group.update()

            if collision_sprite(): #ütközés ellenőrzés
                score+=1

            display_score() #pontok
            display_time(time_left) #visszaszámlálás

        time_left=int((start_time+GAME_TIME-pygame.time.get_ticks()))//1000 #visszaszámlálás - a max játékidőbl kivonja az eddig elteltet
        if time_left<=0:
            endgame() #záróképernyő
            if keys[pygame.K_RETURN]:  # Billentyű lenyomás esemény # Ha az Enter-t nyomják meg
                restart() #újraindítás

    pygame.display.update() #képernyő frissítés
    clock.tick(FPS) #másodpercenként mennyi kép

pygame.quit() #bye bye

#Készítette: ecsitomi
#HEJ 2025.
