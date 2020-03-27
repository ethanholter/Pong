import pygame
import random
import math
from time import sleep

DISP_WIDTH = 1000
DISP_HEIGHT = 500
BACKGROUND = (10, 10, 30)

pygame.init()
pygame.display.set_caption("Pong")
root = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
root.fill(BACKGROUND)
done = False
font = pygame.font.Font('freesansbold.ttf', 300)
clock = pygame.time.Clock()

def map(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

class Scorekeeper:
    def __init__(self):
        self.scores = [0, 0]

    def reset(self):
        self.scores = [0, 0]

    def addPoint(self, player, points):
        self.scores[player - 1] += points

    def display(self):
        text = font.render("{}    {}".format(self.scores[0], self.scores[1]), True, (20, 50, 55))
        root.blit(text,(DISP_WIDTH//2 - text.get_width() // 2, DISP_HEIGHT//2 - text.get_height() // 2))

class Player:
    def __init__(self, player):
        self.MARGIN = 20
        self.COLOR = (255, 255, 255)
        self.SIZE = 150
        self.WIDTH = 10
        self.SPEED = 8
        self.BUFFER = 10
        self.playerNum = player
        self.location = DISP_HEIGHT/2 - self.SIZE/2

    def reset(self):
        self.location = DISP_HEIGHT/2 - self.SIZE/2

    def update(self):
        if self.playerNum == 1:
            pygame.draw.rect(root, self.COLOR, pygame.Rect(self.MARGIN, round(self.location), self.WIDTH, self.SIZE))
        else:
            pygame.draw.rect(root, self.COLOR, pygame.Rect(DISP_WIDTH - self.MARGIN - self.WIDTH, round(self.location), self.WIDTH, self.SIZE))

    def move(self, direction):
        if direction == "up" and self.location > self.BUFFER:
            self.location -= self.SPEED
        elif direction == "down" and self.location + self.SIZE <= DISP_HEIGHT - self.BUFFER:
            self.location += self.SPEED

class AI:
    def __init__(self, player):
        self.MARGIN = 20
        self.COLOR = (255, 255, 255)
        self.SIZE = 150
        self.WIDTH = 10
        self.SPEED = 8
        self.BUFFER = 10
        self.playerNum = player
        self.location = DISP_HEIGHT/2 - self.SIZE/2

    def reset(self):
        self.location = DISP_HEIGHT/2 - self.SIZE/2

    def update(self):
        if self.playerNum == 1:
            pygame.draw.rect(root, self.COLOR, pygame.Rect(self.MARGIN, round(self.location), self.WIDTH, self.SIZE))
        if ball.location[0] <= DISP_WIDTH/2:
            if ball.location[1] + 20 < self.location + self.SIZE/2:
                self.move('up')
            elif ball.location[1] - 20> self.location + self.SIZE/2:
                self.move('down')

    def move(self, direction):
        if direction == "up" and self.location > self.BUFFER:
            self.location -= self.SPEED
        elif direction == "down" and self.location + self.SIZE <= DISP_HEIGHT - self.BUFFER:
            self.location += self.SPEED

class Ball:
    def __init__(self):
        self.COLOR = (255, 255, 255)
        self.SIZE = 8
        self.ACCELERATION = .8
        self.MAXANGLE = .4 * math.pi
        self.speed = 4
        self.location = [DISP_WIDTH/2, DISP_HEIGHT/2]
        self.angle = random.randint(0, 1)*math.pi
        self.angle += map(random.random(), 0, 1, -0.5, 0.5)

    def reset(self):
        self.speed = 4
        self.location = [DISP_WIDTH/2, DISP_HEIGHT/2]
        self.angle = random.randint(0, 1)*math.pi
        self.angle += map(random.random(), 0, 1, -0.5, 0.5)

    def update(self):
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]

        #move ball
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]

        #bounce off walls
        if self.location[1] + self.SIZE > DISP_HEIGHT:
            self.angle *= -1
            self.location[1] -= 2
        if self.location[1] - self.SIZE < 0:
            self.angle *= -1
            self.location[1] += 2

        #bounce off left paddle
        if self.location[0] < player1.MARGIN + player1.WIDTH + self.SIZE and self.location[0] > player1.MARGIN + self.SIZE - self.speed:
            if self.location[1] + self.SIZE > player1.location and self.location[1] - self.SIZE < player1.location + player1.SIZE:
                #prevents ball from getting stuck if saved at the last second and flips velocity
                ball.location[0] = player1.MARGIN + player1.WIDTH + self.SIZE
                self.speed += self.ACCELERATION
                self.angle = map(self.location[1], player1.location, player1.location + player1.SIZE, -self.MAXANGLE, self.MAXANGLE)

        #bounce off right paddle
        if self.location[0] > DISP_WIDTH - player2.MARGIN - player2.WIDTH - self.SIZE and self.location[0] < DISP_WIDTH - player2.MARGIN - self.SIZE + self.speed:
            if self.location[1] + self.SIZE > player2.location and self.location[1] - self.SIZE< player2.location + player2.SIZE:
                ball.location[0] = DISP_WIDTH - player2.MARGIN - player2.WIDTH - self.SIZE
                self.speed += self.ACCELERATION
                self.angle = map(self.location[1], player2.location, player2.location + player2.SIZE, self.MAXANGLE + math.pi, -self.MAXANGLE + math.pi)

        #points system
        if self.location[0] < 0:
            scorekeeper.addPoint(2, 1)
            self.reset()
            player1.reset()
            player2.reset()
            sleep(.5)
        if self.location[0] > DISP_WIDTH:
            scorekeeper.addPoint(1, 1)
            self.reset()
            player1.reset()
            player2.reset()
            sleep(.5)
        #draw ball
        pygame.draw.circle(root, self.COLOR, (round(self.location[0]), round(self.location[1])), self.SIZE)

def newGame():
    root.fill(BACKGROUND)
    text = font.render("RESETING IN:", True, (255, 255, 255))
    root.blit(text,(DISP_WIDTH//2 - text.get_width() // 2, DISP_HEIGHT//2 - text.get_height() // 2))
    pygame.display.flip()
    sleep(1)
    for i in reversed(range(3)):
        root.fill(BACKGROUND)
        text = font.render("%i" % (i+1), True, (255, 255, 255))
        root.blit(text,(DISP_WIDTH//2 - text.get_width() // 2, DISP_HEIGHT//2 - text.get_height() // 2))
        pygame.display.flip()
        sleep(.5)
    root.fill(BACKGROUND)
    ball.reset()
    player1.reset()
    player2.reset()
    pygame.draw.line(root, (155, 155, 155), (DISP_WIDTH//2, 0), (DISP_WIDTH//2, DISP_HEIGHT), 1)
    pygame.display.flip()
    sleep(1)
    scorekeeper.reset()

player1 = AI(1)
player2 = Player(2)
ball = Ball()
scorekeeper = Scorekeeper()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    root.fill(BACKGROUND)
    pygame.draw.line(root, (255, 255, 255), (DISP_WIDTH//2, 0), (DISP_WIDTH//2, DISP_HEIGHT), 1)
    #paddle movement
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: player2.move('up')
    if pressed[pygame.K_DOWN]: player2.move('down')
    if pressed[pygame.K_r]: newGame()

    #update game objects
    scorekeeper.display()
    player1.update()
    player2.update()
    ball.update()
    pygame.display.flip()
    clock.tick(60)

    if scorekeeper.scores[0] == 5:
        font = pygame.font.Font('freesansbold.ttf', 100)
        root.fill((10, 10, 30))
        text = font.render("YOU LOSE", True, (255, 200, 200))
        root.blit(text,(DISP_WIDTH//2 - text.get_width() // 2, DISP_HEIGHT//2 - text.get_height() // 2))
        pygame.display.flip()
        sleep(5)
        done = True
        pygame.QUIT

    if scorekeeper.scores[1] == 5:
        font = pygame.font.Font('freesansbold.ttf', 100)
        root.fill((10, 10, 20))
        text = font.render("YOU WIN", True, (200, 255, 200))
        root.blit(text,(DISP_WIDTH//2 - text.get_width() // 2, DISP_HEIGHT//2 - text.get_height() // 2))
        pygame.display.flip()
        sleep(5)
        done = True
        pygame.QUI
