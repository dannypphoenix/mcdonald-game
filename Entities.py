import pygame, random
#from pygame import *


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Character(Entity):
    def __init__(self, x, y, width, height, img):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.distancelimitx = self.distancelimity = 10**1000000
        self.onGround = False
        self.image = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, width, height)
        self.dead = False
        self.health = 100
        self.healthbar = HealthBar(self)
        self.power = 1
        self.done = False
        self.speed = 4
        self.friction = .5
        self.gravity = .3
        self.regen = .1

    def update(self, platforms):
    
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += self.gravity
            # max falling speed
            #if self.yvel > 100: self.yvel = 100
            
##            if self.rect.top >= 100000:
##                self.rect.top = -100
##                self.yvel = 0
##                #print('teleporting')
            
##        if not(left or right):
##            self.xvel = 0
            
        if abs(self.xvel) < .001:
            self.xvel = 0.0

        if self.health <= 0 or \
           abs(self.rect.left) >= self.distancelimitx or\
           abs(self.rect.top ) >= self.distancelimity:
            self.dead = True
            #print('die!')

        if self.xvel != 0.: # only slow down if moving
            self.xvel *= self.friction
            #print ('xvel',self.xvel)
            #self.xvel -= self.xvel*.4
            


        platforms = self.getCloseEntities(platforms)



            
        # increment in x direction
        self.rect.left += int(round(self.xvel))
        
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        
        # increment in y direction
        self.rect.top += self.yvel
        
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

        if self.health < 100 and self.health != -1: self.health += self.regen
        self.healthbar.update()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            
            if pygame.sprite.collide_rect(self, p):

                
                if isinstance(p, ExitBlock):
                    self.done = True
                    
                if isinstance(p, BounceBlock):
                    
                    if yvel != 0:
                        self.yvel = -self.yvel
                    if xvel != 0:
                        self.xvel = -self.xvel
                        
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                    elif yvel > 0:
                        self.rect.bottom = p.rect.top
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        #print('in Bounce')
                    elif xvel > 0:
                        self.rect.right = p.rect.left
                        #print('in Bounce')
                    continue

                if isinstance(p, DeathBlock):
                    if not self.health == -1:
                        self.dead = True
                        #print('die0')

                if isinstance(p, ZoomBlock):
                    #print('to zoom or not to zoom.',self.xvel,self.yvel)
##                    if (self.rect.left >= p.rect.right and \
##                        self.xvel > 0) or \
##                       (self.rect.right <= p.rect.left and \
##                        self.xvel < 0):
                    if xvel == 0 and yvel != 0:
                        
                        self.xvel *= 10
                        #print('speed up x. ZOOOOOM')
                        
##                    if (self.rect.top >= p.rect.bottom and \
##                        self.yvel > 0) or \
##                       (self.rect.bottom <= p.rect.top and \
##                        self.yvel < 0):
                    if yvel == 0 and xvel != 0:
                        
                        self.yvel *= 10
                        #print('speed up y. ZOOOOOM')
                
                if xvel > 0:
                    self.rect.right = p.rect.left
                    #print("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    #print("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.yvel = 0
                    self.rect.top = p.rect.bottom


    def getCloseEntities(self, platforms):
        closeplatforms = []
        for p in platforms:
            px = p.rect.centerx
            py = p.rect.centery
            sx = self.rect.centerx
            sy = self.rect.centery

##            if abs(px-sx) <= abs(self.xvel*2) and \
##               abs(py-sy) <= abs(self.yvel*2):
            if abs(px-sx) <= abs(self.xvel)+100 and abs(py-sy) <= abs(self.yvel)+100:
                closeplatforms.append(p)
##                if isinstance(self, Player):
##                    print((self.xvel + self.yvel)*10)
##                    print(((px-sx)**2+(py-sy)**2)**.5)
##            print(((px-sx)**2+(py-sy)**2)**.5)

        return closeplatforms


class Player(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, 32, 32, 'pictures/playerTest.gif')
####        self.image = pygame.Surface((32,32))
####        self.image.fill(pygame.Color("#0000FF"))
####        self.image.convert()
        self.speed = 4
        self.jetpack = False
        self.friction = .7
        self.running_speed = 3.3#11#7.7
        self.walking_speed = 2.1#7#4.9
        self.sneaking_speed= .4#1#0.7
        self.continuousshoot = None
        self.shoottimer = 0
        self.shootrate = 5

    def update(self, up, down, left, right, running, sneaking,
               platforms, entities):

        #print('in update ...', up, down, left, right)
        
        if up:
            # only jump if on the ground
            if self.onGround and not self.jetpack: self.yvel -= 10
            elif self.jetpack:
                self.yvel -= 1
                lazer = normal_lazer(self.rect.left + 16,
                                     self.rect.bottom,
                                     (0,1))
                entities.add(lazer)
                lazer.shooter = self
        if down:
            if self.jetpack:
                self.yvel += 1
                lazer = normal_lazer(self.rect.left + 16,
                                     self.rect.top,
                                     (0,-1))
                entities.add(lazer)
                lazer.shooter = self
        if running:
            self.speed = self.running_speed
        elif sneaking:
            self.speed = self.sneaking_speed
        else:
            self.speed = self.walking_speed
        if left:
            if not self.jetpack:
                self.xvel -= self.speed
            else:
                self.xvel -= 2
                lazer = normal_lazer(self.rect.right,
                                     self.rect.top + 16,
                                     (1,0))
                entities.add(lazer)
                lazer.shooter = self
        if right:
            if not self.jetpack:
                self.xvel += self.speed
            else:
                self.xvel += 2
                lazer = normal_lazer(self.rect.left,
                                     self.rect.top + 16,
                                     (-1,0))
                entities.add(lazer)
                lazer.shooter = self


        if self.continuousshoot != None:

            if self.shoottimer <= 0:
                self.shoottimer = self.shootrate
                
                lazer = self.continuousshoot(self.rect.left+16,
                                             self.rect.top+16)
                entities.add(lazer)
                lazer.shooter = self

            elif self.shoottimer > 0:
                self.shoottimer -= 1

        Character.update(self, platforms)


        if self.health == -1:
            self.dead = False


class Enemy(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, 32, 64, 'pictures/enemyTest.gif')
        self.spawn = (x, y)
        self.timer = 1000
        self.max_timer = 1000
        self.respawn = True
        
        
    def update(self, player, platforms, entities):

##        self.rect.left += self.xvel
##        self.rect.top  += self.yvel 
        

        if   player.rect.left > self.rect.right:
##            shoot = random.randint(1, 20)
##            if shoot == 1:
##                lazer = normal_lazer(self.rect.left + 16,
##                                         self.rect.top  + 16,
##                                         (player,), (1, 0))

##                entities.add(lazer)
##                lazer.shooter = self
                
            self.xvel = self.speed

        elif player.rect.right < self.rect.left:
##            shoot = random.randint(1, 20)
##            if shoot == 1:
##                lazer = normal_lazer(self.rect.left + 16,
##                                         self.rect.top  + 16,
##                                         (player,), (-1,0))
##                entities.add(lazer)
##                lazer.shooter = self

            
            self.xvel = -self.speed

##        if   player.rect.top > self.rect.bottom:

##            self.yvel = 4

        if player.rect.bottom < self.rect.top:
##            shoot = random.randint(1, 20)
##            if shoot == 1:

##                lazer = normal_lazer(self.rect.left + 16,
##                                         self.rect.top  + 16,
##                                         (player,), (0,-1))
##                entities.add(lazer)
##                lazer.shooter = self

            
            if self.onGround: self.yvel -= 10

##        elif player.rect.top > self.rect.bottom:
##            shoot = random.randint(1, 20)
##            if shoot == 1:
##                lazer = normal_lazer(self.rect.left + 16,
##                                         self.rect.top  + 16,
##                                         (player,), (0,1))
##                entities.add(lazer)
##                lazer.shooter = self



                
        shoot = random.randint(1, 20)
        if shoot == 1:
            Tx = player.rect.left + 16
            Ty = player.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy

            denom = (deltaX**2 + deltaY**2)**.5

            if deltaX == 0: deltaX = .1
            deltaX /= denom
            time = denom/16
            yvel_lazer = (deltaY - 1/2*Master_Lazer.gravity * time**2)/time

            direction = (deltaX, yvel_lazer/16)

            lazer = normal_lazer(Sx, Sy, direction)

            entities.add(lazer)
            lazer.shooter = self

        Character.update(self, platforms)

        if pygame.sprite.collide_rect(self, player):

            if not player.dead:
                if player.health != -1:
                    player.health -= self.power
                    player.health = max((player.health, 0))
                if player.health == 0: player.dead = True
            else:
                player.dead = True
##                print('killed')


class HamburgurDrone(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, 32, 32, 'pictures/BounceTest1.gif')
        self.spawn = (x, y)
        self.timer = 0
        self.max_timer = 0
        self.speed = .4
        self.friction = .9
        self.destroyed = False
        self.targets = []
    def update(self, platforms, entities):
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.dead == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self, platforms)
            return

            
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:           
            self.yvel -= self.speed



        shoot = random.randint(1, 20)
        if shoot == 1:
            Tx = target.rect.left + 16
            Ty = target.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy

            denom = (deltaX**2 + deltaY**2)**.5
            if denom == 0: denom = 1
            deltaX /= denom
            time = denom/16
            yvel_lazer = (deltaY - 1/2*Master_Lazer.gravity * time**2)/time

            direction = (deltaX, yvel_lazer/16)

            lazer = normal_lazer(Sx, Sy, direction)

            entities.add(lazer)
            lazer.shooter = self

        Character.update(self, platforms)
        



class TomatobombDrone(HamburgurDrone):
    def __init__(self, x, y):
        HamburgurDrone.__init__(self, x, y)
        self.shoot = 0
        
    def update(self, platforms, entities):
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.dead == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-2,1)
            Character.update(self, platforms)
            for e in entities:
                if pygame.sprite.collide_rect(self, e):
                    if isinstance(e, normal_lazer):
                        if e.shooter not in self.targets:
                            self.targets.append(e.shooter)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom-160 <= self.rect.y:
            self.yvel -= self.speed*3#/distanceY/2

        self.shoot += 1
        self.shoot %= 10
        for t in self.targets:
            if abs(self.rect.x-t.rect.x)<32 and self.shoot == 0:
                lazer = bomb_lazer(self.rect.left, self.rect.top)

                entities.add(lazer)
                lazer.shooter = self

        Character.update(self, platforms)

        for e in entities:
            if pygame.sprite.collide_rect(self, e):
                if isinstance(e, normal_lazer) and \
                   not isinstance(e, bomb_lazer):
                    if e.shooter not in self.targets:
                        self.targets.append(e.shooter)

class SniperDrone(HamburgurDrone):
    def __init__(self, x, y):
        HamburgurDrone.__init__(self, x, y)
        self.distance = 320
        
    def update(self, platforms, entities):
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.dead == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self, platforms)
            return

        shoot = random.randint(1, 100)
        if shoot == 1:
            Tx = target.rect.left + 16
            Ty = target.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy

            denom = (deltaX**2 + deltaY**2)**.5
            time = denom/16
            yvel_lazer = (deltaY - 1/2*Master_Lazer.gravity * time**2)
            if denom == 0: denom = 1
            deltaX /= denom
            if time == 0: time = 1
            yvel_lazer /= time

            direction = (deltaX, yvel_lazer/16)

            lazer = normal_lazer(Sx, Sy, direction)

            entities.add(lazer)
            lazer.shooter = self
            lazer.dissipation = 0
            lazer.damage = 100

        Character.update(self, platforms)


class MachineGunDrone(HamburgurDrone):
    def __init__(self, x, y):
        HamburgurDrone.__init__(self, x, y)
    def update(self, platforms, entities):
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.dead == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self, platforms)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:
            self.yvel -= self.speed*3

        Tx = target.rect.left + 16
        Ty = target.rect.top  + 16
        Sx = self.rect.left   + 16
        Sy = self.rect.top    + 16
        deltaX = Tx - Sx
        deltaY = Ty - Sy

        denom = (deltaX**2 + deltaY**2)**.5
        time = denom/16
        yvel_lazer = (deltaY - 1/2*Master_Lazer.gravity * time**2)
        if denom == 0: denom = 1
        deltaX /= denom
        if time == 0: time = 1
        yvel_lazer /= time

        direction = (deltaX, yvel_lazer/16)

        lazer = normal_lazer(Sx, Sy, direction)

        entities.add(lazer)
        lazer.shooter = self

        Character.update(self, platforms)






class BlockHider(HamburgurDrone):
    def __init__(self, x, y):
        HamburgurDrone.__init__(self, x, y)
        self.image = pygame.image.load('pictures/BlockTest0.gif')
        self.health = 100
    def update(self, platforms, entities):
        #print(self.dead)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.dead == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self, platforms)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:
            self.yvel -= self.speed*3


        for i in range(6):

            

            Tx = target.rect.left + 16 + random.randint(-20,20)
            Ty = target.rect.top  + 16 + random.randint(-20,20)
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy

            denom = (deltaX**2 + deltaY**2)**.5
            time = denom/16
            yvel_lazer = (deltaY - 1/2*Master_Lazer.gravity * time**2)
            if denom == 0: denom = 1
            deltaX /= denom
            if time == 0: time = 1
            yvel_lazer /= time

            #print(deltaX*100, deltaY)

            direction = (deltaX,
                         yvel_lazer/16)
            #direction = (deltaX, yvel_lazer/16)

            lazer = WaterLazer(Sx, Sy, direction)

            entities.add(lazer)
            lazer.shooter = self

            #print(lazer.xvel)

        #print(self.dead)
        Character.update(self, platforms)
        #print(self.dead)








class Master_Lazer(Entity):
    List = []
    gravity = 1.1
    friction = 1
    MaxLen = 100
    ReflectChance = 4
    
    @staticmethod
    def update(Entities):

        if len(Master_Lazer.List) > Master_Lazer.MaxLen:
            for lazer in Master_Lazer.List[:-Master_Lazer.MaxLen]:
                lazer.destroyed = True

        for lazer in Master_Lazer.List:

##            lazer.xvel = lazer.direction[0]*lazer.speed
##            lazer.yvel = lazer.direction[1]*lazer.speed
            
            lazer.update(Entities)
            


class normal_lazer(Master_Lazer):

    def __init__(self, x, y, direction=(1,0)):
        Entity.__init__(self)
        self.speed = 16
        self.damage = 10
        self.dissipation = .1
        width = height = 1
        if direction[0]!=0: width =5
        if direction[1]!=0: height=5
        #elif direction[1] == 0: direction = (direction[0], -1)
        self.xvel = direction[0]*self.speed
        self.yvel = direction[1]*self.speed
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill(pygame.Color("#ffd700"))
        self.rect = pygame.Rect(x, y, width, height)
        self.shooter = None
        self.destroyed = False
        self.direction = direction

        Master_Lazer.List.append(self)

    def update(self, Entities):
        if self.damage > 0: self.damage -= self.dissipation
        if self.damage < 0: self.damage = 0
        
        # accelerate with gravity
        self.yvel += Master_Lazer.gravity
        # max falling speed
        if self.yvel > 100: self.yvel = 100

        # deaccelerate with friction
        self.xvel *= Master_Lazer.friction
        self.yvel *= Master_Lazer.friction
        
        
        self.rect.left += round(self.xvel)
        self.rect.top  += round(self.yvel)

        self.collision(Entities)
##        current_tar = 0
##        while current_tar < len(self.targets):
##            if self.targets[current_tar].dead:
##                self.targets.remove(self.targets[current_tar])
##            else: current_tar += 1

        if self.destroyed == True:
            Master_Lazer.List.remove(self)
            Entities.remove(self)

        
    def collision(self, Entities):

        for e in Entities:
            
            if pygame.sprite.collide_rect(self, e):

                if isinstance(e, BounceBlock):
                    self.xvel *= -1
                    self.yvel *= -1
                    if random.randint(0, Master_Lazer.ReflectChance) == 0:
                        self.destroyed = True

                elif isinstance(e, DeathBlock):
                    self.destroyed = True

                elif e != self.shooter and not e == self:
                    #print(e, self.shooter)
                    if not (isinstance(e, ContainmentBlock) or \
                       isinstance(e, HealthBar)):
                        self.destroyed = True
##                    Master_Lazer.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
                    if isinstance(e, bomb_lazer):
                        self.destroyed = True
                        e.exploding = True
                        e.img_index += 1
                    elif isinstance(e, super_lazer):
                        self.destroyed = True
                    elif isinstance(e, normal_lazer):
                        self.destroyed = True
                        e.destroyed = True
                        
                    if isinstance(e, Character):
                            if e.health == -1:
                                continue

                            e. health -= self.damage
                            if e.health <= 0:
                                e.health = 0
                                Entities.remove(e)

                    return


class heat_seaking_lazer(normal_lazer):
    def __init__(self, x, y, direction=(1,0)):
        normal_lazer.__init__(self, x, y, direction)
        self.targets = []
        self.speed = 1
        self.damage = 10
        self.movetimer = 6
        self.moverate = 1
        self.dissipation = 0

    def update(self, Entities):

        normal_lazer.update(self, Entities)
        if len(self.targets) == 0:
            #print('sigh')
            return

        if self.targets[0].dead == True:
            self.targets.pop(0)
            return

        if self.movetimer > 0: self.movetimer -= 1

        if self.movetimer <= 0:
            self.movetimer = self.moverate

            Ex = self.targets[0].rect.centerx
            Ey = self.targets[0].rect.centery
            Sx = self.rect.centerx
            Sy = self.rect.centery
            deltaX = Ex - Sx
            deltaY = Ey - Sy
            
            denom = (deltaX**2 + deltaY**2)**.5
            if denom == 0: denom = 0.000000000001
            deltaX /= denom
    ##                deltaY /= denom
            time = denom/16#lazer.speed
            yvel = (deltaY - 1/2*Master_Lazer.gravity * time**2)/time

            self.direction = (deltaX, yvel/16)#lazer.speed)
            self.xvel = self.direction[0]*self.speed
            self.yvel = self.direction[1]*self.speed
            #print(self.xvel)
            #print(self.direction)



class super_lazer(normal_lazer):
    def __init__(self, x, y, direction=(1,0)):
        normal_lazer.__init__(self, x, y, direction)
        self.damage = 50
        self.dissipation = 5

    def collision(self, Entities):

        for e in Entities:
            
            if pygame.sprite.collide_rect(self, e):

                if isinstance(e, DeathBlock) or \
                isinstance(e, IndestructibleBlock) or \
                isinstance(e, ExitBlock):
                    self.destroyed = True
                    continue

                if e != self.shooter and not e == self:
                    #print(e, self.shooter)
                    if not (isinstance(e, ContainmentBlock) or\
                            isinstance(e, HealthBar) or\
                            isinstance(e, normal_lazer)):
                        self.destroyed = True
                    e.destroyed = True
##                    Master_Lazer.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
                    if isinstance(e, Character):
                            if e.health == -1:
                                continue

                            e.health -= self.damage
                            if e.health <= 0:
                                e.health = 0
                                e.dead = True

                    return


class floor_destroying_lazer(normal_lazer):
    def __init__(self, x, y):
        super_lazer.__init__(self, x, y, (0, 1))
        
    def collision(self, Entities):
        super_lazer.collision(self, Entities)

class bomb_lazer(normal_lazer):
    def __init__(self, x, y, direction=(0,0)):
        normal_lazer.__init__(self, x, y, (1,1))
        self.image = pygame.image.load('pictures/tomatoTest0.gif')
        self.rect = pygame.Rect(x, y, 32, 32)
        self.direction = (0, 0)
        self.xvel = self.yvel = 0
        self.damage = 40
        self.dissipation = 0
        self.img_index = 0
        self.exploding = False
        self.explosionradius = 32
        self.destroyblocks = False
    def update(self, Entities):
        #print(self.shooter)
        if self.exploding:
            self.img_index += 1
##            self.xvel = 0
##            self.yvel = 0
            if self.img_index >= 21:
                self.destroyed = True
                self.img_index  %= 15
        self.image = pygame.image.load('pictures/tomatoTest%s.gif'
                                       % (str(self.img_index)))
        #self.damage = self.yvel + 40
        
        normal_lazer.update(self, Entities)

    def collision(self, Entities):

        for e in Entities:
            
            if pygame.sprite.collide_rect(self, e):

                if isinstance(e, BounceBlock):
                    if self.xvel != 0: self.xvel *= -1
                    if self.yvel != 0: self.yvel *= -1
                    if random.randint(0, Master_Lazer.ReflectChance) == 0:
                        self.destroyed = True

                elif isinstance(e, DeathBlock):
                    self.destroyed = True

                elif isinstance(e, Platform) and not\
                     isinstance(e, ContainmentBlock):
                    if self.yvel > 0:
                        self.rect.bottom = e.rect.top
                        self.yvel = 0
                    if self.yvel < 0:
                        self.yvel = 0
                        self.rect.top = e.rect.bottom
                
                elif e != self.shooter and e != self:
                    if isinstance(e, bomb_lazer):
                        e.exploding = True
                        self.destroyed = True
                    elif isinstance(e, normal_lazer):
                        self.exploding = True
                        e.destroyed = True
                    elif not (isinstance(e, ContainmentBlock) or \
                       isinstance(e, HealthBar)):
                        self.exploding = True
                        
            if self.exploding and \
               ((self.rect.left-e.rect.left)**2+\
                (self.rect.top-e.rect.top)**2)**.5\
                < self.explosionradius:
                
                if isinstance(e, DeathBlock) or \
                   isinstance(e, IndestructibleBlock) or \
                   isinstance(e, ExitBlock):
                    
                    self.destroyed = True
                    continue
                
                elif isinstance(e, Character):
                    #print(e, self.shooter, e == self.shooter)
                    if e.health == -1:
                        continue

                    e. health -= self.damage
                    if e.health <= 0:
                        e.health = 0
                        Entities.remove(e)
                        
                elif isinstance(e, Platform):
                    if self.destroyblocks:
                        e.destroyed = True

                elif isinstance(e, bomb_lazer):
                    e.exploding = True
                    
                elif isinstance(e, normal_lazer):
                    e.destroyed = True




class WaterLazer(normal_lazer):
    def __init__(self, x, y, direction=(1,0)):
        normal_lazer.__init__(self, x, y, direction)
        width = 20; height = 20
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill(pygame.Color("#ff000000"))
        self.speed = 1
        self.damage = .5
        self.dissipation = 0


    def collision(self, Entities):

        for e in Entities:
            
            if pygame.sprite.collide_rect(self, e):

                if isinstance(e, BounceBlock):
                    self.xvel *= -1
                    self.yvel *= -1
                    if random.randint(0, Master_Lazer.ReflectChance) == 0:
                        self.destroyed = True

                elif isinstance(e, DeathBlock):
                    self.destroyed = True

                elif e != self.shooter and not e == self:
                    #print(e, self.shooter)
                    if not (isinstance(e, ContainmentBlock) or \
                       isinstance(e, HealthBar)):
                        self.destroyed = True
##                    Master_Lazer.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
                    if isinstance(e, bomb_lazer):
                        self.destroyed = True
                        e.exploding = True
                        e.img_index += 1
                    elif isinstance(e, super_lazer):
                        self.destroyed = True
                    elif isinstance(e, normal_lazer) and not \
                         isinstance(e, WaterLazer):
                        self.destroyed = True
                        e.destroyed = True
                        
                    if isinstance(e, Character):
                            if e.health == -1:
                                continue

                            e. health -= self.damage
                            if e.health <= 0:
                                e.health = 0
                                Entities.remove(e)

                    return

                    
    



class HealthBar(Entity):
    def __init__(self, target):
        Entity.__init__(self)
        font = pygame.font.SysFont('monospace', 20)
        self.image = font.render(str(int(target.health)),
                                 False, (255, 255, 255))
        self.target = target
        self.rect = pygame.Rect(0, 0, 32, 32)
        
    def update(self):
        self.rect.left    = self.target.rect.left
        self.rect.bottom  = self.target.rect.top
        font = pygame.font.SysFont('monospace', 20)
        self.image = font.render(str(int(self.target.health)),
                                 False, (255, 255, 255))

class Scentence(Entity):
    def __init__(self, message, color=(0,0,0)):
        Entity.__init__(self)
        font = pygame.font.SysFont('monospace', 20)
        self.image = (font.render(message), False, color)
        self.target = target
        self.rect = pygame.Rect(0, 0, 32, 32)
        
    def update(self):
        pass
    


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.destroyed = False
        self.image = pygame.image.load('pictures/wallTest.gif')
##        self.image = pygame.Surface((32, 32))
##        self.image.convert()
##        self.image.fill(pygame.Color("#DDDDDD"))
        self.rect = pygame.Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('pictures/ExitBlockTest1.gif')


class BounceBlock(Platform):
    def __init__(self, x, y, bounciness):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('pictures/BounceTest1.gif')
        self.reflect = bounciness

class BigLogo(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(pygame.Color("#ffff00"))

class DeathBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(pygame.Color("#000000"))

class IndestructibleBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)

class ContainmentBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        #self.image.fill(pygame.Color("#0000f0"))
        self.image.fill((255, 255, 255))

class LetterBlock(Platform):
    def __init__(self, x, y, letter):
        Platform.__init__(self, x, y)
        font = pygame.font.SysFont('monospace', 20)
        self.image = font.render(letter,
                                 False, (100, 100, 100))
        
class SpawnerBlock(Platform):
    pass

class DistanceSpawnerBlock(SpawnerBlock):
    def __init__(self,x,y,entities,target):
        self.entities = entities
        Platform.__init__(self,x,y)
        self.target = target
        self.range = 100
    def update(self):
        deltaX = self.target.rect.x - self.rect.x
        deltaY = self.target.rect.y - self.rect.y
            
        denom = (deltaX**2 + deltaY**2)**.5
        if denom <= self.range: self.destroyed = True


class ZoomBlock(Platform):
    pass

class ShooterBlock(Platform):
    def __init__(self,x,y,entities):
        self.entities = entities
        Platform.__init__(self,x,y)
    def update(self):
        shoot = random.randint(0,10)
        if shoot == 0:
            ##directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(0,0),(-1,1),(1,-1))
            directions = ((0,-1),)
            lazer = normal_lazer(self.rect.left, self.rect.top,
                                 directions[random.randint(0,len(directions)-1)])
            lazer.shooter = self
            self.entities.add(lazer)


class BetterShooterBlock(Platform):
    def __init__(self,x,y,entities,target):
        self.entities = entities
        Platform.__init__(self,x,y)
        self.target = target
        self.range = 200
    def update(self):
        shoot = random.randint(0,20)
        if shoot == 0:
        
            deltaX = self.target.rect.x - self.rect.x
            deltaY = self.target.rect.y - self.rect.y
                
            denom = (deltaX**2 + deltaY**2)**.5
            if denom >= self.range: return
            deltaX /= denom
##                deltaY /= denom
            time = denom/16#lazer.speed
            yvel = (deltaY - 1/2*Master_Lazer.gravity * time**2)/time

            direction = (deltaX, yvel/16)#lazer.speed)
            
            lazer = normal_lazer(self.rect.left, self.rect.top,
                                 direction
                                 )
            lazer.shooter = self
            lazer.damage = 6
            lazer.dissipation = 0.5
            self.entities.add(lazer)

