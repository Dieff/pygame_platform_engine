from src.constants import *
import src.globe as globe
from src.graphics import *
import pygame

class Tile:
    def __init__(self, location, index, sprites, is_background, properties, animationDuration=1):
        self.index = index
        self.loc = location
        self.properties = properties
        self.bg = is_background
        self.anime = Animation(sprites, animationDuration, self.loc, True)
        
    def getRect(self):
        return pygame.Rect(self.index[1]*TILE_SIZE, self.index[0]*TILE_SIZE, TILE_SIZE,TILE_SIZE)
        
    def getCenter(self):
        r = self.getRect()
        return r.center
        
    def update(self, elapsed_time, location = False):
        if(not(location)):
            location = self.loc
        self.anime.update(elapsed_time, location)
        self.loc = location
        
    def draw(self):
        self.anime.draw()