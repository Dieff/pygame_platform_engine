from src.constants import *
from src.graphics import *
import src.globe as globe
import pygame

class Entity:
    def __init__(self):
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.pos = pygame.Rect(0,0,self.width,self.height)
        self.data = {}
        self.curSprite = False
        self.sprites = {}
        
    def addData(self, data):
        self.data.update(data)
        
    def update(self, elapsed_time):
        if(self.curSprite):
            self.curSprite.update(elapsed_time)
    
    def draw(self, pos):
        if(self.curSprite):
            self.curSprite.draw(pos)
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['room-transition', 'paused'])
        globe.Updater.registerDrawee(self.draw)
        
    def unRegister(self):
        globe.Updater.removeUpdatee(self.update)
        globe.Updater.removeDrawee(self.draw)
        
    def spawn(self, location):
        self.pos = pygame.Rect(location[0], location[1], self.width, self.height)
        
    def getNextPos(self):
        return self.pos
    
    def playerCollide(self):
        pass
    
    def tileCollide(self):
        pass
    
    def addSprite(self, spriteName, spriteAnimationObject):
        self.sprites[spriteName] = spriteAnimationObject
        
    def setSprite(self, name):
        self.curSprite = self.sprites[spriteName]
        
    def getCurSprite(self):
        return self.curSprite
    
    def drawWidthDifference(self):
        if(self.curSprite):
            return int(self.width - self.curSprite.getWidth())
        
    def drawHeightDifference(self):
        if(self.curSprite):
            return int(self.height - self.curSprite.getHeight())
        
    def getSprite(self, name):
        return self.sprites[name]
        
class PhysicsEntity(Entity):
    def __init__(self):
        super().__init__()
        self.npos = self.pos
        self.vel = (0,0)
    
    def spawn(self, location):
        super().spawn(location)
        self.vel = (0,0)
        self.npos = self.pos
    
    def getNextPos(self):
        return self.npos
    
    def registerCollidee(self):
        globe.Updater.registerRoomCollidee(self, ['nominal'], ['room-transition', 'paused'])
    
    def registerAll(self):
        self.register()
        self.registerCollidee()
        
    def setTempPosition(self, elapsed):
        self.npos = pygame.Rect(self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed, self.width, self.height)
        
    def setPermanentPosition(self):
        self.pos = self.npos
        
    def update(self, elapsed):
        super().update(elapsed)
        self.setTempPosition()
        
    def getCollidePoints(self):
        self.top = (self.npos.left + (self.width/2), self.npos.top)
        self.bottom = (self.npos.left + (self.width/2), self.npos.bottom)
        self.left = (self.npos.left, self.pos.top + (self.height/2))
        self.right = (self.npos.right, self.pos.top + (self.height/2))