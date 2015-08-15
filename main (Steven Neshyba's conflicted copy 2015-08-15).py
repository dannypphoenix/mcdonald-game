import pygame, random
from Entities import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def main(leveltoplay=1):
    global cameraX, cameraY
    paused = False
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Mcdonald Game")
    timer = pygame.time.Clock()

    up = down = left = right = running = sneaking = False
    bg = pygame.Surface((32,32))
    bg.convert()
    bg.fill(pygame.Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32); #player.health = -1
    playerstartL = playerstartT = 32
    platforms = []
    enemies = []
    dead_enemies = []
    drones = []
    Master_Lazer.List = []
    healthbars = []

    x = y = 0

    number_of_levels = 7

##    cl = 1
##    while cl <= 5:
##        l = open('levels/level%s.txt' %(str(cl)))
##        linfo = l.read()
##        l.close()
##        levels += eval(linfo)
##        print(eval(linfo))
##        cl += 1

    leveltoplay %= number_of_levels
    l = open('levels/level%s.txt' %(str(leveltoplay+1)))
    level = eval(l.read())
    l.close()
    #level = levels[leveltoplay]
    # build the level
    enemyspeed = 3
    mustdestroy = []
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == 'T':
                t = BounceBlock(x, y, .5)
                platforms.append(t)
                entities.add(t)
            if col == 'M':
                m = BigLogo(x, y)
                platforms.append(m)
                entities.add(m)
                mustdestroy.append(m)
            if col == 'D':
                d = DeathBlock(x, y)
                platforms.append(d)
                entities.add(d)
            if col == 'C':
                c = ContainmentBlock(x, y)
                platforms.append(c)
                entities.add(c)
            if col == 'S':
                s = Enemy(x, y)
                s.speed = enemyspeed; enemyspeed += 1
                entities.add(s)
                enemies.append(s)
                healthbars.append(s.healthbar)
            if col == 'H':
                h = HamburgurDrone(x, y)
                h.targets.append(player)
                entities.add(h)
                drones.append(h)
                healthbars.append(h.healthbar)
            if col == 'B':
                b = TomatobombDrone(x, y)
                b.targets.append(player)
                entities.add(b)
                drones.append(b)
                healthbars.append(b.healthbar)
            if col == 'N':
                n = SniperDrone(x, y)
                n.targets.append(player)
                entities.add(n)
                drones.append(n)
                healthbars.append(n.healthbar)
            if col == 'G':
                g = MachineGunDrone(x, y)
                g.targets.append(player)
                entities.add(g)
                drones.append(g)
                healthbars.append(g.healthbar)
            if col == '*':
                playerstartL = x
                playerstartT = y
                
            x += 32
        y += 32
        x = 0



    lazer_types = (#heat_seaking_lazer,
                   normal_lazer, normal_lazer, normal_lazer, normal_lazer,
                   normal_lazer,
                   )
    current_lazer = lazer_types[0]

    player.rect.left = playerstartL
    player.rect.top  = playerstartT
    camera_to_use = complex_camera


    if leveltoplay == 0:
        pass

    elif leveltoplay == 1:
        pass

    elif leveltoplay == 2:
        pass#camera_to_use = simple_camera

    elif leveltoplay == 3:
        pass

    elif leveltoplay == 4:
        
        lazer_types = (super_lazer,)
    
    elif leveltoplay == 5:
        pass
    
    elif leveltoplay == 6:
        bombers = []
        gunners = []
        
        for i in range(5):
            b = TomatobombDrone((i+9)*32, 32*5)
            #b.targets.append(player)
            #b.health = 1000
            entities.add(b)
            drones.append(b)
            healthbars.append(b.healthbar)
            b.targets = gunners
            bombers.append(b)

        for i in range(0):
            g = MachineGunDrone((i+9)*32, 6*32)
            #g.targets.append(player)
            #g.health = 1000
            entities.add(g)
            drones.append(g)
            healthbars.append(g.healthbar)
            g.targets = bombers
            gunners.append(g)

        

    
    elif leveltoplay == 7:
        lazer_types = (super_lazer,)

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(camera_to_use, total_level_width, total_level_height)
    entities.add(player)
    healthbars.append(player.healthbar)



    # Main Loop

    while 1:


        
        timer.tick(60)
        

        current_lazer = lazer_types[random.randint(0, len(lazer_types)-1)]

        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit("QUIT")

            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:

                if paused:
                    paused = False
                    print('not paused')
                    #break
                elif not paused:
                    paused = True
                    print('paused')
                    
            if e.type == pygame.KEYDOWN:

                
                if e.key == pygame.K_w:
                    up = True
                if e.key == pygame.K_s:
                    down = True
                if e.key == pygame.K_a:
                    left = True
                if e.key == pygame.K_d:
                    right = True
                if e.key == pygame.K_SPACE:
                    running = True
                if e.key == pygame.K_LSHIFT:
                    sneaking = True
                if e.key == pygame.K_UP:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.top,
                                         (0,-1))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_DOWN:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.bottom,
                                         (0,1))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_RIGHT:
                    lazer = current_lazer(player.rect.right,
                                         player.rect.top  + 16,
                                         (1,-1))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_LEFT:
                    lazer = current_lazer(player.rect.left,
                                         player.rect.top  + 16,
                                         (-1,-1))
                    entities.add(lazer)
                    lazer.shooter = player
                    
                if e.key == pygame.K_p:
                    print('xvel:',player.xvel,'yvel:',player.yvel)
                    print('x:',player.rect.left+16,'y:',player.rect.top+16)
                    print('equiped lazer:', current_lazer)
                    print('number of entities:', len(entities))
                    #print('top:',player.rect.top,'left:',player.rect.left)
##                if e.key == pygame.K_s:
##                    player.xvel = player.yvel = 0

                if e.key == pygame.K_y:
                    b = bomb_lazer(player.rect.left, player.rect.top)
                    entities.add(b)
                    b.shooter = player
                    b.explosionradius = 64
                    b.destroyblocks = True

            if e.type == pygame.KEYUP:

                if e.key == pygame.K_w:
                    up = False
                if e.key == pygame.K_s:
                    down = False
                if e.key == pygame.K_d:
                    right = False
                if e.key == pygame.K_a:
                    left = False
                if e.key == pygame.K_SPACE:
                    running = False
                if e.key == pygame.K_LSHIFT:
                    sneaking = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                Mx, My = pygame.mouse.get_pos()
                Mx -= camera.state.left
                My -= camera.state.top
                Px = player.rect.left + 16
                Py = player.rect.top  + 16
                deltaX = Mx - Px
                deltaY = My - Py
                
                denom = (deltaX**2 + deltaY**2)**.5
                deltaX /= denom
##                deltaY /= denom
                time = denom/16#lazer.speed
                yvel = (deltaY - 1/2*Master_Lazer.gravity * time**2)/time

                direction = (deltaX, yvel/16)#lazer.speed)

                lazer = current_lazer(Px,
                                         Py,
                                         direction)
                entities.add(lazer)
                lazer.shooter = player


        if paused:

            for e in entities:
                if camera.onscreen(e):
                    screen.blit(e.image, camera.apply(e))

            pygame.display.flip()
        
            continue

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)#any Entity
        if player.rect.top > 15000 and player.rect.top % 4 == 0:
            print('top:',player.rect.top,'left:',player.rect.left)

        # update player, draw everything else
        player.update(up, down, left, right, running, sneaking,
                      platforms, entities)
        Master_Lazer.update(entities)

        for e in entities:
            if camera.onscreen(e):
                screen.blit(e.image, camera.apply(e))

        for h in healthbars:
            if camera.onscreen(h):
                screen.blit(h.image, camera.apply(h))
        
        current_enemy = 0
        while current_enemy < len(enemies):
            enemy = enemies[current_enemy]
            if enemy.dead:
                entities.remove(enemy)
                enemies.remove(enemy)
                healthbars.remove(enemy.healthbar)
                dead_enemies.append(enemy)
            elif not enemy.dead:
                enemy.update(player, platforms, entities)
                current_enemy += 1

        current_drone = 0
        while current_drone < len(drones):
            drone = drones[current_drone]
            if drone.dead:
                entities.remove(drone)
                drones.remove(drone)
                healthbars.remove(drone.healthbar)
            elif not drone.dead:
                drone.update(platforms, entities)
                current_drone += 1

        current_platform = 0
        while current_platform < len(platforms):
            platform = platforms[current_platform]
            if platform.destroyed:
                entities.remove(platform)
                platforms.remove(platform)
            else:
                current_platform += 1

        current_must = 0
        while current_must < len(mustdestroy):
            p = mustdestroy[current_must]
            if p.destroyed:
                mustdestroy.remove(p)
            else:
                current_must += 1

        # if enemy is dead, do stuff
        current_enemy = 0
        while current_enemy < len(dead_enemies):
            enemy = dead_enemies[current_enemy]
            enemy.timer -= 1
            if enemy.timer <= 0:
                dead_enemies.remove(enemy)
                enemy = Enemy(enemy.spawn[0], enemy.spawn[1])
                entities.add(enemy)
                enemies.append(enemy)
                healthbars.append(enemy.healthbar)
##                enemy.dead = False
##                enemy.health = 100
##                enemy.rect.left = enemy.spawn[0]
##                enemy.rect.right = enemy.spawn[1]
##                enemy.xvel = 0
##                enemy.yvel = 0
##                enemy.timer = enemy.max_timer
##                entities.add(enemy)
##                enemies.append(enemy)
##                dead_enemies.remove(enemy)
            else:
                current_enemy += 1



        pygame.display.flip()

        

        if leveltoplay == 4:
            if mustdestroy == []:
                player.done = True
        
        if player.dead:
            return False
        elif player.done:
            return True

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def onscreen(self, target):
        sl = self.state.left
        st = self.state.top
        sw = self.state.width
        sh = self.state.height
        self.rect = pygame.Rect(-sl, -st, sw, sh)
        if pygame.sprite.collide_rect(self, target):
            return True
        else:
            #print('return False')
            return False

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)
    #return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)



if __name__ == '__main__':
    currentnum = 0
    while 1:
        won = main(currentnum)
        if won:
            currentnum += 1


