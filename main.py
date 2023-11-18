import time
from typing import Any
from pygame import *
import pygame
from random import randint as rt
import math

Win_height = 500
Win_width = 500

window = display.set_mode((Win_height, Win_height))
display.set_caption('shooter')

backround = transform.scale(image.load('galaxy.jpg'), (Win_height, Win_width))

font.init()
font1 = font.Font(None, 36)

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

score = 0
missed = 0

bonus = False


last_coin_time = pygame.time.get_ticks()
coin_interval = 5000

finish = False
game = True


class GameSprite(sprite.Sprite):
    # amogus
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        super().__init__()

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed

        if keys[K_RIGHT] and self.rect.x < Win_width - 80:
            self.rect.x = self.rect.x + self.speed

    def fire(self):
        if bonus == False:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
        else:
            bullet1 = Bullet('bullet.png', self.rect.centerx - 20, self.rect.top, 15, 20, -15)
            bullet2 = Bullet('bullet.png', self.rect.centerx + 20, self.rect.top, 15, 20, -15)
            bullets.add(bullet1, bullet2)


class Coin(GameSprite):
    def __init__(self, player_image, size_x, size_y, player_speed):
        super().__init__(player_image, rt(80, Win_width - 80), rt(80, Win_height - 80) , size_x, size_y, player_speed)
        self.angle = 0
    def update(self):
        self.angle += 0.05
        self.rect.x = Win_width // 2 + int(200 * math.cos(self.angle))
        self.rect.y = Win_height // 2 + int(200 * math.sin(self.angle))

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > Win_width - self.rect.width:
            self.rect.x = Win_width - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > Win_height - self.rect.height:
            self.rect.y = Win_height - self.rect.height




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > Win_width:
            missed += 1
            self.rect.y = -23
            self.rect.x = rt(60, Win_width-60)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()


ship = Player("rocket.png", 5, Win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
coins = sprite.Group()

for i in range(rt(1, 10)):
    monster = Enemy("ufo.png", rt(80, Win_width-80), -23, 60, 50, rt(1, 5))
    monsters.add(monster)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)

fire_sound = mixer.Sound('fire.ogg')




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    current_time = time.get_ticks()
    if current_time - last_coin_time >= coin_interval:
        coin = Coin("coin.png", 30, 30, 10)
        coins.add(coin)
        last_coin_time = current_time

    if finish == False:
        window.blit(backround, (0, 0))

        text = font1.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text1 = font1.render("Пропущено:" + str(missed), 1, (255, 255, 255))
        window.blit(text1, (10, 40))

        bullets.update()
        bullets.draw(window)

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        coins.update()
        coins.draw(window)



        collision = sprite.groupcollide(monsters, bullets, True, True)
        for e in collision:
            score += 1
            monster = Enemy("ufo.png", rt(80, Win_width - 80), -23, 60, 50, rt(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or (missed > 10):
            finish = True
            window.blit(lose, (200, 200))

        if score > 10:
            finish = True
            window.blit(win, (200, 200))

        collision_coins = sprite.groupcollide(bullets, coins, True, True)
        for e in collision_coins:
            bonus_choice = rt(0, 1)
            if bonus_choice == 0:
                bonus = True
            else:
                ship.speed += 2



    display.update()
    time.delay(60)