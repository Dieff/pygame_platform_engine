from src.constants import *

class Entity:
    def __init__(self):
        self.pos = (0,0)
        self.vel = (0,0)
        
    def setPosition(self, elapsed):
        self.pos = (self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed)
        
    def update(self, elapsed):
        self.setPosition()