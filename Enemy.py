""" Enemy.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame, math, Block
from Block import Block
pygame.init()
#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380

#Player
class Enemy(Block):
    #initializer
    def __init__(self, color, w, h):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(w, h)
        self.color = color
        self.isPic = False

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0
        self.xaccel = 0
        self.yaccel = 0

        #junk
        self.ph=False

    # --- other methods --- #
    def updateEvents(self):
        #movement
        if self.event1 == True:
            self.xspeed += self.xaccel
            self.yspeed += self.yaccel
            self.rect.x += int(self.xspeed)
            self.rect.y += int(self.yspeed)
            #destroy if leaves window
            if(self.rect.left   > WINDOWWIDTH  or
               self.rect.right  < 0            or
               self.rect.top    > WINDOWHEIGHT):

                self.kill()

    def getPoints(self):
        val = self.rect.width*self.rect.height
        if val < 500:
            return 5
        elif val < 1000:
            return 10
        elif val < 2500:
            return 15
        else:
            return 20

    #IGNORE THIS FUNCTION
    def moveTowards(self, target, accel):

        # DOESN'T WORK...
        
        #angle to target where self is the origin
        diffy = target.rect.centery - self.rect.centery
        diffx = target.rect.centerx - self.rect.centerx
        theta = math.atan2(-diffy, diffx) * 180 / math.pi
        
        #accelerate in said direction (degenerates by 0.1/frame)
        self.xaccel = accel * math.cos(theta)
        self.yaccel = accel * math.sin(theta)
        print("STATS (for single ast)")
        print("angle to ast: ", theta)
        print("(x,y) accel: ", self.xaccel, ",", self.yaccel)


#if this is file running, run this main
if __name__ == "__main__":
    main()

