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
        self.rot   = 0
        self.x_acc = 0.0 #accurate x pos
        self.y_acc = 0.0 #accurate y pos

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0
        self.xaccel = 0
        self.yaccel = 0
        
        self.bullets = None
        self.baddies = None
        self.target  = None

        self.wobble = 0

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
            #normalize xa of missile if not homing
            if self.target == None:
                self.decXAccel(.1)
            #destroy if leaves window
            if(self.rect.left   > WINDOWWIDTH  or
               self.rect.right  < 0            or
               self.rect.bottom < 0            or
               self.rect.top    > WINDOWHEIGHT):

                self.kill()
        #trail
        self.trail()

    def decXAccel(self, dec):
        if self.xaccel > -dec and self.xaccel < dec:
            self.xaccel = 0
        if self.xaccel > 0:
            self.xaccel -= dec
        elif self.xaccel < 0:
            self.xaccel += dec

    def getGroups(self, bullets, baddies):
        self.bullets = bullets
        self.baddies = baddies

    def putForce(self, angle, mag):
        dir_rad = math.radians(angle)
        
        ddx = math.cos(dir_rad) * mag
        ddy = math.sin(dir_rad) * mag
        ddy = -ddy

        self.xaccel += ddx
        self.yaccel += ddy

    def explode(self, vel0, accel0):
        """
        explosion = Bomb(BLACK, 1, 1)
        explosion.load(self, self.bullets)
        explosion.explode(start_angle, end_angle, vel0, accel0, margin)
        """
        pass

    def find(self):
        pass

    def trail(self):
        flame = FlameV2up(YELLOW, 2, 2, 8, 8)
        flame.load(self, self.bullets, 'C')
        flame.aim(self.dir-180, 3)
        flame.fire(2)



#if this is file running, run this main
if __name__ == "__main__":
    main()
