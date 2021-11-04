import pygame
import random
import math

pygame.init()

gameWidth = 800
gameHeight = 600
screen = pygame.display.set_mode((gameWidth,gameHeight))
background = pygame.image.load('stars.png')

#game title and icon
pygame.display.set_caption("Chicken Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#scoring
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(200,250))

#player
playerImage = pygame.image.load('spaceship.png')
playerX = 370
playerY = 550
playerX_change = 0

def player(x,y):
    screen.blit(playerImage, (x,y))

# Regular chicken (enemy)
chickenImage = []
chickenX = []
chickenY = []
chickenX_change = []
chickenY_change = []
default_num_chickens = 6
number_of_chickens = default_num_chickens

speedX = 0.25
speedY = 0.025
for i in range(number_of_chickens):
    chickenImage.append(pygame.image.load('BigChicken.png'))
    chickenX.append(random.randint(50,750))
    chickenY.append(random.randint(50,150))
    chickenX_change.append(speedX)
    chickenY_change.append(speedY)

def chicken(x, y, i):
    screen.blit(chickenImage[i], (x, y))

#shooting mechanics and function
laserImage = pygame.image.load('laser.png')
laserX = 0
laserY = 550
laserY_change = 5
laser_state = "ready"

def shoot(x,y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImage, (x+10,y+10))

#def shoot2(x,y):

def isCollision(chickenX,chickenY,laserX,laserY):
    distance = math.sqrt( (math.pow(chickenX-laserX,2))+(math.pow(chickenY-laserY,2)) )
    if distance < 27:
        return True
    else:
        return False

#leveling system
level = 1
max_level = 15
score_level_scale = 10
percent_scale = 1.15

level_font = pygame.font.Font('freesansbold.ttf',32)

def show_level(x,y):
    score = level_font.render("Level: " + str(level),True, (255,255,255))
    screen.blit(score,(x,y))

#drop system and points
dropImage = pygame.image.load('chicken-leg.png')
dropX = 400
dropY = 0
drop_change = 1.25
rand_test = 0
notDropping = True
def drop(x,y):
    screen.blit(dropImage,(x,y))

#game loop
running = True
while running:
    screen.fill((0, 10, 30)) #RGB background
    screen.blit(background,(0,0)) #background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke checking
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserX = playerX
                    shoot(laserX,laserY)
        if event.type == pygame. KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #boundaries for spaceship
    playerX += playerX_change

    if playerX <= 10:
        playerX = 10
    elif playerX >= 758:
        playerX = 758

    #chicken movement
    for i in range(number_of_chickens):

        #game over
        if isCollision(chickenX[i],chickenY[i],playerX,playerY):
            for j in range(number_of_chickens):
                chickenY[j] = 2000
            game_over_text()
            break

        if chickenY[i] > 600:
            chickenX[i] = random.randint(50, 750)
            chickenY[i] = random.randint(50, 150)

        chickenX[i] += chickenX_change[i]
        chickenY[i] += chickenY_change[i]

        if chickenX[i] <= 10:
            chickenX_change[i] *= -1
        elif chickenX[i] >= 758:
            chickenX_change[i] *= -1

        #collision detection
        collision = isCollision(chickenX[i], chickenY[i], laserX, laserY)
        if collision:
            laserY = 550
            laser_state = "ready"
            score_value += 1
            if notDropping:
                rand_test = random.randint(1,4)
                if rand_test == 1 and notDropping:
                    notDropping = False
                    dropX = chickenX[i]
                    dropY = chickenY[i]
            chickenX[i] = random.randint(50, 750)
            chickenY[i] = random.randint(50, 150)


        chicken(chickenX[i], chickenY[i], i)

    # laser movement
    if laserY <= 0:
        laserY = 550
        laser_state = "ready"
    if laser_state == "fire":
        shoot(laserX, laserY)
        laserY -= laserY_change

    #drop mechanics
    if rand_test == 1:
        drop(dropX, dropY)
        dropY += drop_change
        if isCollision(dropX,dropY,playerX,playerY):
            score_value += 1
            rand_test = 0
            notDropping = True
        elif dropY > 550:
            rand_test = 0
            notDropping = True


    #increase in number of chickens after score
    if score_value >= score_level_scale*level and number_of_chickens == default_num_chickens-1+level and level < max_level:
        chickenImage.append(pygame.image.load('BigChicken.png'))
        chickenX.append(random.randint(50, 750))
        chickenY.append(random.randint(50, 150))
        chickenX_change.append(chickenX_change[0])
        chickenY_change.append(chickenY_change[0])
        chicken(chickenX[number_of_chickens],chickenY[number_of_chickens],number_of_chickens)
        number_of_chickens += 1
        for i in range(number_of_chickens):
            chickenX_change[i] *= percent_scale
            chickenY_change[i] *= percent_scale
        level += 1


    player(playerX,playerY) # player function needed in the while running function
    show_score(textX,textY)
    show_level(gameWidth-200,textY)
    pygame.display.update() #updates screens