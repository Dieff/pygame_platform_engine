from src.constants import *
from src.entity import *
from src.utilities import *
from src.projectiles import *
import src.globe as globe

import pygame

class Accessory(Entity):
    def __init__(self):
        super().__init__()
        self.funcX = 0
        self.xPositionOffset = 0
        self.yPositionOffset = 0
        
    def update(self, elapsedTime):
        super().update(elapsedTime)
        self.funcX += elapsedTime
        
    def getRelativePosition(self, parentalPosition):
        return parentalPosition.move(self.xPositionOffset, self.yPositionOffset)
        
    def draw(self, parentalPosition):
        drawPos = self.getRelativePosition(parentalPosition)
        super().draw(drawPos)
        
class Gun(Accessory):
    def __init__(self):
        super().__init__()
        self.addSprite('left', globe.Loader.getSprite('common', 'gun-left'))
        self.addSprite('right', globe.Loader.getSprite('common', 'gun-right'))
        self.curSprite = self.getSprite('left')
        self.bullets = []
        self.oldStates = pygame.key.get_pressed()
        
        
    def update(self, elapsedTime, side, npos):
        self.pos = npos
        self.curSprite = self.getSprite(side)
        
        super().update(elapsedTime)
        key_states = pygame.key.get_pressed()
        if(key_states[pygame.K_d] and not(self.oldStates[pygame.K_d])):
            if(side == 'left'):
                b = Projectile(self.pos.move(16,16), (-0.6,0), 3000)
            elif(side == 'right'):
                b = Projectile(self.pos.move(16,16), (0.6,0), 3000)
            b.register()
            self.bullets.append(b)
            
        self.oldStates = key_states
        
        for item in self.bullets:
            if(item.kil):
                self.bullets.remove(item)
        
    def cleanse(self):
        for item in self.bullets:
            item.kill()