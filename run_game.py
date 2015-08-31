import pygame
import sys
from src.constants import *
from src.constants import *
from src.utilities import *
from src.update import *
from src.room import *
from src.player import *
from src.loader import *

pygame.init()

pygame.display.set_caption(WINDOW_CAPTION)

FPS_CLOCK = pygame.time.Clock()
ELAPSED = 10

fps_meter = fps_meter()
Loader = Loader()
Loader.load()
State = State()
Updater = Updater()
Player = Player(Updater)

while True:
    DISPLAYSURF.fill(BLUE)
    if (State.getState() == 'nominal'):
        Updater.update(ELAPSED)
        Updater.draw()
        
    if (pygame.event.get(pygame.QUIT)):
                pygame.quit()
                sys.exit()
    fps_meter.updateByMilli(ELAPSED)
    pygame.display.set_caption(WINDOW_CAPTION + fps_meter.getFPS())
    pygame.display.update()
    ELAPSED = FPS_CLOCK.tick(FPS_CAP)