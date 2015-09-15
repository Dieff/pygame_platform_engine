import pygame
import sys
from src.utilities import *
from src.update import *
from src.room import *
from src.player import *
from src.loader import *
from src.constants import *
from src.room import *
from src.graphics import *
from src.area import *
import src.globe as globe

pygame.init()

pygame.display.set_caption(WINDOW_CAPTION)

FPS_CLOCK = pygame.time.Clock()
ELAPSED = 10

fps_meter = fps_meter()

#singletons handled here
globe.Loader = Loader()
globe.Loader.LoadAreas(['Default', 'Common'])
globe.State = State()
globe.State.addState('nominal')
globe.Updater = Updater()
globe.Area = Area()
globe.Area.loadArea('test')
globe.Area.changeRoom('bg-test')

Player = Player()
globe.Updater.setPlayer(Player)

Player.spawn((1200,896))

globe.Camera = Camera()
globe.Camera.start(Player)

iDown = False

while True:
    if(ELAPSED > MAX_FRAME_TIME):
        ELAPSED = MAX_FRAME_TIME
    #events = pygame.event.get()
    
    globe.Camera.fillScreen()
 
    globe.Updater.update(ELAPSED)
    globe.Updater.roomCollide()
    globe.Updater.playerCollide()
    globe.Updater.draw()
        
        
    #handles quit events (clicking x in window)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            print('quit attempt')
            pygame.quit()
            sys.exit()
            break

   #debug stuff
    if(pygame.key.get_pressed()[pygame.K_o]):
        print(Player.pos)
    if(pygame.key.get_pressed()[pygame.K_p]):
        input()
    if(pygame.key.get_pressed()[pygame.K_i]):
        if(not(iDown)):
            if(globe.State.hasState('paused')):
                globe.State.removeState('paused')
            else:
                globe.State.addState('paused')
        iDown = True
    else:
        iDown = False
               
    fps_meter.updateByMilli(ELAPSED)
    pygame.display.set_caption(WINDOW_CAPTION + fps_meter.getFPS())
    pygame.display.flip()
    ELAPSED = FPS_CLOCK.tick(FPS_CAP)