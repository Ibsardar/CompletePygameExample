""" Bomb.py
    By Ibrahim Sardar
"""

#load
import pygame, random, math, MissileV3

from FollowBlock import FollowBlock

from FlameV2 import FlameV2

#init
pygame.init()

#color
YELLOW = (255, 255,   0)

#pics
MISSLE_BASIC = "Graphics\Missile02.png"
BOMB_SMALL   = "Graphics\Bomb01.png"

#Bomb
class Bomb(FollowBlock):

    def initVars(self):
        self.group = None
        self.density = 1
        self.smoke = 0
        self.amt = 0
        self.isReflect = False
        self.isAttract = False
        self.alarm = 0
        self.timer = 0

    def setUpdateGroup(self, group):
        self.group = group

    def setDensity(self, den):
        if den <= 0:
            den = 1
        self.density = den

    def setSmoke(self, lvl):
        self.smoke = lvl

    def setAmt(self, amt):
        self.amt = amt

    def setReflect(self, time):
        self.isReflect = True
        self.isAttract = False
        self.alarm = int(60*time)
        self.timer = 0

    def setAttract(self, time, baddies, bounds):
        self.isReflect = False
        self.isAttract = True
        self.alarm = int(60*time)
        self.timer = 0
        self.targetGroup = baddies
        self.seekBounds = bounds

    #IGNORE THIS FUNCTION
    def reflect(self, group):
        for t in group:
            #repel t from self
            t.moveTowards(self, accel=-0.1)
            
            #if alarm is "ringing"
            if self.timer == self.alarm:

                #10% chance of random explosion
                rnd_explode = random.randint(0,10)
                
                if rnd_explode == 1:
                    
                    #create explosion at t
                    bomb = Bomb(self.surface, BOMB_SMALL)
                    bomb.initVars()
                    bomb.setCenter(self.rect.center)
                    bomb.setUpdateGroup(self.group)
                    bomb.setDensity(20)
                    bomb.setSmoke(1)
                    bomb.setAmt(10)
                    self.group.add(bomb)
                    bomb.speed = 0

    #IGNORE THIS FUNCTION
    def attract(self, group):
        for t in group:
            #attract t to self
            t.moveTowards(self, accel=0.1)

    def updateBoundsCondition(self):
        """ destroy self if leave window+10
        """
        if(self.rect.left   > self.surface.get_width()+10 or
           self.rect.right  < 0-10                        or
           self.rect.bottom < 0-10                        or
           self.rect.top    > self.surface.get_height()+10):

            self.kill()

    def updateMore(self):
        """ update bomb's timer
        """
        
        #increment timer
        if  self.timer < self.alarm:
            self.timer += 1

        #do something based on type
        if self.isReflect:
            #if alarm is "ringing"
            if self.timer == self.alarm:
                
                #reset alarm
                self.timer = 0

                #huge explosion at self
                bomb = Bomb(self.surface, BOMB_SMALL)
                bomb.initVars()
                bomb.setCenter(self.rect.center)
                bomb.setUpdateGroup(self.group)
                bomb.setDensity(5)
                bomb.setSmoke(1)
                bomb.setAmt(20)
                self.group.add(bomb)
                bomb.speed = 0
                
        elif self.isAttract:
            #if alarm is "ringing"
            if self.timer == self.alarm:
                
                #reset alarm
                self.timer = 0

                #launch bunch of missiles
                #this event will have random attributes
                rnd_amt = random.randint(1,4)*4
                cnt = -1
                for m in range( rnd_amt ):
                    cnt += 1
                    rnd_seek = random.randint(0,1)
                    
                    missile = MissileV3.MissileV3(self.surface, MISSLE_BASIC, -90)
                    missile.setUpdateGroup( self.group )
                    self.group.add( missile )
                    missile.setCenter(self.rect.center)

                    #launches for all 4 quadrants
                    corner = (rnd_amt+cnt)%4
                    if corner == 0:
                        missile.setDir( random.randint(0,90) )
                    if corner == 1:
                        missile.setDir( random.randint(90,180) )
                    if corner == 2:
                        missile.setDir( random.randint(180,270) )
                    if corner == 3:
                        missile.setDir( random.randint(270,360) )
                        
                    missile.setSpeed( random.randint(500,800)/100 )
                    
                    if rnd_seek == 1:
                        missile.seek(self.targetGroup, 5, self.seekBounds)
                        
                    missile.setTrailStrength(0)

        else:
            if self.speed <= 0:
                self.speed = 0
                self.explode()
                self.kill()

    def explode(self):
        """ explosion animation using FlameV2
        """
        for i in range(self.amt):
            flame = FlameV2(YELLOW, 8, 8, 18, 18)
            flame.load(self, self.group, 'C')
            flame.aim(0, 360)
            flame.fire(random.randint(1,10)/self.density)
            flame.smokeLevel = self.smoke
            flame.len = 18
        for i in range(self.amt):
            flame = FlameV2(YELLOW, 6, 6, 14, 14)
            flame.load(self, self.group, 'C')
            flame.aim(0, 360)
            flame.fire(random.randint(11,20)/self.density)
            flame.smokeLevel = self.smoke
            flame.len = 20
        for i in range(self.amt):
            flame = FlameV2(YELLOW, 4, 4, 10, 10)
            flame.load(self, self.group, 'C')
            flame.aim(0, 360)
            flame.fire(random.randint(21,30)/self.density)
            flame.smokeLevel = self.smoke
            flame.len = 22
        for i in range(int(self.amt/3)):
            flame = FlameV2(YELLOW, 4, 4, 8, 8)
            flame.load(self, self.group, 'C')
            flame.aim(0, 360)
            flame.fire(3)
            flame.smokeLevel = self.smoke
            flame.len = 23
        
