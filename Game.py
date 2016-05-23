""" Game.py
    by Ibrahim Sardar

    Python 3.3.5
    Pygame 1.9.2a0
"""

#load
import pygame
from   pygame.locals import *

import sys

import time

import random

import Block
from Block import Block

import Player
from Player import Player

import Bullet
from Bullet import Bullet

import Enemy
from Enemy import Enemy
#-END LOAD-#

#init
pygame.init()

#COLORS
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)
GREEN  = (  0, 255,   0)
PINK   = (255, 183, 234)
RED    = (255,   0,   0)
DRED   = (119,  58,  58)
ORANGE = (255, 128,   0)
BLUE   = (  0,   0, 255)
BROWN  = (102,  51,   0)
PURPLE = (102,   0, 102)
YELLOW = (255, 255,   0)
FIRE   = (193, 105,  16)

#window
WINDOWWIDTH   = 720
WINDOWHEIGHT  = 380
WINDOWCENTER  = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Game Example")

#clock
clock = pygame.time.Clock()

#makeAsteroids
def makeAsteroids( speed, counter, group ):
    
    if counter == 0:
        #setting width, height, x-pos, y-pos, velocity(vertical)
        wrnd = random.randint(12, 36)
        hrnd = random.randint(12, 36)
        xrnd = random.randint(wrnd, WINDOWWIDTH-wrnd)
        y    = -hrnd
        vrnd = random.randint(1, 5)
        
        asteroid = Enemy( BLACK, wrnd, hrnd )
        asteroid.setCenterPos( xrnd, y )
        asteroid.moveY( -vrnd )
        group.add( asteroid )
        counter += 1

    elif counter >= speed:
        counter = 0
        
    else:
        counter += 1

    return counter

#endGame
def endGame():
    font = pygame.font.SysFont("aharoni", 152)
    label = font.render("YOU DIED", 1, BLACK)
    
    windowSurface.blit(label, (8, 120) )
    pygame.display.update()
    time.sleep(1.5)

    windowSurface.fill(RED)
    label = font.render("YOU DIED", 1, BLACK)
    windowSurface.blit(label, (8, 120) )
    pygame.display.update()
    time.sleep(1)

    pygame.quit()
    sys.exit()

#showPoints
def showPoints( points ):
    font = pygame.font.SysFont("miriamfixed", 12)
    string = "Points: " + str(points)
    label = font.render(string, 1, BLACK)
    windowSurface.blit(label, (6, 6) )

#updateUnlocked
def updateUnlocked( p ):
    font = pygame.font.SysFont("miriamfixed", 12)

    #update player.unlocked list
    pointMap = [ [0,175,300],
                 [100,400,700],
                 [150,350,900],
                 [200,1000,2500],
                 [250,1500,5000] ]
    w = -1 #track index of weapon
    for weapon in pointMap:
        w += 1
        i = -1 #track index of upgrade
        for upgrade in weapon:
            i += 1
            if p.points >= upgrade:
                if p.unlocked[w] == i:
                    p.unlocked[w] = i+1

    #render & blit labels
    for i in range( len(p.unlocked) ):
        #set text color
        color = BLACK
        if p.unlocked[i] == 0:
            color = RED
        if p.selected == i:
            color = BLUE
        if p.unlocked[i] == 0 and p.selected == i:
            color = DRED
        #--labels--
        #shooter
        if i == 0:
            string = "1: Shooter lvl " + str(p.unlocked[i])
            label = font.render(string, 1, color)
            windowSurface.blit(label, (6, 24+18*i) )
        #missle
        if i == 1:
            string = "2: Missle lvl " + str(p.unlocked[i])
            label = font.render(string, 1, color)
            windowSurface.blit(label, (6, 24+18*i) )
        #sprayer
        if i == 2:
            string = "3: Sprayer lvl " + str(p.unlocked[i])
            label = font.render(string, 1, color)
            windowSurface.blit(label, (6, 24+18*i) )
        #minions
        if i == 3:
            string = "4: Minions lvl " + str(p.unlocked[i])
            label = font.render(string, 1, color)
            windowSurface.blit(label, (6, 24+18*i) )
        #sprayer
        if i == 4:
            string = "5: Bomber lvl " + str(p.unlocked[i])
            label = font.render(string, 1, color)
            windowSurface.blit(label, (6, 24+18*i) )

#main
def main():

    #game fps
    fps = 60

    #sprite group should look like:   [playerBullets][player]
    spriteGroup = pygame.sprite.Group()

    #player(color, width, height),
    # \-> center of player:( WINDOWWIDTH/2, 350 )
    player = Player( BLUE, 16, 16 )
    player.setCenterPos( WINDOWWIDTH/2, 350 )

    #group of all player bullets
    playerBullets = pygame.sprite.Group()

    #group of all falling asteroids
    asteroids = pygame.sprite.Group()

    #the speed in which the number of asteroids increases (speed/fps = # of sec)
    # > 0.6 sec
    speed = 36

    #counts how many times the game loop has looped
    asteroidTimer = 0
    bulletTimer = 0
    
    #game loop
    while(True):
        
        #add asteroid every 1 sec
        asteroidTimer = makeAsteroids( speed, asteroidTimer, asteroids )

        #for press and hold events:
        pressing = pygame.key.get_pressed()
        
        #event handling----------------------------------------------------------------------------------|
        for event in pygame.event.get():

            #quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #keydown
            if event.type == KEYDOWN:

                #=CHEATING=====\
                if event.key == K_UP:
                    player.points += 75
                #==============/
                if event.key == K_RIGHT:
                    player.moveX(4)
                elif event.key == K_LEFT:
                    player.moveX(-4)
                if event.key == K_SPACE:
                    player.shoot( playerBullets, asteroids, fps )
                if event.key == K_1:
                    player.selected = 0
                elif event.key == K_2:
                    player.selected = 1
                elif event.key == K_3:
                    player.selected = 2
                elif event.key == K_4:
                    player.selected = 3
                elif event.key == K_5:
                    player.selected = 4
                        
                    
            #keyup
            elif event.type == KEYUP:
                
                if event.key == K_RIGHT:
                    if player.xspeed > 0: 
                        player.moveX(0)
                if event.key == K_LEFT:
                    if player.xspeed < 0: 
                        player.moveX(0)
                if event.key == K_SPACE:
                    player.stopShooting()

        #timers------------------------------------------------------------------------------------------|
        #...
        
        #collision handling------------------------------------------------------------------------------|
        #if player touches any enemy
        for ast in asteroids:
            if player.rect.colliderect( ast ):
                print("Points:  ", player.points)
                #endGame()!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!testing!!!
        #if bullet touches enemy
        for ast in asteroids:
            for bullet in playerBullets:
                if bullet.rect.colliderect( ast ):
                    player.points += ast.getPoints()
                    ast.kill()
                    bullet.kill()
        
        #update------------------------------------------------------------------------------------------|
        #NOTE: last thing updated will be in "top" layer
        windowSurface.fill(GREY)
        playerBullets.update()
        player.update()
        asteroids.update()
        showPoints( player.points )
        updateUnlocked( player )
        pygame.display.update()

        #fps
        clock.tick(fps)

    #-END GAME LOOP-#
#-END MAIN-#

#if this is file running, run this main
if __name__ == "__main__":
    main()
