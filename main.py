import pygame
import random
import math
from pygame import mixer

# screen initialization
pygame.init()

# set window dimensions
screen = pygame.display.set_mode((800, 600))

# set Title
pygame.display.set_caption("Space Invader")

# set Logo
logo = pygame.image.load('planet.png')
pygame.display.set_icon(logo)

# loading
playerImg = pygame.image.load('spaceship.png')
backgroundImg = pygame.image.load('background.png')
bulletImg = pygame.image.load('bullet.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

# initial player coordinates
playerX = 370
playerY = 480
playerX_change = 0

# enemy coordinates
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

numberOfEnemies = 6

for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(4)
    enemyY_change.append(40)

score = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX=600
scoreY=15
gameoverfont = pygame.font.Font('freesansbold.ttf',64)

# bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def Score(x,y):
    value = font.render("Score : " + str(score), True, (255,0,0))
    screen.blit(value,(x,y))

def show_gameover():
    value = font.render("** GAME OVER ** ", True, (0,255,255))
    screen.blit(value,(280,250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y ,i):
    screen.blit(enemyImg[i], (x, y))
    # screen.blit(bulletImg, (500, 300))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(y2 - y1, 2)) + (math.pow(x2 - x1, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while (running):

    # background Screen Colour
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking KeyStroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    #Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # updating player
    playerX += playerX_change

    # setting boundries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(numberOfEnemies):
        if enemyY[i] >440:
            for j in range(numberOfEnemies):
                enemyY[j]=2000
            show_gameover()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            mixer.Sound('explosion.wav').play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)
            print(score)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # displaying player
    player(playerX, playerY)

    Score(scoreX,scoreY)
    # updating screen
    pygame.display.update()
