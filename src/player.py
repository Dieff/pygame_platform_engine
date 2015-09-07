from src.entity import *
from src.update import *
from src.constants import *
from src.utilities import *
import pygame
import src.globe as globe
import math

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.registerAll()
        
        self.width = 32
        self.height = 32
                
        self.oldTiles = []
        
        self.jumpJuice = 0
        self.jumpCounter = 0
        
        self.old_states = dict()
        
                
    def update(self, elapsedTime):
        key_states = pygame.key.get_pressed()
        
        self.vel = (self.vel[0],self.vel[1] + (0.03))
        
        self.speedLimit = 1
        
        
        speddd = 0.02
        
        self.jumpJuice -= elapsedTime
        
        if(key_states[pygame.K_DOWN]):
            self.vel = (self.vel[0], self.vel[1]+speddd)
            
        if(key_states[pygame.K_UP]):
            self.vel = (self.vel[0], self.vel[1]-0.05)
            
        if(key_states[pygame.K_LEFT]):
            self.vel = (self.vel[0]-speddd, self.vel[1])
            
        if(key_states[pygame.K_RIGHT]):
            self.vel = (self.vel[0]+speddd, self.vel[1])
            
        if(key_states[pygame.K_f]):
            if(self.old_states[pygame.K_f]):
                self.jumpJuice = 0
                self.jumpCounter -= 1
                if(self.jumpCounter > 0):
                    self.vel = (self.vel[0], self.vel[1]-0.3 * self.jumpCounter)
            elif(self.jumpJuice > 0):
                self.jumpCounter = 10

            
            
        yspeedLimit = 0.4
        xSpeedLimit = 0.2
        if(self.vel[0] > xSpeedLimit):
            self.vel = (xSpeedLimit, self.vel[1])
        if(self.vel[0] < xSpeedLimit*-1):
            self.vel = (xSpeedLimit*-1, self.vel[1])
        if(self.vel[1] > yspeedLimit):
            self.vel = (self.vel[0], yspeedLimit)
        if(self.vel[1] < yspeedLimit*-1):
            self.vel = (self.vel[0], yspeedLimit*-1)
            
            
        self.setTempPosition(elapsedTime)
        self.old_states = key_states
        
    def draw(self):
        pdp = globe.Camera.getPlayerDrawPos()
        pygame.draw.rect(DISPLAYSURF, RED, (pdp[0], pdp[1], self.width, self.height))
        
        '''for item in self.oldTiles:
            pos = globe.Camera.getDrawPos(item.loc)
            pygame.draw.rect(DISPLAYSURF, CYAN, (pos[0], pos[1], 32, 32))'''
            
        
    def spawn(self, loc):
        self.pos = loc
        
        
    def tileCollide(self, tiles):
        self.oldTiles = tiles
        
        
        currect = self.npos
        for item in tiles:
            ir = item.getRect()
            if(currect.colliderect(ir)):
                if(item.properties['solid']):
                    tileCenter = (ir.center)
                    self.getCollidePoints()
                    #Creates an array of the distances between collidepoints and tile center
                    distances = [getDistance(self.top, tileCenter),getDistance(self.bottom, tileCenter),getDistance(self.left, tileCenter),getDistance(self.right,tileCenter)]
                    #determines smallest distance (index of smallest number in distances)
                    smallestIndex = distances.index(min(distances))
                    #does shit based on the collision side
                    if(smallestIndex == 0):
                        #Top collision
                        dY = abs(self.npos.top - self.pos.top)
                        badY = abs(ir.bottom - self.npos.top)
                        okY = abs(dY - badY)
                        self.npos = pygame.Rect(self.npos.left, self.pos.top-okY, self.width, self.height)
                        self.vel = (self.vel[0], 0)
                        
                        self.jumpCounter = 0
                        self.jumpJuice = 0
                    elif(smallestIndex == 1):
                        #Bottom collision
                        dY = abs(self.npos.bottom - self.pos.bottom)
                        badY = abs(ir.top - self.npos.bottom)
                        okY = abs(dY - badY)
                        self.npos = pygame.Rect(self.npos.left, self.pos.top+okY, self.width, self.height)
                        
                        Friction = 0.005
                        
                        if(self.vel[0]>0):
                            self.vel = (self.vel[0]-Friction, 0)
                        elif(self.vel[0]<0):
                            self.vel = (self.vel[0]+Friction, 0)
                        else:
                            self.vel = (self.vel[0], 0)
                            
                        self.jumpJuice = 75

                        
                    elif(smallestIndex == 2):
                        #Left collision
                        dX = abs(self.npos.left - self.pos.left)
                        badX = abs(ir.right - self.npos.left)
                        okX = abs(dX - badX)
                        self.npos = pygame.Rect(self.pos.left-okX, self.npos.top, self.width, self.height)
                        self.vel = (0, self.vel[1])
                    else:
                        #Right Collision
                        dX = abs(self.npos.right - self.pos.right)
                        badX = abs(ir.left - self.npos.right)
                        okX = abs(dX - badX)
                        self.npos = pygame.Rect(self.pos.left+okX, self.npos.top, self.width, self.height)
                        self.vel = (0, self.vel[1])
                    
        
        self.setPermanentPosition()
        