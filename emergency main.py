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
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = pygame.Surface((32,32))
    bg.convert()
    bg.fill(pygame.Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32); player.health = -1
    platforms = []

    x = y = 0
    levels = ((
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPEEEPPPPPPPPPP",
        "P                    p          TTTTTTTTTTTTT        P             P",
        "P                       P   p                       P              P",
        "P                                                  P               P",
        "P               P  P  P  P  P  PTTTTTTTTTTTTT      P               P",
        "P                                                                  P",
        "P                                                                  P",
        "P                                              PPPP                P",
        "P    P      P                                                      P",
        "P                                                      T           P",
        "P                          P  P                                    P",
        "P                 P   PP                                           P",
        "P                                                                  P",
        "P                                                                  P",
        "P                     PPPPPP                                       P",
        "P                                                                  P",
        "P                                                                  P",
        "P   P  PPP   PP                                                    P",
        "P                                                                  P",
        "P                                       PPPP                       P",
        "P                                      PPPPPP                      P",
        "P                                     PPPPPPPP                     P",
        "P                                    PPPPPPPPPP                    P",
        "P                                   PPPPPPPPPPPP    T              P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        ),
    
              (
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPE   T",
        "P P           P  PPP      P PPT  P",
        "P PP PPPPPPPP P   P  PPPP     P  T",
        "P PP    P   P   P   P     P P T  P",
        "P PP    P P P P PPP   PPP   P P  T",
        "P PP    P P P   P   P     PPP T  P",
        "P TP    P P P P   P   P PPP   P  T",
        "P  PTP    P P   P   P     P PPP  P",
        "PP PPPPPPPP PTP   P   PPP   P    P",
        "TT TTTTTTTT TTTTTTTTTTTTT PPP  PTP",
        "T       T     T         T P      P",
        "T T    T     T          T P      P",
        "T       T     T      T  T P      P",
        "T        T   T      T   T P      P",
        "T                  T    T P P  PPP",
        "T   T               T   T P  TT  P",
        "T       T            T  T P      P",
        "T                   T   T PT     P",
        "T T   T   T T      T    T P      P",
        "T                   T   T P      P",
        "T                    T  T P      P",
        "T    T          T       T P      P",
        "T                       T P      P",
        "T                    T  T P      P",
        "T T                     T P      P",
        "T            T          T P      P",
        "T                       T P P    P",
        "T     T             T   T   P    P",
        "TTTTTTTTTTTTTTTTTTTTTTTTTPPPPTTTTP"
        ),

               (
        '                                                                    T',
        'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
        'P                                P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P                                                                   E',
        'P',
        'P',
        'P',
        'P',
        'P',
        'PPP PP PPPPP  P  P PP P PPP PPPPPP  PPPPP    PP P PP P PPP PPPPP'
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        'P',
        ),
              (
        'PPP',
        '   ',
        '   ',
        'PPP',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
        ' E '
        ),
              (
'                                                                             ',
'                                                                             ',
'                                                                             ',
'                                                                             ',
'                                                                             ',
'                                MM         MM                                ',
'                               M  M       M  M                               ',
'                               M   M     M   M                               ',
'                               M    M   M    M                               ',
'                               M     M M     M                               ',
'                               M      M      M                               ',
'                               M             M                               ',
'                               M             M                               ',
'           PPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPP PPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPP          ',                                                                             
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPP          ',
'           PPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPP PPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPP PPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPP PPPPPPPPPPPPPPPPPPP EE PPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPP PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          ',
'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP'
            ))

    if leveltoplay >= len(levels): leveltoplay %= len(levels)
    level = levels[leveltoplay]
    # build the level
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
            x += 32
        y += 32
        x = 0


    if leveltoplay == 0:
        number_of_enemies = 2
        enemy_locations = ((32, 160),(160, 32))

    elif leveltoplay == 1:
        number_of_enemies = 3
        enemy_locations = ((32, 160), (160, 32), (32*8, 640))

    elif leveltoplay == 2:
        number_of_enemies = 2
        enemy_locations = ((64, 0),(128, 0))

    elif leveltoplay == 3:
        number_of_enemies = 0
        enemy_locations = ()

    elif leveltoplay == 4:
        number_of_enemies = 11
        enemy_locations = ((12*32,30*32),(),(),(),(),(),(),(),(),(),())



    enemies = [0 for i in range(number_of_enemies)]
    for index in range(number_of_enemies):
        enemies[index] = Enemy(enemy_locations[index][0],
                               enemy_locations[index][1])
        enemies[index].speed = index+2
        entities.add(enemies[index])
               

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    lazer_types = (heat_seaking_lazer,
                   normal_lazer, normal_lazer, normal_lazer, normal_lazer,
                   normal_lazer,
                   )
    current_lazer = lazer_types[0]

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
                    break
                elif not paused:
                    paused = True
                    
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
                if e.key == pygame.K_UP:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.top  + 16,
                                         (enemies), (0,-1))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_DOWN:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.top  + 16,
                                         (enemies), (0,1))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_RIGHT:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.top  + 16,
                                         (enemies), (1,0))
                    entities.add(lazer)
                    lazer.shooter = player
                if e.key == pygame.K_LEFT:
                    lazer = current_lazer(player.rect.left + 16,
                                         player.rect.top  + 16,
                                         (enemies), (-1,0))
                    entities.add(lazer)
                    lazer.shooter = player
                    
                if e.key == pygame.K_p:
                    print('xvel:',player.xvel,'yvel:',player.yvel)
                    print(enemy1.rect.center, player.rect.center,
                          player.rect.left+16)
                    lazer = normal_lazer(player.rect.center[0],
                                         player.rect.center[1],
                                         (),
                                         (0, 0))
                    entities.add(lazer)
                    #print('top:',player.rect.top,'left:',player.rect.left)
##                if e.key == pygame.K_s:
##                    player.xvel = player.yvel = 0

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



        if paused:

            for e in entities:
                screen.blit(e.image, camera.apply(e))

            pygame.display.update()
        
            continue

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)#any Entity
        if player.rect.top > 15000 and player.rect.top % 4 == 0:
            print('top:',player.rect.top,'left:',player.rect.left)

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms)
        current_enemy = 0
        while current_enemy < len(enemies):
            enemy = enemies[current_enemy]
            if enemy.dead:
                entities.remove(enemy)
                enemies.remove(enemy)
            elif not enemy.dead:
                enemy.update(player, platforms, entities)
            current_enemy += 1
            
        Master_Lazer.update(entities)
        
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        
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

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

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

