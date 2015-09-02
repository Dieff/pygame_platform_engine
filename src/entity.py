from src.constants import *
import src.globe as globe
import pygame

class Entity:
    def __init__(self):
        self.pos = (0,0)
        self.npos = (0,0)
        self.vel = (0,0)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
    def register(self):
        globe.Updater.registerUpdatee(self.update)
        globe.Updater.registerDrawee(self.draw)
        
    def setTempPosition(self, elapsed):
        self.npos = (self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed)
        
    def setPermanentPosition(self):
        self.pos = self.npos
        
    def update(self, elapsed):
        self.setTempPosition()
        
    def createCollisionRects(self):
        self.up = pygame.Rect(self.npos[0] + 1, self.npos[1] + 1, self.width-2, (self.height/2)-2)
        self.down = pygame.Rect(self.npos[0] + 1, self.npos[1] + self.height - 1, self.width-2, (self.height/2 -2))
        self.right = pygame.Rect(self.npos[0] + 1, self.npos[1] + 1, (self.width / 2) -2, self.height - 2)
        self.left = pygame.Rect(self.npos[0] + self.width - 1, self.npos[1] + 1, (self.width / 2) -2, self.height - 2)
        
    def collide(self, side, object):
        print('ouch', side, object)
        