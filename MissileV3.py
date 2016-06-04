""" MissileV3.py
    By Ibrahim Sardar
"""

#load
import pygame, random, math

from FollowBlock import FollowBlock

from FlameV2 import FlameV2

from Bomb import Bomb

#init
pygame.init()

#color
YELLOW = (255, 255,   0)

#pics
BOMB_SMALL = "Graphics\Bomb01.png"

#MissileV3
class MissileV3(FollowBlock):

    def setUpdateGroup(self, group):
        self.group = group

    def setTrailStrength(self, stren):
        self.stren = stren

    def updateBoundsCondition(self):
        """ destroy self if leave window+10
        """
        if(self.rect.left   > self.surface.get_width()+10 or
           self.rect.right  < 0-10                        or
           self.rect.bottom < 0-10                        or
           self.rect.top    > self.surface.get_height()+10):

            self.kill()

    def updateMore(self):
        """ update trail
        """
        if self.stren == 2:
            self.heavyTrail()
        elif self.stren == 1:
            self.trail()
        elif self.stren == 0:
            self.weakTrail()

    def trail(self):
        """ creates a trail of fire
            behind self
        """
        flame = FlameV2(YELLOW, 4, 4, 12, 12)
        flame.load(self, self.group, 'C')
        flame.aim(self.dir-180, 5)
        flame.fire(2)
        flame.smokeLevel = 5
        flame.len = 20

    def weakTrail(self):
        """ creates a light trail of fire
            behind self
        """
        flame = FlameV2(YELLOW, 4, 4, 6, 6)
        flame.load(self, self.group, 'C')
        flame.aim(self.dir-180, 3)
        flame.fire(0.3)
        flame.smokeLevel = 0
        flame.len = 50
        flame.noRed = True

    def heavyTrail(self):
        """ creates a heavy trail of fire
            behind self
        """
        flame = FlameV2(YELLOW, 4, 4, 36, 36)
        flame.load(self, self.group, 'C')
        flame.aim(self.dir-180, 16)
        flame.fire(2)
        flame.smokeLevel = 5
        flame.len = 10

    def explode(self):
        """ creates a dense bomb that
            explodes immediately
        """
        bomb = Bomb(self.surface, BOMB_SMALL)
        bomb.initVars()
        bomb.setCenter(self.rect.center)
        bomb.setUpdateGroup(self.group)
        bomb.setDensity(30)
        bomb.setSmoke(25)
        bomb.setAmt(5)
        self.group.add(bomb)
        bomb.speed = 0

    def explodeLarge(self):
        """ creates a large bomb that
            explodes immediately
        """
        bomb = Bomb(self.surface, BOMB_SMALL)
        bomb.initVars()
        bomb.setCenter(self.rect.center)
        bomb.setUpdateGroup(self.group)
        bomb.setDensity(10)
        bomb.setSmoke(25)
        bomb.setAmt(15)
        self.group.add(bomb)
        bomb.speed = 0



