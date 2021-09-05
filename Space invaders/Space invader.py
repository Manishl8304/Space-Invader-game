import pygame
import random
import math
from pygame import mixer


pygame.init()


screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('space invaders')
icon = 'C:\\Users\\LG\\Downloads\\launch.png'
pygame.display.set_icon(pygame.image.load(icon))

player = 'C:\\Users\\LG\\Downloads\\spaceship (2).png'
pl = pygame.image.load(player)
playerx =450
playery = 520
playerx_change = 0

enemy = 'C:\\Users\\LG\\Downloads\\enemy.png'
enemy_img = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
enemyx_changef = 2
number_of_enemies = 6

score = 0

for i in range(number_of_enemies):

    enemy_img.append(pygame.image.load(enemy))
    enemyx.append(random.randint(0, 930))
    enemyy.append(random.randint(0, 150))
    enemyx_change.append(enemyx_changef)
    enemyy_change.append(40)


bulletx = playerx
bullety = 520
bulletx_change = 0
bullety_change = -4
bullet_state = "Ready"



pygame.mixer.init()
pygame.mixer.music.load('C:\\Users\\LG\\Downloads\\background.wav')
pygame.mixer.music.play(-1)



def game_over():
    font = pygame.font.Font('freesansbold.ttf', 90)
    gameover = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameover, (200, 200))


def show_score( score):
    textx = 10
    texty = 10
    font = pygame.font.Font('freesansbold.ttf', 30)
    score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score, (textx, texty))


def player(playerx, playery):

    screen.blit(pl, (playerx, playery))


def background():
    backgrounds = 'C:\\Users\\LG\\Downloads\\bg.jpg'
    bl = pygame.image.load(backgrounds)
    screen.blit(bl, (0, 0))


def enemy(enemyx, enemyy):
    screen.blit(enemy_img[i], (enemyx, enemyy))


def bullet(bulletx, bullety):
    bullet = 'C:\\Users\\LG\\Downloads\\bullet.png'
    bl = pygame.image.load(bullet)
    screen.blit(bl, (bulletx, bullety))


def iscollision(bulletx, bullety, enemyx, enemyy):
    distance1 = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance1 < 30:
        return True
    else:
        return False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                playerx_change = -3
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerx_change = 3
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                if bullet_state == "Ready":
                    x = mixer.Sound('C:\\Users\\LG\\Downloads\\laser.wav')
                    x.play()
                    bulletx = playerx
                    bullet_state = "fire"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d :
                playerx_change = 0


    screen.fill((0, 0, 0))
    # background()
    playerx = playerx + playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 930:
        playerx = 930
    for i in range(number_of_enemies):


        if enemyy[i] >= 450:
            for j in range(number_of_enemies):
                enemyy[j] = 4000
            game_over()
        enemyx[i] = enemyx[i] + enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = enemyx_changef
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 930:
            enemyx_change[i] = -enemyx_change[i]
            enemyy[i] += enemyy_change[i]


        collision = iscollision(bulletx, bullety, enemyx[i], enemyy[i])
        if collision:
            explosionSound = mixer.Sound("C:\\Users\\LG\\Downloads\\explosion.wav")
            explosionSound.play()
            bullety = 480
            bullet_state = "Ready"
            score += 1
            enemyx[i] = random.randint(0, 930)
            enemyy[i] = random.randint(0, 150)

        enemy(enemyx[i], enemyy[i])

    if bullet_state == "fire":
            bullety += bullety_change

            bullet(bulletx+16, bullety)
    if bullety <= 0:
            bullet_state = "Ready"
            bullety = 480

    player(playerx, playery)

    show_score(score)
    pygame.display.update()
