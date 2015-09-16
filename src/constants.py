import pygame
import os.path

FPS_CAP = 60
MAX_FRAME_TIME = 50

WINDOW_CAPTION = 'Spunky Doods Game Engine  FPS:'

TILE_SIZE = 32

WINDOWWIDTH = TILE_SIZE*20

WINDOWHEIGHT = TILE_SIZE*16

flags = pygame.DOUBLEBUF | pygame.RESIZABLE# | pygame.FULLSCREEN # | pygame.RESIZABLE

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags, 32)

DISPLAYSURF.set_alpha(None)

#Some helpful colors
#            R    G    B
GRAY     = (100, 100, 100)
GREY = GRAY
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
TRANSPARENT = (255, 0, 255)
BLACK = (0,0,0)


PATH_TO_AREAS = os.path.join('Data', 'Areas')