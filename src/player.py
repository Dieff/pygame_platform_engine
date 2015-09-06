from src.entity import *
from src.update import *
from src.constants import *
import pygame
import src.globe as globe

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.registerAll()
        
        self.width = 32
        self.height = 32
                
        self.oldTiles = []
                
    def update(self, elapsedTime):
        key_states = pygame.key.get_pressed()
        
        speddd = 0.01
        
        if(key_states[pygame.K_DOWN]):
            self.vel = (self.vel[0], self.vel[1]+speddd)
            
        if(key_states[pygame.K_UP]):
            self.vel = (self.vel[0], self.vel[1]-speddd)
            
        if(key_states[pygame.K_LEFT]):
            self.vel = (self.vel[0]-speddd, self.vel[1])
            
        if(key_states[pygame.K_RIGHT]):
            self.vel = (self.vel[0]+speddd, self.vel[1])
            
        self.setTempPosition(elapsedTime)
        #self.setPermanentPosition()
        
    def draw(self):
        pdp = globe.Camera.getPlayerDrawPos()
        pygame.draw.rect(DISPLAYSURF, RED, (pdp[0], pdp[1], self.width, self.height))
        
        '''for item in self.oldTiles:
            pos = globe.Camera.getDrawPos(item.loc)
            pygame.draw.rect(DISPLAYSURF, CYAN, (pos[0], pos[1], 32, 32))
            
        pygame.draw.rect(DISPLAYSURF, BLUE, self.up)
        pygame.draw.rect(DISPLAYSURF, GREEN, self.down)
        pygame.draw.rect(DISPLAYSURF, YELLOW, self.right)
        pygame.draw.rect(DISPLAYSURF, ORANGE, self.left)'''
        
    def spawn(self, loc):
        self.pos = loc
        
    def tileCollide(self, tiles):
        
        self.oldTiles = tiles
        
        '''self.createCollisionRects()
        
        for item in tiles:
            if(item.properties['solid']):
                print(item)
                if(item.getRect().colliderect(self.up)):
                    print('UP')
                if(item.getRect().colliderect(self.down)):
                    print('DOWN')
                if(item.getRect().colliderect(self.right)):
                    print('RIGHT')
                if(item.getRect().colliderect(self.left)):
                    print('LEFT')'''
        currect = self.npos
        for item in tiles:
            ir = item.getRect()
            if(currect.colliderect(ir)):
                if(item.properties['solid']):
                    print('ouch')
                    self.npos = self.pos
        

        self.setPermanentPosition()
        