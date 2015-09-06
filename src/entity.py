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
        
    def createCollisionRects(self):
        self.up = pygame.Rect(self.npos[0] + 1, self.npos[1] + 1, self.width-2, (self.height/2)-2)
        self.down = pygame.Rect(self.npos[0] + 1, self.npos[1] + (self.height/2)+1, self.width-2, (self.height/2 -2))
        self.left = pygame.Rect(self.npos[0] + 1, self.npos[1] + 1, (self.width / 2) -2, self.height - 2)
        self.right = pygame.Rect(self.npos[0] + (self.width/2)+1, self.npos[1] + 1, (self.width / 2) -2, self.height - 2)
        
    '''def collide(self, side, object):
        print('ouch', side, object, self.pos)'''
        