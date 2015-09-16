from src.constants import *
from src.entity import *
from src.utilities import *
import src.globe as globe
import pygame

class DisplayMessage(Entity):
    def __init__(self, text, duration, location):
        super().__init__()
        self.deleteMe = False
        self.timer = Timer()
        self.timer.set(duration)
        self.spawn(location)
        self.timer.start()
        self.text = text

    def draw(self):
        if(self.timer.isDone()):
            self.deleteMe = True
            self.unRegister()
            
        font = pygame.font.SysFont('Georgia', 27, False, True,)
        text = font.render(self.text, 1, WHITE, GREY)
        text.set_colorkey(GREY)
        DISPLAYSURF.blit(text, self.pos)
            
    def delete(self):
        return self.deleteMe


        
class Hud:
    def __init__(self):
        self.currentDisplayEntities = []
        globe.Updater.registerUpdatee(self.update)
        globe.Updater.registerDrawee(self.draw)
        
    def displayText(self, duration, text, location):
        print('text rendered', text)
        dislay = DisplayMessage(text, duration, location)
        self.currentDisplayEntities.append(dislay)
        
    def update(self, elapsed):
        for item in self.currentDisplayEntities:
            if(item.delete()):
                self.currentDisplayEntities.remove(item)
            
    def draw(self):
        for item in self.currentDisplayEntities:
            item.draw()