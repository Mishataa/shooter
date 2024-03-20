
from pygame import *
from time import time as timer
import random
import pygame_menu

init()
mixer.init()

win_width = 700
win_height = 500

Window = display.set_mode((700,500))
display.set_caption("Либиринт")
background = transform.scale(image.load('galaxy.jpg'),(700,500))

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 80)


win = font2.render('You Win', True, (0, 255, 0))
lose = font2.render('You Lose', True, (255, 0, 0))

lost = 0
asters = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        Window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20, 20, 15)
        bulets.add(bullet)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
      

class Asteroid(GameSprite):
    def update(self):
        global asters
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0, win_width - self.rect.width)
            asters = asters + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
     

win_width = 700
win_height = 500

rocket = Player('rocket.png', 80, 100, 10, 100, 80)

bulets = sprite.Group()
asteroids = sprite.Group()
for _ in range(5):
    asteroid = Asteroid('asteroid.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
    asteroids.add(asteroid)

meteorits = sprite.Group()
for _ in range(2):
    meteorit = Asteroid('ufo.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
    meteorits.add(meteorit)

fort = 3
num_fire = 0
rel_fire = False
game = True
finish = False
fire_sound = mixer.Sound('fire.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key  == K_SPACE:
                if num_fire < 3 and rel_fire != True:
                    fire_sound.play()
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 3 and rel_fire != True:
                    rel_fire = True
                    last_time = timer()

                
    if not finish:
        Window.blit(background, (0, 0))
    


        text = font1.render("Пропущено: " + str(asters), 1, (255, 255, 255))
        Window.blit(text, (10,20))
        text_lose = font1.render("Убито: " + str(lost), 1, (255, 255, 255))
        Window.blit(text_lose, (10,55))

        rocket.update()
        rocket.reset()
        bulets.update()
        bulets.draw(Window)
        meteorits.update()
        meteorits.draw(Window)
        fort_text = font1.render(str(fort), True, (0, 255, 0))
        Window.blit(fort_text, (650, 10))
        if rel_fire:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('Перезарядка', True, (100, 200, 100))
                Window.blit(reload, (250, 450))
            else:
                num_fire = 0 
                rel_fire = False
        for asteroid in asteroids:
            asteroid.update()
            asteroid.reset()
        if sprite.spritecollide(rocket, asteroids, False):
            Window.blit(lose, (200, 200))
            finish = True 
        if sprite.groupcollide(bulets, asteroids, True, True):  
            lost += 1
            asteroid = Asteroid('asteroid.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
            asteroids.add(asteroid)
        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            Window.blit(lose, (200, 200))
        if sprite.spritecollide(rocket, meteorits, True):
            fort -= 1
            meteorit = Asteroid('ufo.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
            meteorits.add(meteorit)
            if fort == 0:
                finish = True
                Window.blit(lose, (200, 200))
        if sprite.groupcollide(bulets, meteorits, True, True):
            lost += 1
            meteorit = Asteroid('ufo.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
            meteorits.add(meteorit)

            
        if asters > 9:
            finish = blit
            Window.blit(win, (200, 200))
    else:
        finish = False
        asters = 0
        lost = 0  
        firt = 3 
        fort = 3
        for bb in bulets:
            bb.kill()
        for mm in meteorits:
            mm.kill()
        for aa in asteroids:
            aa.kill()
        time.delay(2000)
        for _ in range(5):
            asteroid = Asteroid('asteroid.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
            asteroids.add(asteroid)
        for _ in range(2):
            meteorit = Asteroid('ufo.png', random.randint(0, win_width - 65), random.randint(-500, -50), random.randint(1, 5), 80, 80)
            meteorits.add(meteorit)



    display.update()
    time.delay(30)