""" Flame.py
    by Ibrahim Sardar

    WARNING: very messy and crappy but it does what I want !!!
"""

#general housekeeping
import pygame, math, random, Block, Bullet
from Block import Block
from Bullet import Bullet
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
        self.dmg = 0
        
        self.dir   = 0.0 #accurate angle
        self.x_acc = 0.0 #accurate x pos
        self.y_acc = 0.0 #accurate y pos

        self.event1 = False
        self.xspeed = 0.0 #accurate x vel
        self.yspeed = 0.0 #accurate y vel
        self.xaccel = 0.0 #accurate x accel
        self.yaccel = 0.0 #accurate y accel

        self.event2 = False
        self.origSize = (w, h) #original size
        self.waccel   = 0.0 #accurate width accel
        self.haccel   = 0.0 #accurate height accel
        self.margin   = 0.0 #accurate angle margin
        self.bullets  = None

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
        #flame size
        if self.event2 == True:
            #decrease size
            self.changeSize(self.rect.w + self.waccel, self.rect.h + self.haccel)
            #split into 2 halves if size is half IFF size is not 0
            wlimit = self.origSize[0]/1.1
            hlimit = self.origSize[1]/1.1
            
            if self.rect.w <= 6 or self.rect.h <= 6:
                self.kill()
                rnd = random.randint(0,300)
                if rnd == 1:
                    crnd = random.randint(0,200)
                    srnd = random.randint(2,5)
                    smoke = Bullet( (crnd,crnd,crnd), srnd,srnd)
                    smoke.load(self, self.bullets)
                    smoke.aim(self.dir, self.margin)
                    smoke.fire(1)
                    smoke.yaccel = 0
                    
            elif self.rect.w <= wlimit and self.rect.h <= hlimit:
                #prepare some variables
                speed = int(math.sqrt( (self.xspeed**2) + (self.yspeed**2) ))
                color = self.incrementColor()
                self.margin += 15
                #make 2 more flames
                flame = Flame(color, wlimit, hlimit)
                flame.load(self, self.bullets)
                flame.aim(70, self.margin)
                flame.throw(speed, self.xaccel, self.yaccel, self.waccel, self.haccel) #--1
                flame = Flame(color, wlimit, hlimit)
                flame.load(self, self.bullets)
                flame.aim(110, self.margin)
                flame.throw(speed, self.xaccel, self.yaccel, self.waccel, self.haccel) #--2

    def incrementColor(self):
        #increases G of RGB by 50
        G = self.color[1] + 50
        if G > 255:
            G = 255
        return (self.color[0], G, self.color[2])

    def setCenterPos(self, xPos, yPos):
        self.rect.centerx = self.x_acc = xPos
        self.rect.centery = self.y_acc = yPos

    def load(self, block, group):
        self.setCenterPos(block.rect.centerx, block.rect.centery)
        group.add(self)
        #update current bullet group for this class
        self.bullets = group

    def aim(self, angle, margin):
        #FIRST, set self's margin
        self.margin = margin
        #the big number allows many decimal places
        margin = margin * 100000000
        angle = angle * 100000000
        self.dir = random.randint(angle-margin, angle+margin)/100000000
        

    def throw(self, speed, xaccel, yaccel, waccel, haccel):
        #randomize speed a bit:
        speed = random.randint(speed*1000-700, speed*1000+2300)/1000
        #convert angle to radians
        dir_rad = math.radians(self.dir)
        
        dx = math.cos(dir_rad) * speed
        dy = math.sin(dir_rad) * speed
        
        self.xaccel = xaccel
        self.yaccel = -yaccel
        self.waccel = waccel
        self.haccel = haccel

        self.event2 = True
        self.moveX( dx )
        self.moveY( dy )



#if this is file running, run this main
if __name__ == "__main__":
    main()
