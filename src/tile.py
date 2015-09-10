from src.constants import *
import src.globe as globe
from src.graphics import *
import pygame

class LevelBlock:
    def __init__(self, location, index, properties):
        self.index = index
        self.loc = location
        self.properties = properties
    
    def getRect(self):
        return pygame.Rect(self.index[1]*TILE_SIZE, self.index[0]*TILE_SIZE, TILE_SIZE,TILE_SIZE)
    
    def getCenter(self):
        r = self.getRect()
        return r.center
    
    def update(self, location=False):
        if(not(location)):
            location = self.loc
        self.loc = location
    
    def draw(self):
        pass

class Tile(LevelBlock):
    def __init__(self, location, index, properties, sprites, is_background, animationDuration=100):
        super().__init__(location, index, properties)
        
        self.bg = is_background
        self.anime = Animation(sprites, animationDuration, self.loc, True)
        
        #using "n" as uninitiated value is probably bad practice
        self.topCol = 'n'
        self.bottomCol = 'n'
        self.leftCol = 'n'
        self.rightCol = 'n'
        
        
    def update(self, elapsed_time, location = False):
        self.anime.update(elapsed_time, location)
        super().update(location)
        
    def draw(self):
        self.anime.draw()
        
    def canCollide(self, side):
        #print('myIndex', self.index)
        if(side == 'right'):
            peer = globe.Room.getTile((self.index[1]-1, self.index[0]))
            if(peer):
                if(peer.properties['solid']):
                    return False
            return True
        if(side == 'left'):
            peer = globe.Room.getTile((self.index[1]+1, self.index[0]))
            #print('hisIndex', peer.index)
            if(peer):
                if(peer.properties['solid']):
                    return False
            return True
        if(side == 'top'):
            peer = globe.Room.getTile((self.index[1], self.index[0]+1))
            if(peer):
                if(peer.properties['solid']):
                    return False
            return True
        if(side == 'bottom'):
            peer = globe.Room.getTile((self.index[1], self.index[0]-1))
            if(peer):
                if(peer.properties['solid']):
                    return False
            return True
        return True
    
    def canCollisionOccur(self, side):
        if(side == 'top'):
            if(self.topCol == 'n'):
                self.topCol = self.canCollide('top')
            return self.topCol
        elif(side == 'bottom'):
            if(self.bottomCol == 'n'):
                self.bottomCol = self.canCollide('bottom')
            return self.bottomCol
        elif(side == 'left'):
            if(self.leftCol == 'n'):
                self.leftCol = self.canCollide('left')
            return self.leftCol
        elif(side == 'right'):
            if(self.rightCol == 'n'):
                self.rightCol == self.canCollide('right')
            return self.rightCol
        return True
    
    
class BackgroundTile():
    def __init__(self, index, location, sprites, animationDuration=10):
        self.index = index
        self.startingLoc = location
        self.anime = Animation(sprites, animationDuration, location)
        
    def update(self, elapsed_time):
        self.anime.update(elapsed_time, globe.Camera.getBackgroundDrawPos(self.startingLoc))
        
    def draw(self):
        self.anime.draw()