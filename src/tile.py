from src.constants import *
import src.globe as globe
from src.graphics import *

class Tile:
    def __init__(self, location, index, sprites, is_background, properties, animationDuration=1):
        self.index = index
        self.loc = location
        self.properties = properties
        self.bg = is_background
        self.anime = Animation(sprites, animationDuration, self.loc, True)
        
    def update(self, elapsed_time, location = False):
        if(not(location)):
            location = self.loc
        self.anime.update(elapsed_time, location)
        self.loc = location
        
    def draw(self):
        self.anime.draw()