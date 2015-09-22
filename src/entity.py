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
            #fixes things if sprite is different width from collision width
            self.curSprite.draw((pos[0]+int(self.drawWidthDifference()/2),pos[1]+int(self.drawHeightDifference()/2)))
        
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
        self.npos = self.pos.move(int(self.vel[0]*elapsed), int(self.vel[1]*elapsed))#pygame.Rect(self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed, self.width, self.height)
        self.npos.inflate(self.npos.width - self.width, self.npos.height - self.height)
        
    def setPermanentPosition(self):
        self.pos = self.npos
        
    def update(self, elapsed):
        super().update(elapsed)
        self.setTempPosition(elapsed)
        
    def getCollidePoints(self):
        self.top = (self.npos.left + (self.width/2), self.npos.top)
        self.bottom = (self.npos.left + (self.width/2), self.npos.bottom)
        self.left = (self.npos.left, self.pos.top + (self.height/2))
        self.right = (self.npos.right, self.pos.top + (self.height/2))
        
class HealthEntity(PhysicsEntity):
    def __init__(self):
        super().__init__()
        self.maxHealth = 1
        self.health = self.maxHealth
        
    def kill(self):
        print('Shit Im Dead!')
        self.unRegister()
        
    def setMaxHealth(self, health):
        self.maxHealth = health
        
    def hurt(self, damage):
        self.health -= damage
        
    def heal(self, health):
        self.health += health
        
    def getMaxHealth(self):
        return self.maxHealth
    
    def getHealth(self):
        return self.health
        
    def update(self, elapsed):
        super().update(elapsed)
        if(self.health <= 0):
            self.kill()
        