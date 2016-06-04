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
        self.isPic = False

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

        #------junk***
        self.ph = False

    # --- update method --- #
    def update(self):
        if self.isPic == False:
            self.image.fill(self.color)
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.updateEvents()

    # --- other methods --- #
    def updateEvents(self):
        #Use this when you want some action to be
        # continuous. (any press & hold action)
        pass

    def convertToPic(self, pic, scale=1):
        self.isPic = True
        oldCenter = self.rect.center
        self.image = pygame.image.load( pic ).convert_alpha()
        if scale != 1:
            self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect  = self.image.get_rect()
        self.rect.center = oldCenter

    def convertToColor(self, color, w, h):
        self.isPic = False
        self.color = color
        
        oldCenter = self.rect.center
        self.setImage(w,h)
        self.rect.center = oldCenter

    def setImage(self, xsize, ysize):
        #use if isPic == False
        self.image = pygame.Surface( (xsize, ysize) )
        self.rect = self.image.get_rect()
    
    def setCenterPos(self, xPos, yPos):
        self.rect.centerx = xPos
        self.rect.centery = yPos

    def changeSize(self, w, h):
        #use if isPic == False
        xtemp = self.rect.centerx
        ytemp = self.rect.centery
        self.setImage(w, h)
        self.rect.centerx = xtemp
        self.rect.centery = ytemp

    def rotate(self, angle):
        #image becomes low quality
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

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
