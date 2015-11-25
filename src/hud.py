from src.constants import *
from src.entity import *
from src.menus import *
from src.utilities import *
import src.globe as globe
import pygame


class DisplayMessage(TextItem):
    def __init__(self, text, duration, location):
        super().__init__(text, textSize=30)
        self.deleteMe = False
        self.timer = Timer()
        self.timer.set(duration)
        self.spawn(location)
        if(not(duration == 0)):
            self.timer.start()

    def draw(self):
        if(self.timer.isDone()):
            self.deleteMe = True
            self.unRegister()    
        super().draw()
        
    def delete(self):
        return self.deleteMe
    
    def kill(self):
        self.deleteMe = True
        self.unRegister()

class Meter(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.register()
        self.deleteMe = False
        
        #customizeables
        self.mColor = RED
        self.lColor = WHITE
        self.aColor = BLUE
        self.bgColor = GREY
        self.scale = 1 #pixels per unit
        self.cD = 1000 #in milliseconds
        
        self.barHeight = 14
        self.margin = 2
        self.padding = 4
        
        self.addSprite('Default-Meter', globe.Loader.getSprite('Default', 'meter'))
        self.curSprite = self.getSprite('Default-Meter')
        
        self.maxVal = 1
        self.minVal = 0
        self.curVal = 1
        self.oldVal = self.curVal
        self.changes = []
        self.curTime = 0
        
    def setMax(self, maxVal):
        self.maxVal = maxVal
        
    def setMin(self, minVal):
        self.minVal = minVal
        
    def setCurrentValue(self, curVal):
        self.curVal = curVal
        self.oldVal = self.curVal
        
    def update(self, elapsed):
        if(self.curVal > self.maxVal):
            self.curVal = self.maxVal
        elif(self.curVal < 0):
            self.curVal = 0
        self.curTime += elapsed
        if(not(self.curVal == self.oldVal)):
            change = {}
            change['start'] = self.curTime
            change['value'] = self.curVal - self.oldVal
            self.changes.append(change)
            
        for item in self.changes:
            if(item['start'] + self.cD < self.curTime):
                self.changes.remove(item)
                
        self.oldVal = self.curVal
    
    def draw(self):
        barFullHeight = self.barHeight + (2*self.margin) + (2*self.padding)
        backingHeight = self.barHeight + (2*self.margin)
        
        pygame.draw.rect(DISPLAYSURF, self.bgColor, pygame.Rect((self.pos[0], self.pos[1], self.curSprite.getWidth() + self.padding*3 + self.margin*2 + self.maxVal*self.scale, barFullHeight)))
        pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(self.pos[0]+(self.curSprite.getWidth() + self.padding*2), self.pos[1]+self.padding,self.maxVal*self.scale + self.margin*2, backingHeight))
        super().draw((self.pos[0]-self.padding, self.pos[1]-self.padding))
        
        barStartX = self.pos[0]+self.padding*2 + self.curSprite.getWidth() + self.margin
        barStartY = self.pos[1]+self.padding+self.margin
        barHeight = self.barHeight
        
        pygame.draw.rect(DISPLAYSURF, self.mColor, pygame.Rect(barStartX, barStartY, self.curVal*self.scale, barHeight))
        
        if(len(self.changes)>0):
            ch = self.changes[0]['value']
            if(ch > 0):
                pygame.draw.rect(DISPLAYSURF, self.aColor, pygame.Rect(barStartX + (self.curVal - ch)*self.scale, barStartY, ch*self.scale, barHeight))
            elif(ch < 0):
                pygame.draw.rect(DISPLAYSURF, self.lColor, pygame.Rect(barStartX + (self.curVal- ch)*self.scale, barStartY, ch*self.scale, barHeight))
        
    def delete(self):
        return self.deleteMe
        
class HealthBar(Meter):
    def __init__(self, pos):
        super().__init__(pos)
        self.setMax(100)
        self.setCurrentValue(self.maxVal)
        
    def update(self, elapsed):
        if(not(globe.Updater.getPlayerMaxHealth() == self.maxVal)):
            self.setMax(globe.Updater.getPlayerMaxHealth())
            
        self.curVal = globe.Updater.getPlayerHealth()
            
        super().update(elapsed)
        
class Hud:
    def __init__(self):
        self.currentDisplayEntities = []
        globe.Updater.registerUpdatee(self.update)
        globe.Updater.registerDrawee(self.draw, ['nominal'], [], 'hud')
        self.currentDisplayEntities.append(HealthBar((50,50)))
        
    def displayText(self, duration, text, location):
        print('text rendered', text)
        display = DisplayMessage(text, duration, location)
        self.currentDisplayEntities.append(display)
        return display
        
    def removeAllText(self):
        for item in self.currentDisplayEntities:
            if(type(item) is DisplayMessage):
                item.kill()
        
    def update(self, elapsed):
        for item in self.currentDisplayEntities:
            if(item.delete()):
                self.currentDisplayEntities.remove(item)
            
    def draw(self):
        for item in self.currentDisplayEntities:
            item.draw()