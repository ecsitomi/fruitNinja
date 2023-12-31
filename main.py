import pygame

#állandó értékek
WIDTH=1280
HEIGHT=620
BG_COLOR=(255,255,255)
FPS=60

pygame.init() #inicializálja magát a pygame
screen=pygame.display.set_mode((WIDTH,HEIGHT)) #meghatározza az ablakot
pygame.display.set_caption('Fruit Ninja') #főcím
clock=pygame.time.Clock() #időzítő

running=True #futás
while running:
    for event in pygame.event.get(): #események
        if event.type==pygame.QUIT: #kilépés
            running=False

    screen.fill(BG_COLOR) #háttérszín

    pygame.display.update() #frissítés
    clock.tick(FPS)

pygame.quit()