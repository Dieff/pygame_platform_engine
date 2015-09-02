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
import src.globe as globe

pygame.init()

pygame.display.set_caption(WINDOW_CAPTION)

FPS_CLOCK = pygame.time.Clock()
ELAPSED = 10

fps_meter = fps_meter()

#singletons handled here
globe.Loader = Loader()
globe.Loader.LoadAreas(['Default', 'Common'])
globe.Loader.LoadAreas(['test'])
globe.State = State()
globe.Updater = Updater()

globe.Camera = Camera()

globe.Room = Room('test','1')
globe.Room.load()


Player = Player()
Player.spawn((50,50))

globe.Camera.start(Player)

while True:
    globe.Camera.fillScreen()
    if (globe.State.getState() == 'nominal'):
        globe.Updater.update(ELAPSED)
        globe.Updater.draw()
        
    if (pygame.event.get(pygame.QUIT)):
                pygame.quit()
                sys.exit()
    fps_meter.updateByMilli(ELAPSED)
    pygame.display.set_caption(WINDOW_CAPTION + fps_meter.getFPS())
    pygame.display.update()
    ELAPSED = FPS_CLOCK.tick(FPS_CAP)