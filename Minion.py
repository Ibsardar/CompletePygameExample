""" Minion.py
    by Ibrahim Sardar
"""

#load
import pygame, math, random, FlameV2, MissileV3, Bomb, Bullet
from FollowBlock import FollowBlock

#init
pygame.init()

#colors
YELLOW = (255, 255,   0)

#pics
BULLET_RED   = "Graphics\Bullet04.png"
BULLET_GREEN = "Graphics\Bullet05.png"
MISSLE_BASIC = "Graphics\Missile02.png"
BOMB_SMALL   = "Graphics\Bomb01.png"

#Minion
class Minion(FollowBlock):

    def init(self, ang=0):
        """ avoid re-writting a new constructor
            ** optional begin self turned by angle 'ang'
        """
        self.setDir(ang)
        self.group = None
        self.alarm = 0
        self.timer = 0
        self.idleTimer = 0
        self.type = 0
        self.subtype = ""
        self.isIdle = True
        self.isFound = False
        self.health = 100
        self.side = 0

    def setAlarm(self, time):
        self.alarm = int(60*time)
        self.timer = 0

    def setUpdateGroup(self, group):
        self.group = group

    def setTargetGroup(self, group):
        self.targetGroup = group

    def updateBoundsCondition(self):
        """ overwrite ** destroy self if leave window
        """
        if(self.rect.left   > self.surface.get_width() or
           self.rect.right  < 0                        or
           self.rect.bottom < 0                        or
           self.rect.top    > self.surface.get_height()):

            self.kill()

    def updateMore(self):
        """ overwrite ** updates timer and current action
        """

        #increment timer
        if  self.timer < self.alarm:
            self.timer += 1
        elif self.timer >= self.alarm:
            self.timer = 0

        #minion idle animation
        # 0,1,2,3 : all minions have same idle animation
        if self.isIdle:
            self.idle()
        elif self.isFound == False:
            self.speed = 0

        #action based on type
        # 0 : no type
        # 1 : detonates if touched by any. launches self to an enemy in range, stops for a moment, then explodes
        # 2 : has some life. dies if life<=0. rotates to an enemy in range and shoots 3 lasers based on alarm attributes
        # 3 : has little life. dies if life<=0. rotates to an enemy in range and, depending on subtype, shoots either flames if red, rockets if blue, 2 green lasers if green
        if self.type == 1:
            self.suicider()
        elif self.type == 2:
            self.shooter( BULLET_RED, 3, self.side ) #3 red lasers
        elif self.type == 3:
            if self.subtype == "red":
                self.flamer()
            elif self.subtype == "blue":
                self.launcher()
            elif self.subtype == "green":
                self.shooter( BULLET_GREEN, 1 ) #1 green lasers

    def idle(self):
        """ animation of self when idle
        """
        
        #action at time intervals
        if self.idleTimer == 1:
            self.speed = -0.5
        elif self.idleTimer == 30:
            self.speed = 0.5
        elif self.idleTimer >= 60:
            self.idleTimer = 0
            
        #increment timer
        self.idleTimer += 1

    def suicider(self):
        """ launches self to target if target
            is in range then explodes
        """
        
        #if self has not locked on a target yet
        if self.isFound == False:
            
            #prepare bounds for simplicity later (N,E,S,W)
            self.seekBounds = [self.rect.top-120, self.rect.centerx+130, self.rect.bottom, self.rect.centerx-130]
            
            #point North
            self.setDir(90)

            #get closest target, if >=1 targets in range
            if self.find() == True:

                #not idle anymore
                self.isIdle = False

                #angle to target where self is the origin
                diffy = self.target.rect.centery - self.rect.centery
                diffx = self.target.rect.centerx - self.rect.centerx
                ang = math.atan2(-diffy, diffx) * 180 / math.pi

                #point to target
                self.setDir(ang)

                #move to target
                self.setSpeed( 6 )

                #self has found its target
                self.isFound = True

    def shooter(self, pic, amt, side=0):
        """ point to closest target in range
            every <alarm-divided-by-fps> seconds:
                shoot <amt> <pic> lasers
                precision of lasers is not perfect
        """
        
        #prepare bounds for simplicity later (N,E,S,W)
        self.seekBounds = [0, self.surface.get_width(), self.rect.y, 0]

        #find closest target
        if self.find() == True:

            #not idle
            self.isIdle = False

            # -----  Point to Target:  -----

            #angle to target where self is the origin
            diffy = self.target.rect.centery - self.rect.centery
            diffx = self.target.rect.centerx - self.rect.centerx
            incline = math.atan2(-diffy, diffx) * 180 / math.pi

            #get turning angle where cc-wise is positive
            turn = incline - self.dir

            #angle to set self to later
            ang = self.dir
            
            #if max turning limit reached
            if abs(turn) > 3:
                #check if turn direction is pos or neg
                if turn > 0:
                    ang += 3
                elif turn < 0:
                    ang -= 3

            #if max turning limit NOT reached
            elif abs(turn) < 15:
                #no checking needed since 'turn' is already signed appropriately
                ang += turn

            #point to target
            self.setDir(ang)
            # ------------------------------
            
            #if aiming at the target (vicinity is:  1 >= dir >= -1)
            if abs(ang)+1 >= abs(incline) or abs(ang)-1 <= abs(incline):
                #shoot <amt> lasers with a 3-frame time gap
                for i in range(amt):
                    if self.timer == (i*4):
                        self.timer += 1
                        #shoot 1 <pic> laser of type 'Bullet'
                        bullet = Bullet.Bullet((0,0,0), 4, 8)
                        bullet.convertToPic(pic)
                        self.group.add( bullet )
                        
                        #-- special cases --#
                        c = self.getCenter()
                        if side == 1: #right
                            bullet.setCenterPos(c[0],c[1])
                            bullet.offset(20, 24, self.dir)
                        elif side == 2: #left
                            bullet.setCenterPos(c[0],c[1])
                            bullet.offset(20,-24, self.dir)
                        #-- usual case --#
                        else:
                            bullet.setCenterPos(c[0],c[1])
                            
                        bullet.aim(self.dir, 4)
                        bullet.fire(6)
                        break

        #if none found
        else:

            #become idle
            self.isIdle = True

    def flamer(self):
        """ point to closest target in range
                shoot flames continously until no enemies in range
                precision of flames is not perfect
        """

        #prepare bounds for simplicity later (N,E,S,W)
        self.seekBounds = [self.rect.centery-100, self.rect.centerx+100, self.rect.y, self.rect.centerx-100]

        #find closest target
        if self.find() == True:

            #not idle
            self.isIdle = False

            # -----  Point to Target:  -----

            #angle to target where self is the origin
            diffy = self.target.rect.centery - self.rect.centery
            diffx = self.target.rect.centerx - self.rect.centerx
            incline = math.atan2(-diffy, diffx) * 180 / math.pi

            #get turning angle where cc-wise is positive
            turn = incline - self.dir

            #angle to set self to later
            ang = self.dir
            
            #if max turning limit reached
            if abs(turn) > 3:
                #check if turn direction is pos or neg
                if turn > 0:
                    ang += 3
                elif turn < 0:
                    ang -= 3

            #if max turning limit NOT reached
            elif abs(turn) < 15:
                #no checking needed since 'turn' is already signed appropriately
                ang += turn

            #point to target
            self.setDir(ang)
            # ------------------------------
            
            #if aiming at the target (vicinity is:  1 >= dir >= -1)
            if abs(ang)+1 >= abs(incline) or abs(ang)-1 <= abs(incline):
                #shoot flames
                if self.timer == 0:
                    self.timer += 1

                    #3 flame streams
                    c = self.getCenter()
                    
                    flame = FlameV2.FlameV2(YELLOW, 2, 2, 6, 6)
                    flame.load(self, self.group, 'N')
                    flame.setCenterPos(c[0], c[1])
                    flame.aim(self.dir, 25)
                    flame.fire(2)
                    flame = FlameV2.FlameV2(YELLOW, 2, 2, 6, 6)
                    flame.load(self, self.group, 'N')
                    flame.setCenterPos(c[0], c[1])
                    flame.aim(self.dir, 10)
                    flame.fire(2)
                    flame = FlameV2.FlameV2(YELLOW, 2, 2, 6, 6)
                    flame.load(self, self.group, 'N')
                    flame.setCenterPos(c[0], c[1])
                    flame.aim(self.dir, 5)
                    flame.fire(2)

        #if none found
        else:

            #become idle
            self.isIdle = True


    def launcher(self):
        """ point to closest target in range
                shoot seeking missile every <...> seconds
                precision of missiles is perfect
        """

        #prepare bounds for simplicity later (N,E,S,W)
        self.seekBounds = [0, self.surface.get_width(), self.rect.y, 0]

        #find closest target
        if self.find() == True:

            #not idle
            self.isIdle = False

            # -----  Point to Target:  -----

            #angle to target where self is the origin
            diffy = self.target.rect.centery - self.rect.centery
            diffx = self.target.rect.centerx - self.rect.centerx
            incline = math.atan2(-diffy, diffx) * 180 / math.pi

            #get turning angle where cc-wise is positive
            turn = incline - self.dir

            #angle to set self to later
            ang = self.dir
            
            #if max turning limit reached
            if abs(turn) > 3:
                #check if turn direction is pos or neg
                if turn > 0:
                    ang += 3
                elif turn < 0:
                    ang -= 3

            #if max turning limit NOT reached
            elif abs(turn) < 15:
                #no checking needed since 'turn' is already signed appropriately
                ang += turn

            #point to target
            self.setDir(ang)
            # ------------------------------
            
            #if aiming at the target (vicinity is:  15 >= dir >= -15)
            if abs(ang)+15 >= abs(incline) or abs(ang)-15 <= abs(incline):

                #launch 1 missile
                if self.timer == 0:
                    self.timer += 1
                    missile = MissileV3.MissileV3(self.surface, MISSLE_BASIC, -90)
                    missile.setUpdateGroup( self.group )
                    self.group.add( missile )
                    missile.setCenter(self.rect.center)
                    missile.setDir( self.dir )
                    missile.setSpeed( random.randint(500,800)/100 )
                    missile.seek(self.targetGroup, 5, self.seekBounds)
                    missile.setTrailStrength(0)

        #if none found
        else:

            #become idle
            self.isIdle = True

    def explode(self):
        """ creates a dense bomb that
            explodes immediately
        """
        bomb = Bomb.Bomb(self.surface, BOMB_SMALL)
        bomb.initVars()
        bomb.setCenter(self.rect.center)
        bomb.setUpdateGroup(self.group)
        bomb.setDensity(25)
        bomb.setSmoke(1)
        bomb.setAmt(5)
        self.group.add(bomb)
        bomb.speed = 0

    def loseHealth(self, amt, pop=[]):
        """ loses some health
            explodes if <=0
            removed from a population if <=0
            kill self if <=0
        """
        self.health -= amt
        if self.health <= 0:
            self.explode()
            if len(pop)>0: pop.remove(self)
            self.kill()






if __name__ == "__main__":
    main()
