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

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

    # --- other methods --- #
    def updateEvents(self):
        #movement
        if self.event1 == True:
            self.rect.x += self.xspeed
            self.rect.y += self.yspeed
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
            return 50
            




#if this is file running, run this main
if __name__ == "__main__":
    main()

