from src.constants import *
import src.globe as globe
import pygame

class Entity:
    def __init__(self):
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.pos = pygame.Rect(0,0,self.width,self.height)
        self.npos = self.pos
        self.vel = (0,0)
        
    def register(self):
        globe.Updater.registerUpdatee(self.update)
        globe.Updater.registerDrawee(self.draw)
        
    def registerCollidee(self):
        globe.Updater.registerRoomCollidee(self)
        
    def registerAll(self):
        self.register()
        self.registerCollidee()
        
    def setTempPosition(self, elapsed):
        self.npos = pygame.Rect(self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed, self.width, self.height)
        
    def setPermanentPosition(self):
        self.pos = self.npos
        
    def update(self, elapsed):
        self.setTempPosition()
        
    def spawn(self, location):
        self.pos = pygame.Rect(location[0], location[1], self.width, self.height)
        
    def getCollidePoints(self):
        self.top = (self.npos.left + (self.width/2), self.npos.top)
        self.bottom = (self.npos.left + (self.width/2), self.npos.bottom)
        self.left = (self.npos.left, self.pos.top + (self.height/2))
        self.right = (self.npos.right, self.pos.top + (self.height/2))
        