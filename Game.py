""" Game.py
    by Ibrahim Sardar

    Python 3.3.5
    Pygame 1.9.2a0

    Notes:  This game is SUPER MESSY, UNORGANIZED, and LACKING A SOLID GAME ENGINE!
            I intended this game to be at least 100 times simpler than it is now,
            I guess I got a bit carried away. :)
            
            Also note that it is not really complete; it got so messy at one point
            that I just felt like starting a new, fresh project would be much more
            beneficial than putting more brute-force into this chaotic game.

            ** press UP arrow key to cheat **
            
            Anyways, HAVE FUN!
"""

#load
import pygame
from   pygame.locals import *

import sys
import time
import random

from Block import Block
from Player import Player
from Bullet import Bullet
from Enemy import Enemy
from MissileV3 import MissileV3
from Bomb import Bomb
from Minion import Minion
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

#pictures
SHIP_PLAYER = "Graphics/Ship.png"
AST_SMALL   = "Graphics/Asteroid02.png"
AST_MED     = "Graphics/Asteroid01.png"
AST_BIG     = "Graphics/Asteroid03.png"
BG_START    = "Graphic s/Wallpaper01.png"
BG_GAME     = "Graphics/Wallpaper02.png"

#window
WINDOWWIDTH   = 720
WINDOWHEIGHT  = 380
WINDOWCENTER  = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Game Example")
bg_game = pygame.image.load(BG_GAME)

#clock
clock = pygame.time.Clock()

#makeAsteroids
def makeAsteroids( speed, counter, group ):
    
    if counter == 0:
        #   THIS IS ONLY IF NO GRAPHICS ARE USED:
        ###wrnd = random.randint(12, 36)
        ###hrnd = random.randint(12, 36)
        
        #setting asteroid, x-pos, y-pos, velocity(vertical)
        vyrnd = random.randint(1, 4)
        vxrnd = (random.randint(0, 40)/10)-2
        arnd  = random.choice( [AST_SMALL,AST_SMALL,AST_SMALL,AST_MED,AST_MED,AST_BIG] )
        
        asteroid = Enemy( BLACK, 0, 0 )
        asteroid.convertToPic(arnd, 1)
        asteroid.rotate( random.randint(0,359) )
        xrnd = random.randint(asteroid.rect.w, WINDOWWIDTH-asteroid.rect.w)
        y    = -asteroid.rect.h
        
        asteroid.setCenterPos( xrnd, y )
        asteroid.moveY( -vyrnd )
        asteroid.moveX(  vxrnd )
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
def showPoints( player ):
    health = player.health
    points = player.points
    font = pygame.font.SysFont("miriamfixed", 12)

    string = "Health: " + str(health)
    label = font.render(string, 1, BLACK)
    windowSurface.blit(label, (WINDOWWIDTH-82, 6) )
    
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

    #player(color, width, height),
    # \-> center of player:( WINDOWWIDTH/2, 350 )
    player = Player( BLUE, 16, 16 )
    player.convertToPic(SHIP_PLAYER, 1)
    player.setCenterPos( WINDOWWIDTH/2, 350 )

    #group of all player bullets
    playerBullets = pygame.sprite.Group()

    #group of all falling asteroids
    asteroids = pygame.sprite.Group()

    #the speed in which the number of asteroids increases (speed/fps = # of sec)
    # -> 1 sec
    speed = int(fps)

    #counts how many times the game loop has looped
    asteroidTimer = 0
    bulletTimer = 0
    
    #game loop
    while(True):

        #increase difficulty based on score
        if player.points < 200:
            speed = int(fps)
        elif player.points < 500:
            speed = int(fps/2)
        elif player.points < 1000:
            speed = int(fps/4)
        elif player.points < 2500:
            speed = int(fps/6)
        elif player.points < 5000:
            speed = int(fps/10)
        elif player.points < 7500:
            speed = int(fps/20)
        elif player.points < 12500:
            speed = int(fps/30)
        else:
            speed = 1 #LAG mode !!
        
        #add asteroid every <...> sec
        asteroidTimer = makeAsteroids( speed, asteroidTimer, asteroids )
        
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
                ast.kill()
                player.health -= 10
                if player.health <= 0:
                    endGame()
        #if bullet touches enemy
        for ast in asteroids:
            for bullet in playerBullets:
                if bullet.rect.colliderect( ast ):
                    
                    if isinstance(bullet, MissileV3):
                        if bullet.stren == 2:
                            bullet.explodeLarge()
                        else:
                            bullet.explode()

                    if isinstance(bullet, Minion):
                        if bullet.type == 1:
                            bullet.explode()
                            bullet.kill()
                        elif bullet.type == 2:
                            bullet.loseHealth(25, player.pop2) #!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHANGE DAMAGE !!!!!!!!!!!
                        elif bullet.type == 3:
                            bullet.loseHealth(25, player.pop3)

                    if (isinstance(bullet, Bomb)   == False and
                        isinstance(bullet, Minion) == False):
                        bullet.kill()
                    
                    player.points += ast.getPoints()
                    ast.kill()
        
        #update------------------------------------------------------------------------------------------|
        #NOTE: last thing updated will be in "top" layer
        windowSurface.blit(bg_game, (0,0))
        playerBullets.update()
        player.update()
        asteroids.update()
        showPoints( player )
        updateUnlocked( player )
        pygame.display.update()

        #fps
        clock.tick(fps)

    #-END GAME LOOP-#
#-END MAIN-#

#if this is file running, run this main
if __name__ == "__main__":
    main()
