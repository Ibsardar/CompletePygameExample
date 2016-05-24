""" Player.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame, math, random, Block, Bullet, FlameV2, Missile
from Block import Block
from Bullet import Bullet
from FlameV2 import FlameV2
from Missile import Missile
pygame.init()
#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)
DGREY  = ( 91,  91,  91)
DDGREY = ( 34,  34,  34)
GREEN  = (  0, 255,   0)
PINK   = (255, 183, 234)
RED    = (255,   0,   0)
ORANGE = (255, 128,   0)
BLUE   = (  0,   0, 255)
BROWN  = (102,  51,   0)
PURPLE = (102,   0, 102)
YELLOW = (255, 255,   0)
FIRE   = (193, 105,  16)
#pictures
BULLET_LGREY = "Graphics/Bullet01.png"
BULLET_GREY  = "Graphics/Bullet02.png"
BULLET_DGREY = "Graphics/Bullet03.png"
MISSLE_BASIC = "Graphics/Missile02.png"
MISSLE_HEAVY = "Graphics/Missile01.png"

#Player
class Player(Block):
    #initializer
    def __init__(self, color=BLACK, w=0, h=0):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(w, h)
        self.color = color
        self.isPic = False

        self.baddies = None
        self.bullets = None

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

        self.event2 = False
        self.event3 = False
        self.timer  = 0
        self.alarm  = 0

        #The player's choice of weapons... (5 choices each w/ 3 upgrades)
        #[ shooter, missile, sprayer, minions, bombs ]
        """ shooter:    <pts | 0, 175, 300>
                1: shooter
                2: machine gun
                3: gatling gun
            missile:     <pts | 100, 400, 700>
                1: missile launcher
                2: auto launcher
                3: auto seeker
            sprayer:    <pts | 150, 350, 900>
                1: shotgun
                2: flame thrower
                3: party blaster
            minions:    <pts | 200, 1000, 2500>
                1: suicide minion
                2: shooter minion
                3: army
            bombs:      <pts | 250, 1500, 5000>
                1: grenade
                2: reflector **then explodes
                3: attractor **then explodes w/ fragments
        """
        self.unlocked = [0,0,0,0,0]
        self.selected = 0
        self.points = 0

    # --- update method --- #
    def update(self):
        if self.isPic == False:
            self.image.fill(self.color)
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.updateEvents()
        #limit shots per frame
        if self.timer != 0:
            if  self.timer < self.alarm:
                self.timer += 1
            else:
                self.timer = 0

    # --- other methods --- #
    def updateEvents(self):
        
        #movement
        if self.event1 == True:
            #stop from leaving window
            #left edge
            if self.rect.left > 0:
                self.rect.x += self.xspeed
            elif self.xspeed < 0:
                self.stopX()
                self.rect.left = 0
            #right edge
            if self.rect.right < WINDOWWIDTH:
                self.rect.x += self.xspeed
            elif self.xspeed > 0:
                self.stopX()
                self.rect.right = WINDOWWIDTH
            #top edge
            if self.rect.top > 0:
                self.rect.y += self.yspeed
            elif self.yspeed < 0:
                self.stopY()
                self.rect.top = 0
            #bottom edge
            if self.rect.bottom < WINDOWHEIGHT:
                self.rect.y += self.yspeed
            elif self.yspeed > 0:
                self.stopY()
                self.rect.bottom = WINDOWHEIGHT
                
        #shooting (lvl 3)
        if self.event2 == True:
            #shoot a bullet
            if self.timer == 0:
                self.timer += 1
                bullet = Bullet(BLACK, 4, 8)
                bullet.convertToPic(BULLET_DGREY, 1.8)
                bullet.load(self, self.bullets)
                bullet.aim(90, 1)
                bullet.fire(18)

        #sprayer (lvl 2)
        if self.event3 == True:
            if self.timer == 0:
                self.timer += 1
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(90, 30)
                flame.fire(5)
                flame.wiggle = True #--1
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(100, 30)
                flame.fire(5)       #--2
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(80, 30)
                flame.fire(5)       #--3
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(95, 15)
                flame.fire(5)
                flame.wiggle = True #--4
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(85, 15)
                flame.fire(5)
                flame.wiggle = True #--5

    # --- END UPDATING EVENTS --- #
    

    #shoots depending on selected weapon
    #returns  0 if success
    #returns -1 if warning
    #returns -2 if error
    def shoot(self, bullets, baddies, fps):
        
        #shooter
        if self.selected == 0:
            
            #locked
            if self.unlocked[0] == 0:
                print("Warning: shooter is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[0] == 1:
                #allow a shot every 1/4 sec
                self.alarm = int(fps/4)
                #shoot a bullet
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DGREY, 4, 8)
                    bullet.convertToPic(BULLET_LGREY, 1.8)
                    bullet.load(self, bullets)
                    bullet.aim(90, 5)
                    bullet.fire(6)

            #lvl 2
            elif self.unlocked[0] == 2:
                #allow a shot every 1/fps sec
                self.alarm = 1
                #shoot a bullet
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DDGREY, 4, 8)
                    bullet.convertToPic(BULLET_GREY, 1.8)
                    bullet.load(self, bullets)
                    bullet.aim(90, 10)
                    bullet.fire(10)

            #lvl 3
            elif self.unlocked[0] == 3:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/30 sec
                self.alarm = int(fps/30)
                #allow holding down to keep shooting
                self.event2 = True

            else:
                print("Error: player is trying to shoot with an incorrect weapon selection")
                return -2
            
        #missile
        elif self.selected == 1:
            
            #locked
            if self.unlocked[1] == 0:
                print("Warning: missile is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[1] == 1:
                #allow a shot every 1/2 sec
                self.alarm = int(fps/2)
                #shoot a missile
                if self.timer == 0:
                    self.timer += 1
                    missile = Missile(PURPLE, 5, 16)
                    missile.convertToPic(MISSLE_BASIC, 1.7)
                    missile.load(self, bullets)
                    missile.getGroups(bullets, baddies)
                    missile.aim(90, 3)
                    missile.fire(3)

            #lvl 2
            elif self.unlocked[1] == 2:
                pass

            #lvl 3
            elif self.unlocked[1] == 3:
                pass

            else:
                print("Error: player is trying to shoot with an incorrect weapon selection")
                return -2
            
        #sprayer
        elif self.selected == 2:

            #locked
            if self.unlocked[2] == 0:
                print("Warning: sprayer is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[2] == 1:
                #allow a shot every 1 sec
                self.alarm = int(fps)
                #shoot 3 bullets, 4 fragments
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(90, 4)
                    bullet.fire(16) #--1
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(95, 6)
                    bullet.fire(15) #--2
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(85, 6)
                    bullet.fire(15) #--3

            #lvl 2
            elif self.unlocked[2] == 2:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/15 sec
                self.alarm = int(fps/15)
                #allow holding down to keep shooting
                self.event3 = True

            #lvl 3
            elif self.unlocked[2] == 3:
                #allow a shot every 1/4 sec
                self.alarm = int(fps/4)
                #...

            else:
                print("Error: player is trying to shoot with an incorrect weapon selection")
                return -2
            
        #minions
        elif self.selected == 3:
            pass
        #bombs
        elif self.selected == 4:
            pass
        #error
        else:
            print("Error: player is trying to shoot with an incorrect weapon selection")
            return -2

        #if all goes well, return 0
        return 0

    def stopShooting(self):
        self.event2 = False
        self.event3 = False
            




#if this is file running, run this main
if __name__ == "__main__":
    main()

