""" MissileV2.py
    By Ibrahim Sardar
"""

#load
import pygame, random, math, Block, FlameV2

from Block import Block

from FlameV2 import FlameV2

#init
pygame.init()

#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380
windowSurface = pygame.display.set_mode( (WINDOWWIDTH,WINDOWHEIGHT) )

#color
YELLOW = (255,255,0)

#pics
PH_TARGET = "Graphics/placeholder_target.png"

#MissileV2
class MissileV2(Block):

    def __init__(self):
        """ constructor
        """
        pygame.sprite.Sprite.__init__(self)
        
        #dim
        self.w = 0  #irrelevant if isPic is True
        self.h = 0  #irrelevant if isPic is True
        
        #pos
        self.x = 0
        self.y = 0
        
        #vel
        self.xspeed = 0
        self.yspeed = 0
        
        #acc
        self.xaccel = 0
        self.yaccel = 0
        
        #dir
        self.ang = 0
        self.angspeed = 0
        self.angaccel = 0

        #max/min
        self.maxRot = 0
        
        #other
        self.image = None
        self.rect = None
        self.color = None  #irrelevant if isPic is True
        self.target = None
        self.isPic = True
        self.isSeek = False
        self.bullets = None
        self.targets = None
        self.source = None

        #--debug--#
        self.isDebug = False
        self.debugDelay = 0
        self.debugTimer = 0
        #--debug--#


    #\
    ##>--- UPDATE methods ---------------------------------<
    #/

        
    def update(self):
        """ updates all changing attributes
            of self.
        """
        self.updateRotational() #angular: speed, accel
        self.updateLinear() #x and y: speed, accel
        self.updateImage() #(w,h) or image, (x,y), angle
        self.updateBoundsCondition() #kill if leave window
        self.trail() #FlameV2 in the rear
        if self.isSeek == True:
            self.toTarget() #change ang and angspeed towards target
        if self.isDebug == True:
            self.__trace()

    def updateRotational(self):
        """ updates rotational movement
        """
        #accelerate the turn
        self.angspeed += self.angaccel
        
        #turn
        self.ang += self.angspeed

        #update angular speed

        #update angular acceleration

    def updateLinear(self):
        """ updates linear movement
        """
        #accelerate
        self.xspeed += self.xaccel
        self.yspeed += self.yaccel

        #convert the angle to radians
        rads = self.ang * math.pi / 180

        #update speed vector
        self.xspeed = math.cos( rads ) * self.getSpeed()
        self.yspeed = math.sin( rads ) * self.getSpeed() * -1

        #update acceleration vector
        self.xaccel = math.cos( rads ) * self.getAccel()
        self.yaccel = math.sin( rads ) * self.getAccel() * -1
        
        #move
        self.x += self.xspeed
        self.y += self.yspeed

    def updateImage(self):
        """ updates scale, position, and direction
            scale cannot change if image is a picture
        """ 
        #position
        self.rect.x = self.x
        self.rect.y = self.y
        
        #rotate
        self.rotate(self.angspeed)

        #blit
        if self.isPic == False:
            self.image.fill(self.color)
            self.changeSize(self.w, self.h)
        if self.image != None:
            windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            print("Error: Image not loaded")

    def updateBoundsCondition(self):
        """ deletes self if self has gone
            much past the bounds
        """
        if(self.rect.left   > WINDOWWIDTH+50  or
           self.rect.right  < 0-50            or
           self.rect.bottom < 0-50            or
           self.rect.top    > WINDOWHEIGHT+50):

            self.kill()
    
    
    #\
    ##>--- GET methods ---------------------------------<
    #/


    #|
    #|> visual


    def getW(self):
        """ returns the accurate width
        """
        return self.w

    def getH(self):
        """ returns the accurate height
        """
        return self.h

    def getColor(self):
        """ returns the color
        """
        return self.color
    
    
    #|
    #|> positional:

    
    def getX(self):
        """ returns the accurate x position
        """
        return self.x

    def getY(self):
        """ returns the accurate y position
        """
        return self.y

    def getCenter(self):
        """ returns the accurate center coordinates
        """
        cx = self.x + self.w/2
        cy = self.y + self.h/2
        center = (cx, cy)
        return center

    
    #|
    #|> speed-related:

    
    def getSpeedX(self):
        """ returns the accurate speed in
            the x direction
        """
        return self.xspeed

    def getSpeedY(self):
        """ returns the accurate speed in
            the y direction
        """
        return self.yspeed

    def getSpeed(self):
        """ returns the accurate speed
        """
        s = (self.xspeed**2) + (self.yspeed**2)
        s = math.sqrt(s)
        return s

    
    #|
    #|> acceleration-related:

    
    def getAccelX(self):
        """ returns the accurate acceleration
            in the x direction
        """
        return self.xaccel

    def getAccelY(self):
        """ returns the accurate acceleration
            in the y direction
        """
        return self.yaccel

    def getAccel(self):
        """ returns the accurate acceleration
        """
        a = (self.xaccel**2) + (self.yaccel**2)
        a = math.sqrt(a)
        return a

    
    #|
    #|> angular:

    
    def getAng(self):
        """ returns the accurate angle (deg)
        """
        return self.ang

    def getAngSpeed(self):
        """ returns the accurate angular speed
            (deg per update)
        """
        return self.angspeed

    def getAngAccel(self):
        """ returns the accurate angular acceleration
            (angular speed per update)
        """
        return self.angaccel

    
    #|
    #|> other:

    
    def getTarget(self):
        """ returns the current target
            returns None if there is no target
        """
        return self.target
    

    #\
    ##>--- SET methods ---------------------------------<
    #/


    #|
    #|> visual:


    def setSize(self, size):
        """ sets accurate width and height
        """
        self.w = size[0]
        self.h = size[1]
        self.setImage( size[0], size[1] )

    def setColor(self, color):
        """ sets a color
        """
        self.color = color

    def setPicture(self, pic):
        """ sets a custom image for self
            enables isPic
        """
        self.image = pygame.image.load( pic ).convert_alpha()
        self.rect = self.image.get_rect()
        self.isPic = True


    #|
    #|> positional:


    def setX(self, x):
        """ sets x position (top left)
        """
        self.x = x

    def setY(self, y):
        """ sets y position (top left)
        """

    def setCenter(self, center):
        """ sets center position
        """
        self.x = center[0] - self.w/2
        self.y = center[1] - self.h/2


    #|
    #|> speed-related


    def setSpeedX(self, xspeed):
        """ sets the accurate speed in
            the x direction
        """
        self.xspeed = xspeed

    def setSpeedY(self, yspeed):
        """ sets the accurate speed in
            the x direction
        """
        self.xspeed = xspeed

    def setSpeed(self, speed):
        """ sets the accurate speed in
            the x and y directions according
            to the current angle
        """
        radians = self.ang * math.pi / 180
        
        self.xspeed = math.cos(radians) * speed
        self.yspeed = math.sin(radians) * speed * -1


    #|
    #|> acceleration-related:

    
    def setAccelX(self, xaccel):
        """ sets the accurate acceleration
            in the x direction
        """
        self.xaccel = xaccel

    def setAccelY(self, yaccel):
        """ sets the accurate acceleration
            in the y direction
        """
        self.yaccel = yaccel

    def setAccel(self, accel):
        """ sets the accurate acceleration in
            the x and y directions according
            to the current angle
        """
        radians = self.ang * math.pi / 180
        
        self.xaccel = math.cos(radians) * accel
        self.yaccel = math.sin(radians) * accel * -1

    
    #|
    #|> angular:

    
    def setAng(self, ang):
        """ sets the accurate angle
        """
        self.ang = ang

    def setAngSpeed(self, angspeed):
        """ sets the accurate angular speed
        """
        self.angspeed = angspeed

    def setAngAccel(self, angaccel):
        """ sets the accurate angular acceleration
        """
        self.angaccel = angspeed

    
    #|
    #|> other:


    def setTarget(self, target):
        """ sets a target
        """
        self.target = target

    def setBulletGroup(self, bulletGroup):
        """ sets bullet sprite group for various
            bullets to be loaded into
        """
        self.bullets = bulletGroup
        

    #\
    ##>--- OTHER methods ---------------------------------<
    #/

    def debug(self, delay):
        """ stops printing all of self's info if delay is < 1
            else, print all of self's info every 'delay' frames
        """
        if delay >= 1:
            self.isDebug = True
            self.debugDelay = delay
            self.debugTimer = 0
        else:
            self.isDebug = False
    
    def __trace(self):
        """ prints out information on each missile
            'self.debugDelay' is the time (frames) interval of each trace
        """
        if self.debugTimer == 0:
            self.debugTimer += 1
            print("---TRACE--------------")
            print("self: (w,h): ", self.w, ", ", self.h)
            print("self.rect: (w,h): ", self.rect.w, ", ", self.rect.h)
            print("self: (x,y): ", self.x, ", ", self.y)
            print("self.rect: (x,y): ", self.rect.x, ", ", self.rect.y)
            print("self: speed(x,y): ", self.xspeed, ", ", self.yspeed)
            print("self: accel(x,y): ", self.xaccel, ", ", self.yaccel)
            print("self: ang(ang, speed, accel): ", self.ang, ", ", self.angspeed, ", ", self.angaccel)
            print("self: maxs/mins: MAXROT: ", self.maxRot)
            print("self: other: \n\timage:", self.image!=None, ", \n\trect: ", self.rect!=None, ", \n\tcolor: ", self.color, ", \n\ttarget:", self.target!=None, ", \n\tisPic: ", self.isPic, ", \n\tisSeek: ", self.isSeek, ", \n\tbullets: ", self.bullets!=None, ", \n\ttargets: ", self.targets!=None, ", \n\tsource: ", self.source!=None)
            print("---END TRACE----------")
        elif self.debugTimer < self.debugDelay:
            self.debugTimer += 1
        else:
            self.debugTimer = 0

    def seek(self, possibleTargets, maxRot, source):
        """ enables seeking capabilities by
            setting possible targets of self
            sets max turning speed
            sets source of launch
        """
        self.isSeek = True
        self.targets = possibleTargets
        self.maxRot = maxRot
        self.source = source

    def find(self):
        """ finds closest target to self by
            looping through all targets and
            then sets self's target
        """
        #min always begins at a large value
        minDist = 9999999
        
        #loop thru all targets
        for target in self.targets:

            #if target is above source
            if target.rect.y < self.source.rect.y:
            
                #get dist between
                diffx = target.rect.x - self.x
                diffy = target.rect.y - self.y
                minDistTemp = math.sqrt( (diffx**2) + (diffy**2) )

                #if closer than any already checked, select target
                if minDist > minDistTemp:
                    minDist = minDistTemp
                    self.target = target
                

    def toTarget(self):
        """ IF there are any possible targets:
             finds the closest target amongst all targets
             changes angspeed to turn towards the target
        """
        #find the target
        self.find()
        if self.target.ph == False:
            self.target.ph = True
            self.target.convertToPic(PH_TARGET, 0.01)

        #find angle between (deg)
        diffy = self.target.rect.y - self.y
        diffx = self.target.rect.x - self.x
        between = math.atan2(diffy, diffx) * 180 / math.pi
        
        #alter angular movement
        if between == 0:
            self.angspeed = 0
        elif abs(between) < self.maxRot:
            self.angspeed = between
        else:
            self.angspeed = self.maxRot

        

    def trail(self):
        """ creates a trail of fire
            behind self
        """
        flame = FlameV2(YELLOW, 2, 2, 8, 8)
        flame.load(self, self.bullets, 'C')
        flame.aim(self.ang-180, 3)
        flame.fire(2)

    def explode(self):
        """ creates an invisible bomb that
            explodes immediately
        """
        pass
        

if __name__ == "__main__":
    main()
