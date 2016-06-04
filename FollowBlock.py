""" FollowBlock.py
    By Ibrahim Sardar
"""

#load
import pygame, random, math

#init
pygame.init()

#FollowBlock
class FollowBlock(pygame.sprite.Sprite):

    def __init__(self, surface, imgFile, imgRot=0):
        """ constructor
            params:
              surface to blit to
              imgFile containing graphics
              rotation of imgFile *opt*
        """
        pygame.sprite.Sprite.__init__(self)
        self.setPic(imgFile, imgRot)
        
        #pos
        self.x = self.rect.x
        self.y = self.rect.y
        
        #vel
        self.speed = 0
        self.dx = 0
        self.dy = 0
        
        #acc
        self.accel = 0
        
        #ang
        self.dir = 0
        self.rot = 0
        self.dr = 0

        #max/min
        self.maxRot = 0
        
        #other
        self.surface = surface
        self.isSeek = False
        self.target = None
        self.targetGroup = None
        #   (top, right, bottom, left)
        self.seekBounds = [ 0, surface.get_width(), surface.get_height(), 0 ]

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
        
        #seek to target
        if self.isSeek == True:
            self.toTarget()

        #updates movement
        self.move()

        #updateGraphics
        self.render()

        #update bounds event(s)
        self.updateBoundsCondition()

        #additional custom updates
        self.updateMore()

    def move(self):
        """ updates all movement
        """
        #   accel
        #
        #linear acceleration
        self.speed += self.accel
        #angular acceleration (affects both orientation and direction)
        self.rot += self.dr
        self.dir += self.dr

        #   speed
        #
        #convert to radians
        theta = self.dir * math.pi / 180
        theta *= -1
        #speed vector
        self.dx = math.cos(theta) * self.speed
        self.dy = math.sin(theta) * self.speed
        #update diff in x and y position
        self.x += self.dx
        self.y += self.dy

        #   image & rect
        #
        #update actual orientation
        self.rotate(self.rot)
        #update actual rect
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self):
        """ draws self's image on surface
        """
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def updateBoundsCondition(self):
        """ overwrite this for custom bounds condition
        """
        pass

    def updateMore(self):
        """ overwrite this for custom updates
        """
        pass
    
    
    #\
    ##>--- GET methods ---------------------------------<
    #/
    
    
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
        cx = self.x + self.rect.w/2
        cy = self.y + self.rect.h/2
        center = (cx, cy)
        return center

    
    #|
    #|> speed-related:

    
    def getSpeedX(self):
        """ returns the accurate speed in
            the x direction
        """
        rads = self.dir * math.pi / 180
        return math.cos(rads) * self.speed

    def getSpeedY(self):
        """ returns the accurate speed in
            the y direction
        """
        rads = self.dir * math.pi / 180
        return math.sin(rads) * self.speed * -1

    def getSpeed(self):
        """ returns the accurate speed
        """
        return self.speed

    
    #|
    #|> acceleration-related:

    
    def getAccelX(self):
        """ returns the accurate acceleration
            in the x direction
        """
        rads = self.dir * math.pi / 180
        return math.cos(rads) * self.accel

    def getAccelY(self):
        """ returns the accurate acceleration
            in the y direction
        """
        rads = self.dir * math.pi / 180
        return math.sin(rads) * self.accel * -1

    def getAccel(self):
        """ returns the accurate acceleration
        """
        return self.accel

    
    #|
    #|> angular:

    
    def getDir(self):
        """ returns the accurate angle (deg)
        """
        return self.dir

    def getAngSpeed(self):
        """ returns the accurate angular speed
            (deg per update)
        """
        return self.rot

    def getAngAccel(self):
        """ returns the accurate angular acceleration
            (angular speed per update)
        """
        return self.dr

    
    #|
    #|> other:

    
    def getTarget(self):
        """ returns the current target
            returns None if there is no target
            target should consist of type pygame.Rect
        """
        return self.target
    

    #\
    ##>--- SET methods ---------------------------------<
    #/


    #|
    #|> visual:

    def setPic(self, pic, rot):
        """ sets a custom image for self
            rotates to desired default orientation
        """
        self.imageLord = pygame.image.load( pic ).convert_alpha()
        #rotate counter-clockwise 'rot' degrees
        self.imageLord = pygame.transform.rotate(self.imageLord, rot)
        self.imageLord = self.imageLord.convert_alpha()
        
        self.image = self.imageLord
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
        self.y = y

    def setCenter(self, center):
        """ sets center position
        """
        self.x = center[0] - self.rect.w/2
        self.y = center[1] - self.rect.h/2


    #|
    #|> speed-related


    def setSpeed(self, speed):
        """ sets the accurate speed
        """
        self.speed = speed


    #|
    #|> acceleration-related:


    def setAccel(self, accel):
        """ sets the accurate acceleration
        """
        self.accel = accel

    
    #|
    #|> angular:

    
    def setDir(self, ang):
        """ sets the accurate angle
            also rotates the orientation
        """
        self.dir = ang
        self.rot = ang

    def setAngAccel(self, angaccel):
        """ sets the accurate angular acceleration
        """
        self.dr = -angaccel

    
    #|
    #|> other:


    def setTarget(self, target):
        """ sets a target
        """
        self.target = target
        

    #\
    ##>--- OTHER methods ---------------------------------<
    #/

    def rotate(self, angle):
        """ rotates original image by 'angle' degrees
        """
        oldCenter = self.getCenter()
        self.image = self.imageLord
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = self.image.convert_alpha()
        self.rect  = self.image.get_rect()
        self.setCenter(oldCenter)

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
        """ prints out variable information of self
            'self.debugDelay' is the time (frames) interval of each trace
        """
        if self.debugTimer == 0:
            self.debugTimer += 1
            print("---TRACE--------------")
            print("self.rect: (w,h): ", self.rect.w, ", ", self.rect.h)
            print("self: (x,y): ", self.x, ", ", self.y)
            print("self.rect: (x,y): ", self.rect.x, ", ", self.rect.y)
            print("self: speed(x,y): ", self.dx, ", ", self.dy, ", speed: ", self.speed, ", accel: ", self.accel)
            print("self: ang(dir, speed, accel): ", self.dir, ", ", self.rot, ", ", self.dr)
            print("self: maxs/mins: MAXROT: ", self.maxRot)
            print("self: other: \n\timage:", self.image!=None, ", \n\trect: ", self.rect!=None, ", \n\ttarget:", self.target!=None, ", \n\tisSeek: ", self.isSeek, ", \n\ttargets: ", self.targetGroup!=None, ", \n\tseek bounds: ", self.seekBounds)
            print("---END TRACE----------")
        elif self.debugTimer < self.debugDelay:
            self.debugTimer += 1
        else:
            self.debugTimer = 0

    def seek(self, possibleTargets, maxRot, seekBounds=[0,10,10,0]):
        """ enables seeking capabilities by
            setting possible targets of self,
            sets max turning speed
            sets bounds where seeking can occur *opt*
        """
        self.isSeek = True
        self.targetGroup = possibleTargets
        self.maxRot = maxRot
        self.seekBounds = seekBounds

    def find(self):
        """ finds closest target to self by
            looping through all targets and
            then sets self's target
        """
        #min always begins at a large value
        minDist = 9999999
        
        #loop thru all targets
        for target in self.targetGroup:

            #if target is within seeking bounds
            if(target.rect.bottom > self.seekBounds[0] and
               target.rect.left   < self.seekBounds[1] and
               target.rect.top    < self.seekBounds[2] and
               target.rect.right  > self.seekBounds[3]):
                
                #get dist between
                diffx = target.rect.x - self.x
                diffy = target.rect.y - self.y
                minDistTemp = math.sqrt( (diffx**2) + (diffy**2) )

                #if closer than any already checked, select target
                if minDist > minDistTemp:
                    minDist = minDistTemp
                    self.target = target

        #return False if no target found
        if self.target == None:
            return False
        return True
                

    def toTarget(self):
        """ IF there are any possible targets:
             finds the closest target amongst all targets
             changes dir and orientation to turn towards the target
        """
        
        #find the target, don't seek if none are found
        if self.find() == True:

            #angle to target where self is the origin
            diffy = self.target.rect.centery - self.rect.centery
            diffx = self.target.rect.centerx - self.rect.centerx
            incline = math.atan2(-diffy, diffx) * 180 / math.pi
            
            #get turning angle where cc-wise is positive
            turn = incline - self.dir
            
            #choose quicker turn direction
            if turn > 180:
                turn = 360 - turn
                turn *= -1
            elif turn < -180:
                turn = 360 + turn

            #angle to set self to later
            ang = self.dir
            
            #if max turning limit reached
            if abs(turn) > self.maxRot:
                #check if turn direction is pos or neg
                if turn > 0:
                    ang += self.maxRot
                elif turn < 0:
                    ang -= self.maxRot

            #if max turning limit NOT reached
            elif abs(turn) < self.maxRot:
                #no checking needed since 'turn' is already signed appropriately
                ang += turn

            #point to target
            self.setDir(ang)

            
#===========================================================
#======================== DEBUG ============================
#===========================================================
def main():
    import sys
    from Block import Block

    PH_TARGET = "Graphics\placeholder_target.png"
    WINDOWWIDTH = 720
    WINDOWHEIGHT = 380
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    #  N,E,S,W
    bounds = [ 0, WINDOWWIDTH, WINDOWHEIGHT, 0 ]
    timer = pygame.time.Clock()
    fps = 60

    a = Block((255,0,0), 500, 220, 32, 32)
    b = Block((0,255,0), 300, 120, 16, 16)
    c = Block((0,0,255), 100, 20, 8, 8)
    
    gr = pygame.sprite.Group()
    gr2 = pygame.sprite.Group()
    gr.add( a, b, c )
    
    f = FollowBlock(windowSurface, "Graphics\missile01.png", -90)
    f.setCenter( (160, 245) )
    f.speed = 8
    f.setDir( 90 )
    f.seek(gr, 10, bounds)

    while(True):

        #wrap
        for i in gr:
            if i.rect.centery <= 0:
                i.rect.centery = WINDOWHEIGHT
                i.rect.centerx = random.randint(20, 700)
            else:
                i.rect.y -= 4

        #random teleport
        for i in gr:
            
            if i.rect.colliderect( f ):
                i.setCenterPos(random.randint(50,670), random.randint(50,330))
                side = random.randint(8,32)
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                i.convertToColor( (r,g,b), side, side )
                i.ph = False
                
            for j in gr2:
                if i.rect.colliderect( j ):
                    i.kill()
                    j.kill()

        #CHECK FOR WIN
        cnt = 0
        for enemy in gr:
            cnt += 1
        if cnt == 0:
            input(" YOU WIN ! (press enter bro)\n")
            pygame.quit()
            sys.exit()

        #events
        for event in pygame.event.get():

            #QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #CREATE BLOCK
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    side = random.randint(8,32)
                    x = random.randint(side,WINDOWWIDTH-side)
                    y = random.randint(side,WINDOWHEIGHT-side)
                    r = random.randint(0,255)
                    g = random.randint(0,255)
                    b = random.randint(0,255)
                    blok = Block((r,g,b), x, y, side, side)
                    blok2 = Block((r,g,b), x, y, side, side)
                    gr.add( blok, blok2 )
                    if f.speed < 16:
                        f.speed += 1
                    else:
                        rnd = random.randint(1,6)
                        for i in range(rnd):
                            f2 = FollowBlock(windowSurface, "Graphics\missile02.png", -90)
                            f2.setCenter( (WINDOWWIDTH/2, WINDOWHEIGHT) )
                            f2.speed = 4.5
                            f2.setDir( random.randint(15,165) )
                            f2.seek(gr, 5, bounds)
                            gr2.add(f2)

        #destroy extra missile if leave window:
        for b in gr2:
            if(b.rect.left   > WINDOWWIDTH  or
               b.rect.right  < 0            or
               b.rect.bottom < 0            or
               b.rect.top    > WINDOWHEIGHT):

                b.kill()

        #update
        windowSurface.fill( (245,145,45) )
        gr.update()
        gr2.update()
        f.update()
        pygame.display.update()

        #fps
        timer.tick(60)
#===========================================================
#======================= END DEBUG =========================
#===========================================================


if __name__ == "__main__":
    main()
