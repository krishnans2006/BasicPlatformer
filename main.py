import os
import random

import pygame
from pygame.locals import *

pygame.init()

W, H = 800, 447
window = pygame.display.set_mode((W, H))
pygame.display.set_caption("Basic Platformer")

bg = pygame.image.load(os.path.join("images", "bg.png")).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

STARTSPEED = 5

class Player(object):
    run = [pygame.image.load(os.path.join("images", str(x) + ".png")) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join("images", str(x) + ".png")) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join("images", "S1.png")), pygame.image.load(os.path.join("images", "S2.png")),
             pygame.image.load(os.path.join("images", "S2.png")), pygame.image.load(os.path.join("images", "S2.png")),
             pygame.image.load(os.path.join("images", "S2.png")), pygame.image.load(os.path.join("images", "S2.png")),
             pygame.image.load(os.path.join("images", "S2.png")), pygame.image.load(os.path.join("images", "S2.png")),
             pygame.image.load(os.path.join("images", "S3.png")), pygame.image.load(os.path.join("images", "S4.png")),
             pygame.image.load(os.path.join("images", "S5.png"))]
    fall = pygame.image.load(os.path.join("images", "0.png"))
    jumpList = [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5,
                5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2,
                -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4,
                -4, -4, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False
        self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (200, 360))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 15:
                self.y += 1
                self.hitbox = (self.x, self.y + 3, self.width - 32, self.height - 20)
            elif self.slideCount == 80:
                self.y -= 14
                self.sliding = False
                self.slideUp = True
            elif 15 < self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
            if self.slideCount >= 85:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class Saw(object):
    images = [pygame.image.load(os.path.join("images", "SAW0.png")),
              pygame.image.load(os.path.join("images", "SAW1.png")),
              pygame.image.load(os.path.join("images", "SAW2.png")),
              pygame.image.load(os.path.join("images", "SAW3.png"))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.imagecount = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height - 5)
        self.imagecount += 1
        if self.imagecount >= 8:
            self.imagecount = 0
        win.blit(pygame.transform.scale(self.images[self.imagecount // 2], (64, 64)), (self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if (rect[0] + rect[2] > self.hitbox[0]) and (rect[0] < self.hitbox[0] + self.hitbox[2]):
            if (rect[1] + rect[3] > self.hitbox[1]) and (rect[1] < self.hitbox[1] + self.hitbox[3]):
                return True
        return False


class Spike(Saw):
    image = pygame.image.load(os.path.join("images", "spike.png"))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y, 30, 340)
        win.blit(pygame.transform.scale(self.image, (40, 350)), (self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if (rect[0] + rect[2] > self.hitbox[0]) and (rect[0] < self.hitbox[0] + self.hitbox[2]):
            if rect[1] < self.hitbox[3]:
                return True
        return False


def updatefile():
    try:
        with open("highscore.txt", "r") as file:
            highscore = int(file.readlines()[0])
    except (FileNotFoundError, ValueError):
        with open("highscore.txt", "w") as file:
            file.write("0")
            highscore = 0

    if highscore < dispScore:
        with open("highscore.txt", "w") as file:
            file.write(str(dispScore))
            return dispScore

    return highscore


def redrawWindow(win, dispscore):
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    for danger in dangers:
        danger.draw(win)
    runner.draw(win)
    font = pygame.font.SysFont("timesnewroman", 30)
    dispScore = font.render(f"Score: {dispscore}", 1, (255, 255, 255))
    win.blit(dispScore, (win.get_width() - (dispScore.get_width() + 10), 10))
    pygame.display.update()


def endScreen():
    global window, dangers, speed, score, dispScore, runner
    pygame.time.delay(1000)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        window.blit(bg, (0, 0))
        font = pygame.font.SysFont("timesnewroman", 80, bold=True)
        highScore = font.render(f"High Score: {updatefile()}", 1, (0, 0, 0))
        window.blit(highScore, (W/2 - highScore.get_width()/2, 100))
        displayScore = font.render(f"Score: {dispScore}", 1, (255, 255, 255))
        window.blit(displayScore, (W/2 - displayScore.get_width()/2, 250))
        font2 = pygame.font.SysFont("timesnewroman", 40, bold=True)
        playAgain = font2.render("Click to play again!", 1, (0, 0, 0))
        window.blit(playAgain, (W/2 - playAgain.get_width()/2, 350))
        pygame.display.update()
        clock.tick(30)
    dangers = []
    speed = STARTSPEED
    score = 0.0
    dispScore = 0
    runner = Player(200, 335, 64, 64)


runner = Player(200, 335, 64, 64)
dangers = []
pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT - 1, random.randrange(4000, 5000))
run = True
speed = STARTSPEED
score = 0.0
dispScore = 0
while run:
    if not runner.falling:
        bgX -= speed
        bgX2 -= speed
        for danger in dangers:
            danger.x -= speed
            if danger.collide(runner.hitbox):
                runner.falling = True
            if danger.x < danger.width * -1:
                dangers.pop(dangers.index(danger))
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT + 1 and speed < 15:
            speed = round(speed + 0.02, 2)
            score += 0.5
        if event.type == USEREVENT - 1:
            r = random.randrange(0, 2)
            if r == 0:
                dangers.append(Saw(810, 335, 64, 64))
            else:
                dangers.append(Spike(810, 0, 40, 350))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        if not (runner.jumping or runner.sliding or runner.falling):
            runner.jumping = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if not (runner.jumping or runner.sliding or runner.falling):
            runner.sliding = True
    clock.tick(30)
    dispScore = int(score - 0.5) if not score.is_integer() else int(score)
    redrawWindow(window, dispScore)
    if runner.falling:
        endScreen()
