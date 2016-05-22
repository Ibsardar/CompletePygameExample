""" Flame.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame, math, random, Block
from Block import Block
pygame.init()
#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380

#Bullet
class Flame(Block):
    #initializer
    def __init__(self, color, w, h):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(w, h)
        self.color = color
        
        self.dir   = 0.0 #accurate angle
        self.x_acc = 0.0 #accurate x pos
        self.y_acc = 0.0 #accurate y pos

        self.event1 = False
        self.xspeed = 0.0 #accurate x vel
        self.yspeed = 0.0 #accurate y vel
        self.xaccel = 0.0 #accurate x accel
        self.yaccel = 0.0 #accurate y accel

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

    def setCenterPos(self, xPos, yPos):
        self.rect.centerx = self.x_acc = xPos
        self.rect.centery = self.y_acc = yPos

    def load(self, block, group):
        self.setCenterPos(block.rect.centerx, block.rect.centery)
        group.add(self)

    def aim(self, angle, margin):
        #the big number allows many decimal places
        margin = margin * 100000000
        angle = angle * 100000000
        self.dir = random.randint(angle-margin, angle+margin)/100000000

    def throw(self, speed, yaccel):
        #convert angle to radians
        dir_rad = math.radians(self.dir)
        
        dx = math.cos(dir_rad) * speed
        dy = math.sin(dir_rad) * speed

        self.yaccel = math.sin(dir_rad) * -yaccel

        self.moveX( dx )
        self.moveY( dy )




#if this is file running, run this main
if __name__ == "__main__":
    main()
