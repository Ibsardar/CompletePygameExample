""" Player.py
    by Ibrahim Sardar
"""

#general housekeeping
import pygame, math, random
from Block import Block
from Bullet import Bullet
from FlameV2 import FlameV2
from MissileV3 import MissileV3
from Bomb import Bomb
from Minion import Minion
pygame.init()
#window
WINDOWWIDTH  = 720
WINDOWHEIGHT = 380
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)
DGREY  = ( 91,  91,  91)
DDGREY = ( 34,  34,  34)
GREEN  = (  0, 255,   0)
PINK   = (255, 183, 234)
RED    = (255,   0,   0)
ORANGE = (255, 128,   0)
DDBLUE = ( 22,  22,  57)
DBLUE  = (  3,   3,  92)
BLUE   = (  0,   0, 255)
LBLUE  = ( 20, 218, 240)
LLBLUE = (188, 226, 230)
BROWN  = (102,  51,   0)
PURPLE = (102,   0, 102)
YELLOW = (255, 255,   0)
FIRE   = (193, 105,  16)
#pictures
BULLET_LGREY = "Graphics\Bullet01.png"
BULLET_GREY  = "Graphics\Bullet02.png"
BULLET_DGREY = "Graphics\Bullet03.png"
BULLET_RED   = "Graphics\Bullet04.png"
BULLET_GREEN = "Graphics\Bullet05.png"
MISSLE_BASIC = "Graphics\Missile02.png"
MISSLE_HEAVY = "Graphics\Missile01.png"
BOMB_SMALL   = "Graphics\Bomb01.png"
BOMB_REFLECT = "Graphics\Reflector.png"
BOMB_ATTRACT = "Graphics\Attractor.png"
MINION_1     = "Graphics\Minion01.png"
MINION_2     = "Graphics\Minion02.png"
MINION_3     = "Graphics\Minion03.png"
MINION_4     = "Graphics\Minion04.png"
MINION_5     = "Graphics\Minion05.png"
ARMY_1       = "Graphics\ArmyMinion01.png"
ARMY_2       = "Graphics\ArmyMinion02.png"
ARMY_3       = "Graphics\ArmyMinion03.png"

#Player
class Player(Block):
    #initializer
    def __init__(self, color=BLACK, w=0, h=0):
        pygame.sprite.Sprite.__init__(self)
        #attributes
        self.setImage(w, h)
        self.color = color
        self.isPic = False
        self.health = 100

        self.baddies = None
        self.bullets = None

        self.event1 = False
        self.xspeed = 0
        self.yspeed = 0

        self.event2 = False
        self.event3 = False
        self.event4 = False
        self.event5 = False
        self.timer  = 0 
        self.alarm  = 0

        self.currMinion = None
        self.pop1 = []
        self.pop2 = []
        self.pop3 = []

        #The player's choice of weapons... (5 choices each w/ 3 upgrades each)
        #[ shooter, missile, sprayer, minions, bombs ]
        #the following are not entirely precise
        """ shooter:    <pts | 0, 175, 300>
                1: shooter
                2: machine gun
                3: gatling gun
            missile:     <pts | 100, 400, 700>
                1: missile launcher
                2: auto launcher
                3: 1 seeker, 2 normal
            sprayer:    <pts | 150, 350, 900>
                1: shotgun
                2: flame thrower
                3: party blaster
            minions:    <pts | 200, 1000, 2500>
                1: suicide minion
                2: shooter minion
                3: army
            bombs:      <pts | 250, 1500, 5000>
                1: grenade
                2: reflector **then explodes
                3: attractor **then explodes w/ fragments
        """
        self.unlocked = [0,0,0,0,0]
        self.selected = 0
        self.points = 0

    # --- update method --- #
    def update(self):
        if self.isPic == False:
            self.image.fill(self.color)
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.updateEvents()
        #limit shots per frame
        if self.timer != 0:
            if  self.timer < self.alarm:
                self.timer += 1
            else:
                self.timer = 0

    # --- other methods --- #
    def updateEvents(self):
        
        #movement
        if self.event1 == True:
            #stop from leaving window
            #left edge
            if self.rect.left > 0:
                self.rect.x += self.xspeed
            elif self.xspeed < 0:
                self.stopX()
                self.rect.left = 0
            #right edge
            if self.rect.right < WINDOWWIDTH:
                self.rect.x += self.xspeed
            elif self.xspeed > 0:
                self.stopX()
                self.rect.right = WINDOWWIDTH
            #top edge
            if self.rect.top > 0:
                self.rect.y += self.yspeed
            elif self.yspeed < 0:
                self.stopY()
                self.rect.top = 0
            #bottom edge
            if self.rect.bottom < WINDOWHEIGHT:
                self.rect.y += self.yspeed
            elif self.yspeed > 0:
                self.stopY()
                self.rect.bottom = WINDOWHEIGHT
                
        #shooting (lvl 3)
        if self.event2 == True:
            #shoot a bullet
            if self.timer == 0:
                self.timer += 1
                bullet = Bullet(BLACK, 4, 8)
                bullet.convertToPic(BULLET_DGREY, 1)
                bullet.load(self, self.bullets)
                bullet.aim(90, 1)
                bullet.fire(18)

        #sprayer (lvl 2)
        if self.event3 == True:
            if self.timer == 0:
                self.timer += 1
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(90, 30)
                flame.fire(5)
                flame.wiggle = True #--1
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(100, 30)
                flame.fire(5)       #--2
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(80, 30)
                flame.fire(5)       #--3
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(95, 15)
                flame.fire(5)
                flame.wiggle = True #--4
                flame = FlameV2(YELLOW, 6, 6, 24, 24)
                flame.load(self, self.bullets, 'N')
                flame.aim(85, 15)
                flame.fire(5)
                flame.wiggle = True #--5

        #missile (lvl 2)
        if self.event4 == True:
            if self.timer == 0:
                self.timer += 1
                missile = MissileV3(windowSurface, MISSLE_BASIC, -90)
                missile.setUpdateGroup( self.bullets )
                self.bullets.add( missile )
                missile.setCenter(self.rect.center)
                missile.setDir( random.randint(87,93) )
                missile.setSpeed( random.randint(300,500)/100 )
                missile.setTrailStrength(1)

        #sprayer (lvl 3)
        if self.event5 == True:
            if self.timer == 0:
                self.timer += 1
                #shoot 5 different bullets
                side = random.randint(8,10)
                bullet = Bullet(DDBLUE, side,side)
                bullet.load(self, self.bullets)
                bullet.aim(90, 5)
                bullet.yaccel = 0.35
                bullet.special_01()
                bullet.fire(random.randint(10,14)) #--1
                side = random.randint(8,10)
                bullet = Bullet(DDBLUE, side,side)
                bullet.load(self, self.bullets)
                bullet.aim(87, 4)
                bullet.yaccel = 0.35
                bullet.special_01()
                bullet.fire(random.randint(10,14)) #--2
                side = random.randint(8,10)
                bullet = Bullet(DDBLUE, side,side)
                bullet.load(self, self.bullets)
                bullet.aim(83, 3)
                bullet.yaccel = 0.35
                bullet.special_01()
                bullet.fire(random.randint(10,14)) #--3
                side = random.randint(8,10)
                bullet = Bullet(DDBLUE, side,side)
                bullet.load(self, self.bullets)
                bullet.aim(93, 4)
                bullet.yaccel = 0.35
                bullet.special_01()
                bullet.fire(random.randint(10,14)) #--4
                side = random.randint(8,10)
                bullet = Bullet(DDBLUE, side,side)
                bullet.load(self, self.bullets)
                bullet.aim(97, 3)
                bullet.yaccel = 0.35
                bullet.special_01()
                bullet.fire(random.randint(10,14)) #--5

        #update target group for current minion
        if self.currMinion == None and self.baddies != None:
            self.currMinion.setTargetGroup(self.baddies)
                
                
    # --- END UPDATING EVENTS --- #
    
    

    #shoots depending on selected weapon
    #returns  0 if success
    #returns -1 if warning
    #returns -2 if error
    def shoot(self, bullets, baddies, fps):
        
        #    fyi...
        # Assuming fps=60 for comments mentioning
        # how long the alarm is set for.
        
        #shooter
        if self.selected == 0:
            
            #locked
            if self.unlocked[0] == 0:
                print("Warning: shooter is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[0] == 1:
                #allow a shot every 1/4 sec
                self.alarm = int(fps/4)
                #shoot a bullet
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DGREY, 4, 8)
                    bullet.convertToPic(BULLET_LGREY, 1)
                    bullet.load(self, bullets)
                    bullet.aim(90, 5)
                    bullet.fire(6)

            #lvl 2
            elif self.unlocked[0] == 2:
                #allow a shot every 1/fps sec
                self.alarm = 1
                #shoot a bullet
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DDGREY, 4, 8)
                    bullet.convertToPic(BULLET_GREY, 1)
                    bullet.load(self, bullets)
                    bullet.aim(90, 10)
                    bullet.fire(10)

            #lvl 3
            elif self.unlocked[0] == 3:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/30 sec
                self.alarm = int(fps/30)
                #allow holding down to keep shooting
                self.event2 = True

            else:
                print("Error: player is trying to shoot with an incorrect upgrade selection")
                return -2
            
        #missile
        elif self.selected == 1:
            
            #locked
            if self.unlocked[1] == 0:
                print("Warning: missile is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[1] == 1:
                #allow a shot every 1 sec
                self.alarm = int(fps)
                #shoot a missile
                if self.timer == 0:
                    self.timer += 1
                    missile = MissileV3(windowSurface, MISSLE_BASIC, -90)
                    missile.setUpdateGroup( bullets )
                    bullets.add( missile )
                    missile.setCenter(self.rect.center)
                    missile.setDir( random.randint(87,93) )
                    missile.setSpeed( random.randint(300,500)/100 )
                    missile.setTrailStrength(1)
                    
            #lvl 2
            elif self.unlocked[1] == 2:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/2 sec
                self.alarm = int(fps/2)
                #allow holding down to keep launching
                self.event4 = True

            #lvl 3
            elif self.unlocked[1] == 3:
                #allow a small missile every 1 sec
                self.alarm = int(fps*1)

                #25% chance for a large missile
                # ...
                #shoot 3 missiles
                if self.timer == 0:
                    self.timer += 1

                    #seeking bounds
                    bounds = [0,WINDOWWIDTH,self.rect.y,0]

                    special = random.randint(1,4)
                    if special == 1:
                        # 1 big seek missile
                        missile = MissileV3(windowSurface, MISSLE_HEAVY, -90)
                        missile.setUpdateGroup( bullets )
                        bullets.add( missile )
                        missile.setCenter(self.rect.center)
                        missile.setDir( 90 )
                        missile.setSpeed( random.randint(200,400)/100 )
                        missile.seek(baddies, 2, bounds)
                        missile.setTrailStrength(2)

                    # 2 small seek missiles
                    missile = MissileV3(windowSurface, MISSLE_BASIC, -90)
                    missile.setUpdateGroup( bullets )
                    bullets.add( missile )
                    missile.setCenter(self.rect.center)
                    missile.setDir( random.randint(82,88) )
                    missile.setSpeed( random.randint(400,600)/100 )
                    missile.seek(baddies, 5, bounds)
                    missile.setTrailStrength(0)
                    
                    missile = MissileV3(windowSurface, MISSLE_BASIC, -90)
                    missile.setUpdateGroup( bullets )
                    bullets.add( missile )
                    missile.setCenter(self.rect.center)
                    missile.setDir( random.randint(92,98) )
                    missile.setSpeed( random.randint(400,600)/100 )
                    missile.seek(baddies, 5, bounds)
                    missile.setTrailStrength(0)

            else:
                print("Error: player is trying to shoot with an incorrect upgrade selection")
                return -2
            
        #sprayer
        elif self.selected == 2:

            #locked
            if self.unlocked[2] == 0:
                print("Warning: sprayer is not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[2] == 1:
                #allow a shot every 1 sec
                self.alarm = int(fps)
                #shoot 3 bullets, 4 fragments
                if self.timer == 0:
                    self.timer += 1
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(90, 4)
                    bullet.fire(16) #--1
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(95, 6)
                    bullet.fire(15) #--2
                    bullet = Bullet(DDGREY, 7, 7)
                    bullet.load(self, bullets)
                    bullet.aim(85, 6)
                    bullet.fire(15) #--3

            #lvl 2
            elif self.unlocked[2] == 2:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/10 sec
                self.alarm = int(fps/10)
                #allow holding down to keep shooting
                self.event5 = True

            #lvl 3
            elif self.unlocked[2] == 3:
                #update bullet group for self
                self.bullets = bullets
                #allow a shot every 1/15 sec
                self.alarm = int(fps/15)
                #allow holding down to keep shooting
                self.event3 = True

            else:
                print("Error: player is trying to shoot with an incorrect upgrade selection")
                return -2
            
        #minions
        elif self.selected == 3:
            
            #locked
            if self.unlocked[3] == 0:
                print("Warning: minions are not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[3] == 1:
                #allow a shot every 0.5 sec
                self.alarm = int(fps/2)
                    
                #create a random suicide minion
                if self.timer == 0:
                    self.timer += 1
                    suiciders = [MINION_1,MINION_2,MINION_3]
                    minion = Minion(windowSurface, random.choice(suiciders), -90)
                    minion.init()

                    #place minion randomly in front of self
                    # N,E,S,W
                    bounds = [self.rect.centery-80,self.rect.centerx+50,self.rect.y-10,self.rect.centerx-50]
                    cx = random.randint(bounds[3],bounds[1])
                    cy = random.randint(bounds[0],bounds[2])
                    minion.setCenter( (cx,cy) )
                    
                    #set type, update group, target group
                    minion.type = 1
                    minion.setUpdateGroup(bullets)
                    minion.setTargetGroup(baddies)

                    #load minion into update group
                    bullets.add(minion)

                    #set current minion
                    self.currMinion = minion

            #lvl 2
            elif self.unlocked[3] == 2:
                #allow a shot every 1/6 sec
                self.alarm = int(fps/6)

                #create a shooter minion
                if self.timer == 0:
                    self.timer += 1

                    #only if fewer than 2 shooter-minions are alive
                    if len(self.pop2) < 2:

                        # bounds: N,E,S,W
                        bounds = [self.rect.centery-35,self.rect.centerx+50,self.rect.y+15,self.rect.centerx-50]
                        cx = random.randint(bounds[3],bounds[1])
                        cy = random.randint(bounds[0],bounds[2])
                        
                        #pick a side this minion will be on (right/left)
                        if cx >= WINDOWWIDTH/2:
                            pic = MINION_4 #right
                            side = 1
                        else:
                            pic = MINION_5 #left
                            side = 2

                        #create a shooter minion
                        minion = Minion(windowSurface, pic, -90)
                        minion.init()
                        minion.side = side

                        #place minion randomly in front of self
                        minion.setCenter( (cx,cy) )
                        
                        #set type, alarm, update group, target group
                        minion.type = 2
                        minion.alarm = 60*2
                        minion.setUpdateGroup(bullets)
                        minion.setTargetGroup(baddies)

                        #load minion into update group, pop2
                        bullets.add(minion)
                        self.pop2.append(minion)

                        #set current minion
                        self.currMinion = minion

            #lvl 3
            elif self.unlocked[3] == 3:
                #allow a shot every 0.25 sec
                self.alarm = int(fps/4)

                #create an army minion
                if self.timer == 0:
                    self.timer += 1

                    #only if fewer than 8 army-minions are alive
                    if len(self.pop3) < 8:

                        #create a random army minion
                        armies = { 1 : ARMY_1,   #flames
                                   2 : ARMY_2,   #missiles
                                   3 : ARMY_3 }  #lasers
                        choice = random.randint(1,3)
                        minion = Minion(windowSurface, armies[choice], -90)
                        minion.init()

                        # bounds: N,E,S,W
                        bounds = [self.rect.centery-35,self.rect.centerx+50,self.rect.y+15,self.rect.centerx-50]
                        cx = random.randint(bounds[3],bounds[1])
                        cy = random.randint(bounds[0],bounds[2])

                        #place minion randomly in front of self
                        minion.setCenter( (cx,cy) )
                        
                        #set type, health, subtype, alarm, update group, target group, dir
                        minion.type = 3
                        minion.health = 40
                        if choice == 1:
                            minion.alarm = 60/6
                            minion.subtype = "red"
                        elif choice == 2:
                            minion.alarm = 60*2
                            minion.subtype = "blue"
                        elif choice == 3:
                            minion.alarm = 60/3
                            minion.subtype = "green"
                        minion.setUpdateGroup(bullets)
                        minion.setTargetGroup(baddies)
                        minion.setDir(90)

                        #load minion into update group, pop3
                        bullets.add(minion)
                        self.pop3.append(minion)

                        #set current minion
                        self.currMinion = minion

            else:
                print("Error: player is trying to shoot with an incorrect upgrade selection")
                return -2
        
        #bombs (NOTE*** attractor and reflector do not attract/reflect enemies)
        elif self.selected == 4:

            #locked
            if self.unlocked[4] == 0:
                print("Warning: bombs are not unlocked yet")
                return -1
            
            #lvl 1
            elif self.unlocked[4] == 1:
                #allow a shot every 1/2 sec
                self.alarm = int(fps/2)
                #throws 1 bomb
                if self.timer == 0:
                    self.timer += 1
                    bomb = Bomb(windowSurface, BOMB_SMALL)
                    bomb.initVars()
                    bomb.setCenter(self.rect.center)
                    bomb.setUpdateGroup(bullets)
                    bomb.setDensity(15)
                    bomb.setSmoke(5)
                    bomb.setAmt(10)
                    bullets.add(bomb)
                    bomb.dir = random.randint(60, 120)
                    bomb.speed = random.randint(115,190)/10
                    bomb.accel = -random.randint(5,7)/10

            #lvl 2
            elif self.unlocked[4] == 2:
                #allow a shot every 2 sec
                self.alarm = int(fps*2)
                #throws 1 reflector
                if self.timer == 0:
                    self.timer += 1
                    bomb = Bomb(windowSurface, BOMB_REFLECT)
                    bomb.initVars()
                    bomb.setCenter(self.rect.center)
                    bomb.setUpdateGroup(bullets)
                    bullets.add(bomb)
                    bomb.dir = 90
                    bomb.speed = 2
                    bomb.setReflect(0.8)

            #lvl 3
            elif self.unlocked[4] == 3:
                #allow a shot every 4 sec
                self.alarm = int(fps*4)
                #throws 1 attractor
                if self.timer == 0:
                    self.timer += 1

                    #seeking bounds
                    bounds = [0,WINDOWWIDTH,self.rect.y,0]

                    #attractor (also launches missiles)
                    bomb = Bomb(windowSurface, BOMB_ATTRACT)
                    bomb.initVars()
                    bomb.setCenter(self.rect.center)
                    bomb.setUpdateGroup(bullets)
                    bullets.add(bomb)
                    bomb.dir = 90
                    bomb.speed = 2
                    bomb.setAttract(0.7, baddies, bounds)

            else:
                print("Error: player is trying to shoot with an incorrect upgrade selection")
                return -2
            
        #error
        else:
            print("Error: player is trying to shoot with an incorrect weapon selection")
            return -2

        #if all goes well, return 0
        return 0

    def stopShooting(self):
        self.event2 = False
        self.event3 = False
        self.event4 = False
        self.event5 = False
            




#if this is file running, run this main
if __name__ == "__main__":
    main()

