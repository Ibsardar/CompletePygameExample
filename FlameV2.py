""" FlameV2.py
    by Ibrahim Sardar

    **messy**  an update (V3) is very possible
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
class FlameV2(Bullet):
    #initializer
    def __init__(self, color, w, h, w_max, h_max):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(w, h)
        self.color = color
        self.isPic = False
        self.dmg = 0
        self.w_max = w_max
        self.h_max = h_max
        
        self.dir   = 0
        self.x_acc = 0.0 #accurate x pos
        self.y_acc = 0.0 #accurate y pos

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0
        self.xaccel = 0
        self.yaccel = 0

        self.group = None
        
        self.burnOut = False

        self.wiggle = False

        self.smokeLevel = 0

        self.len = 10

        self.noBlack = False
        self.noRed = False
        
    
    # --- other methods --- #
    def updateEvents(self):
        #movement
        if self.event1 == True:
            if self.wiggle == True:
                #make the flame move around a little bit
                self.doWiggle()
            #update accurate position
            self.x_acc += self.xspeed
            self.y_acc += self.yspeed
            #update real position
            self.rect.x = self.x_acc
            self.rect.y = self.y_acc
            #update speed
            self.xspeed += self.xaccel
            self.yspeed += self.yaccel
            #destroy if leaves (much past) window
            if(self.rect.left   > WINDOWWIDTH+50  or
               self.rect.right  < 0-50            or
               self.rect.bottom < 0-50            or
               self.rect.top    > WINDOWHEIGHT+50):

                self.kill()
        #size
        if self.rect.w+1 >= self.w_max or self.rect.h+1 >= self.h_max:
            self.smoke()

            #avoid smoke from becoming black
            if self.noBlack == True:
                if(self.color[0] < 100 and
                   self.color[1] < 100 and
                   self.color[2] < 100):
                    self.kill()
                    
            #self destruct when black
            elif self.color == (0,0,0):
                self.kill()
                
        elif self.rect.w <= self.rect.h:
            self.changeSize(self.rect.w+1, self.rect.h)
            
        else:
            self.changeSize(self.rect.w, self.rect.h+1)
            
        #color
        R = self.color[0]
        G = self.color[1]
        B = self.color[2]

        if self.burnOut == False:
            grey = int( (R+G+B)/3 )
            #\\ YELLOW to RED
            if R == 255 and G != 0 and self.color[2] == 0:
                G = self.fadeTo(G, 0, self.len-4)
            #\\ RED to GREY
            else:
                #kill self if noRed:
                if self.noRed == True:
                    self.kill()
                #fade
                R = self.fadeTo(R, grey, self.len + 10)
                G = self.fadeTo(G, grey, self.len + 10)
                B = self.fadeTo(B, grey, self.len + 10)
            if R == grey and G == grey and B == grey:
                self.burnOut = True
        else:
            #\\ GREY to BLACK
            R = self.fadeTo(R, 0, self.len-4)
            G = self.fadeTo(G, 0, self.len-4)
            B = self.fadeTo(B, 0, self.len-4)
        self.color = (R, G, B)

    def fadeTo(self, n, nTarget, mag):
        #fades a number towards another number by mag
        if n > nTarget:
            n -= mag
            if n < nTarget:
                n = nTarget
            return n
        
        elif n < nTarget:
            n += mag
            if n > nTarget:
                n = nTarget
            return n
        
        else:
            return n

    def doWiggle(self):
        xa_rnd = 0.001 * random.randint(0, 1500)
        if self.xaccel > 0:
            self.xaccel = -xa_rnd
        else:
            self.xaccel = xa_rnd

    def load(self, block, group, side):
        #what side should the flame start from
        if side == 'N':
            self.setCenterPos(block.rect.centerx, block.rect.top-self.rect.height )
        elif side == 'S':
            self.setCenterPos(block.rect.centerx, block.rect.bottom+self.rect.height )
        elif side == 'W':
            self.setCenterPos(block.rect.left+block.rect.width, block.rect.centery )
        elif side == 'E':
            self.setCenterPos(block.rect.right-block.rect.width, block.rect.centery )
        elif side == 'C':
            self.setCenterPos(block.rect.centerx, block.rect.centery)
        else:
            self.setCenterPos(0, 0)
        #add to main bullet group
        group.add(self)
        #set group for this class
        self.group = group

    def smoke(self):
        if self.smokeLevel > 0:
            hue_rnd = random.randint(115,200)
            size_rnd = random.randint(int(2*self.w_max/4),self.w_max-1)
            #highest smoke level = 10000, lowest = 1
            exist_rnd = random.randint(0,int(10000 / (self.smokeLevel+1) ))
            color = ( hue_rnd, hue_rnd, hue_rnd )
            if exist_rnd == 1:
                smoke = Bullet(color, size_rnd, size_rnd)
                smoke.load(self, self.group)
                smoke.aim(90, 75)
                smoke.fire(1)




#if this is file running, run this main
if __name__ == "__main__":
    main()
