""" Missile.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame, math, random, Bullet, FlameV2
from Bullet import Bullet
from FlameV2 import FlameV2
pygame.init()
#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380
#color
YELLOW = (255, 255,   0)

#Bullet
class Missile(Bullet):
    #initializer
    def __init__(self, color, w, h):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(w, h)
        self.color = color
        self.isPic = True
        self.dmg = 0
        
        self.dir   = 0
        self.x_acc = 0.0 #accurate x pos
        self.y_acc = 0.0 #accurate y pos

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0
        self.xaccel = 0
        self.yaccel = 0
        
        self.bullets = None
        self.baddies = None

    # --- other methods --- #
    def updateEvents(self):
        #movement
        if self.event1 == True:
            #update accurate position
            self.x_acc += self.xspeed
            self.y_acc += self.yspeed
            #update real position
            self.rect.x = self.x_acc
            self.rect.y = self.y_acc
            #update speed
            self.xspeed += self.xaccel
            self.yspeed += self.yaccel
            #destroy if leaves window
            if(self.rect.left   > WINDOWWIDTH  or
               self.rect.right  < 0            or
               self.rect.bottom < 0            or
               self.rect.top    > WINDOWHEIGHT):

                self.kill()
        #trail
        self.trail()

    def getGroups(self, bullets, baddies):
        self.bullets = bullets
        self.baddies = baddies

    def trail(self):
        flame = FlameV2(YELLOW, 2, 2, 8, 8)
        flame.load(self, self.bullets, 'C')
        flame.aim(self.dir-180, 3)
        flame.fire(2)



#if this is file running, run this main
if __name__ == "__main__":
    main()
