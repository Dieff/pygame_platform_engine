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
globe.Updater = Updater()
globe.Area = Area()
globe.Area.loadArea('test')
globe.Area.changeRoom('bg-test')

Player = Player()
globe.Updater.setPlayer(Player)


Player.spawn((1200,896))

globe.Camera = Camera()
globe.Camera.start(Player)

while True:
    if(ELAPSED > MAX_FRAME_TIME):
        ELAPSED = MAX_FRAME_TIME
    #events = pygame.event.get()
    
    globe.Camera.fillScreen()
    if (globe.State.getState() == 'nominal'):
        globe.Updater.update(ELAPSED)
        globe.Updater.roomCollide()
        globe.Updater.playerCollide()
        globe.Updater.draw()
        
    #handling quit events?
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
               
    fps_meter.updateByMilli(ELAPSED)
    pygame.display.set_caption(WINDOW_CAPTION + fps_meter.getFPS())
    pygame.display.flip()
    ELAPSED = FPS_CLOCK.tick(FPS_CAP)