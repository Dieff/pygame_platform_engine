from src.entity import *
from src.update import *
from src.constants import *
import pygame
import src.globe as globe

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.register()
        
        self.width = 32
        self.height = 32
                
                
    def update(self, elapsedTime):
        key_states = pygame.key.get_pressed()
        
        speddd = 0.05
        
        if(key_states[pygame.K_DOWN]):
            self.vel = (self.vel[0], self.vel[1]+speddd)
            
        if(key_states[pygame.K_UP]):
            self.vel = (self.vel[0], self.vel[1]-speddd)
            
        if(key_states[pygame.K_LEFT]):
            self.vel = (self.vel[0]-speddd, self.vel[1])
            
        if(key_states[pygame.K_RIGHT]):
            self.vel = (self.vel[0]+speddd, self.vel[1])
            
        self.setTempPosition(elapsedTime)
        self.setPermanentPosition()
        
    def draw(self):
        pdp = globe.Camera.getPlayerDrawPos()
        pygame.draw.rect(DISPLAYSURF, RED, (pdp[0], pdp[1], self.width, self.height))
        
    def spawn(self, loc):
        self.pos = loc