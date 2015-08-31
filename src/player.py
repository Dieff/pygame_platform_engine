from src.entity import *
from src.update import *
from src.constants import *
import pygame

class Player(Entity):
    def __init__(self, Updater):
        super().__init__()
        Updater.registerUpdatee(self.update)
        Updater.registerDrawee(self.draw)
        
        self.width = 32
        self.height = 32
                
    def update(self, elapsedTime):
        key_states = pygame.key.get_pressed()
        if(key_states[pygame.K_DOWN]):
            self.vel = (self.vel[0], self.vel[1]+0.1)
            
        if(key_states[pygame.K_UP]):
            self.vel = (self.vel[0], self.vel[1]-0.1)
            
        if(key_states[pygame.K_LEFT]):
            self.vel = (self.vel[0]-0.1, self.vel[1])
            
        if(key_states[pygame.K_RIGHT]):
            self.vel = (self.vel[0]+0.1, self.vel[1])
            
        self.setPosition(elapsedTime);
        self.vel = (0,0)
        
    def draw(self):
        pygame.draw.rect(DISPLAYSURF, RED, (self.pos[0], self.pos[1], self.width, self.height))