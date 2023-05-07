import pygame
pygame.init()
pygame.font.init()
import random

window = pygame.display.set_mode((600, 600))
Clock = pygame.time.Clock()

count_lost = 0
count_win = 0

f1 = pygame.font.Font(None, 36)
grass = pygame.transform.scale(pygame.image.load('images/grass.png'), (600,600))

music = pygame.mixer.music.load("sounds/C418 - Door.mp3")
music = pygame.mixer.music.set_volume(0.3)
music = pygame.mixer.music.play(-1)

music_fire = pygame.mixer.music.load("sounds/fair.mp3")
music_fire = pygame.mixer.music.set_volume(0.3)

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, player_image, x, y, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_a] and self.rect.x > 0: # left blue
                self.rect.x -= 3
            if key[pygame.K_d] and self.rect.x < 600 - 65: # right blue
                self.rect.x += 3
                 
    def fire(self):
        bul = Bullet('images/hammer.png', self.rect.centerx, self.rect.top, -3)
        
        bullets.append(bul)
        music_fire = pygame.mixer.music.play(0)
        

class Enemis(GameSprite):

    def update(self):
        global count_lost
        self.rect.y += 1

        if self.rect.y > 560:
            count_lost += 1
            self.rect.y = 0
            self.rect.x = random.randint(10, 550) 
            self.speed = random.uniform(1, 5)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()   


bullets = []
enemis = []
wait = 0

player = Player('images/bow.png', 100, 550, 1)

for i in range(5):
    if wait == 0:
        if True:
            e = Enemis('images/creeper.png', random.randint(10, 550), 0, random.uniform(1, 5))
            enemis.append(e)
    wait = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    
    text1 = f1.render('проїхало типов:' + str(count_lost), 1, (180, 0, 0))
    window.blit(grass, (0, 0))
    window.blit(text1, (10, 50))
        
    for bul in bullets:    
        bul.update()
        bul.reset()
        for e in enemis:
            if pygame.sprite.collide_rect(bul, e):
                bullets.remove(bul)
                count_win += 1
                e.rect.x = random.randint(10, 550)
                e.rect.y = 0
                break

    for e in enemis:
        e.update()
        e.reset()

    player.update() 
    player.reset()

    if count_win >= 20  or  count_lost >= 3:
        text2 = f1.render('проїхало типов: ' + str(count_lost) + ' кильнув: ' + str(count_win), 1, (180, 0, 0))
        window.blit(grass, (0, 0))
        window.blit(text2, (100, 300))

    pygame.display.update()
    Clock.tick(60)