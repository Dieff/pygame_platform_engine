from src.constants import *
import src.globe as globe
from src.graphics import *
import pygame

class Tile:
    def __init__(self, location, index, sprites, is_background, properties, animationDuration=100):
        self.index = index
        self.loc = location
        self.properties = properties
        self.bg = is_background
        self.anime = Animation(sprites, animationDuration, self.loc, True)
        
        #using "n" as uninitiated value is probably bad practice
        self.topCol = 'n'
        self.bottomCol = 'n'
        self.leftCol = 'n'
        self.rightCol = 'n'
        
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
    