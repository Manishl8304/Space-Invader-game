import pygame
import random
import math
import sys
from pygame.locals import *   # after using this no need to use pygame.QUIT simply use QUIT
import time

SCREEWIDTH = 1000
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((1000, 600))
image_s = {}
audio_s = {}


def welcomescreen():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
            maingame()

        else:
            SCREEN.blit(image_s['welcomemessage'], (0, 0))
            textx = 170
            texty = 500
            font = pygame.font.Font('freesansbold.ttf', 30)
            textt = font.render("PRESS SPACE OR UP KEY TO START GAME", True, (255, 255, 255))
            SCREEN.blit(textt, (textx, texty))
            pygame.display.update()


def maingame():
    playerx = (SCREEWIDTH - image_s['SPACESHIP'].get_width()) / 2
    playery = SCREENHEIGHT * 0.9
    playerx_change = 0

    enemy_img = []
    enemyx = []
    enemyy = []
    enemyx_change = []
    enemyy_change = []
    enemyx_changef = 2
    number_of_enemies = 6
    for i in range(number_of_enemies):
        enemy_img.append(image_s['ENEMY'])
        enemyx.append(random.randint(0, 930))
        enemyy.append(random.randint(0, 300))
        enemyx_change.append(enemyx_changef)
        enemyy_change.append(40)

    score = 0

    bulletx = playerx
    bullety = 520
    bullety_change = -4
    bullet_state = "Ready"

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    playerx_change = -3
                elif event.key == K_RIGHT or event.key == K_d:
                    playerx_change = 3
                elif event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    if bullet_state == "Ready":
                        audio_s['LASER'].play()
                        bulletx = playerx
                        bullet_state = "fire"
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d:
                    playerx_change = 0

        SCREEN.fill((0, 0, 0))

        playerx = playerx + playerx_change
        if playerx <= 0:
            playerx = 0
        elif playerx >= 930:
            playerx = 930

        for i in range(number_of_enemies):
            if enemyy[i] + image_s['ENEMY'].get_height() >= playery:
                time.sleep(2)
                for j in range(number_of_enemies):
                    enemyy[j] = 4000
                SCREEN.blit(image_s['gameover'], (0, 0))
                pygame.display.update()
                time.sleep(2)
                return
            enemyx[i] = enemyx[i] + enemyx_change[i]
            # to make game crazier
            if score % 5 == 0 and score != 0:
                for j in range(number_of_enemies):
                    if '-' in str(enemyx_change[i]):
                        enemyx_change[j] = enemyx_change[j] - 0.001
                    else:
                        enemyx_change[j] = enemyx_change[j] + 0.001

            if enemyx[i] <= 0:
                enemyx_change[i] = enemyx_changef
                enemyy[i] += enemyy_change[i]

            elif enemyx[i] >= 930:
                enemyx_change[i] = -enemyx_change[i]
                enemyy[i] += enemyy_change[i]

            collision = iscollision(bulletx, bullety, enemyx[i], enemyy[i])
            if collision:
                audio_s['EXPLOSION'].play()
                bullety = 520
                bullet_state = "Ready"
                score += 1
                enemyx[i] = random.randint(0, 930)
                enemyy[i] = random.randint(0, 150)

            enemy(enemyx[i], enemyy[i])
            player(playerx, playery)

        if bullet_state == "fire":
            bullety += bullety_change
            bullet(bulletx + 16, bullety)

        if bullety <= 0:
            bullet_state = "Ready"
            bullety = 520

        show_score(score)
        pygame.display.update()


def show_score(score):
    textx = 10
    texty = 10
    font = pygame.font.Font('freesansbold.ttf', 30)
    score = font.render("Score : " + str(score), True, (255, 255, 255))
    SCREEN.blit(score, (textx, texty))


def player(playerx, playery):
    SCREEN.blit(image_s['SPACESHIP'], (playerx, playery))


def enemy(enemyx, enemyy):
    SCREEN.blit(image_s['ENEMY'], (enemyx, enemyy))


def bullet(bulletx, bullety):
    SCREEN.blit(image_s['BULLET'], (bulletx, bullety))


def iscollision(bulletx, bullety, enemyx, enemyy):
    distance1 = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance1 < 30:
        return True
    else:
        return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Space invaders')
    pygame.display.set_icon(
        pygame.image.load('image_s\\icon.png'))
    image_s['ENEMY'] = pygame.image.load(
        'image_s\\enemy.png')
    image_s['SPACESHIP'] = pygame.image.load(
        'image_s\\spaceship.png')
    image_s['BULLET'] = pygame.image.load(
        'image_s\\bullet.png')
    image_s['welcomemessage'] = pygame.image.load(
        'image_s\\welcomemessage.png')
    image_s['gameover'] = pygame.image.load(
        'image_s\\gameover.png')
    pygame.mixer.init()
    pygame.mixer.music.load('audio_s\\background.wav')
    pygame.mixer.music.play(-1)
    audio_s['EXPLOSION'] = pygame.mixer.Sound(
        'audio_s\\explosion.wav')
    audio_s['LASER'] = pygame.mixer.Sound(
        'audio_s\\laser.wav')
    while True:
        welcomescreen()
