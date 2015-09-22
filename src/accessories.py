from src.constants import *
from src.entity import *
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
        
    def update(self, elapsedTime, side):
        self.curSprite = self.getSprite(side)
        
        super().update(elapsedTime)
        key_states = pygame.key.get_pressed()
        if(key_states[pygame.K_d]):
            print('POW')