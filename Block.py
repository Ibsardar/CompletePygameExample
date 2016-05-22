""" Block.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame
pygame.init()
#window
WINDOWWIDTH   = 720
WINDOWHEIGHT  = 380
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#Block
class Block(pygame.sprite.Sprite):
    #initializer
    def __init__(self, color, xCenterPos, yCenterPos, xsize, ysize):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.setImage(xsize, ysize)
        self.setCenterPos(xCenterPos, yCenterPos)
        self.color = color

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

    # --- update method --- #
    def update(self):
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.image.fill(self.color)
        self.updateEvents()

    # --- other methods --- #
    def updateEvents(self):
        #Use this when you want some action to be
        # continuous. (any press & hold action)
        pass
    
    def setCenterPos(self, xPos, yPos):
        self.rect.centerx = xPos
        self.rect.centery = yPos

    def setImage(self, xsize, ysize):
        self.image = pygame.Surface( (xsize, ysize) )
        self.rect  = self.image.get_rect()

    def changeSize(self, size):
        xP = self.rect.centerx
        yP = self.rect.centery
        w  = size
        h  = size
        self.setImage(w, h)
        self.rect.centerx = xP
        self.rect.centery = yP

    # *NOTE*  this makes positive speed 'up' and vice versa
    def moveY(self, speed):
        self.event1 = True
        self.yspeed = -speed

    def moveX(self, speed):
        self.event1 = True
        self.xspeed = speed

    def stop(self):
        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

    def stopX(self):
        self.event1 = False
        self.xspeed = 0

    def stopY(self):
        self.event1 = False
        self.yspeed = 0
        




#if this is file running, run this main
if __name__ == "__main__":
    main()
