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
from src.hud import *
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
globe.Hud = Hud()
globe.Area.loadArea('test')

Player = Player()
globe.Camera = Camera()
globe.Camera.start(Player)
globe.Updater.setPlayer(Player)


globe.Area.initialCinematicLoad('starting-point', (32,356))

Player.unRegister()
Player.register()

iDown = False
lDown = False
updateToggle = False
fullScreen = False

while True:
    if(ELAPSED > MAX_FRAME_TIME):
        ELAPSED = MAX_FRAME_TIME
        
    events = pygame.event.get()
    #events = pygame.event.get()
    
    globe.Camera.fillScreen()
 
    globe.Updater.update(ELAPSED)
    globe.Updater.playerCollide()
    globe.Updater.roomCollide()
    globe.Updater.draw()
        
        
    #handles quit events (clicking x in window)
    for event in events:
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
    if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    if(pygame.key.get_pressed()[pygame.K_i]):
        if(not(iDown)):
            if(globe.State.hasState('paused')):
                globe.State.removeState('paused')
            else:
                globe.State.addState('paused')
        iDown = True
    else:
        iDown = False
    if(pygame.key.get_pressed()[pygame.K_l]):
        if(not(lDown)):
            if(fullScreen):
                pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
            else:
                fullScreen = True
                flags = pygame.FULLSCREEN
                pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), flags, 32)
        lDown = True
    else:
        lDown = False
               
    fps_meter.updateByMilli(ELAPSED)
    pygame.display.set_caption(WINDOW_CAPTION + fps_meter.getFPS())
    
    if(updateToggle):
        updateToggle = False
        updateRect = pygame.Rect(0,0,int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2))
    else:
        updateToggle = True
        updateRect = pygame.Rect(int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2),int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2))
    pygame.display.update(updateRect)
    ELAPSED = FPS_CLOCK.tick(FPS_CAP)