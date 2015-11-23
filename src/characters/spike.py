from src.characters.enemy import *
from src.constants import *
import src.globe as globe

class Spike(Enemy):
    def __init__(self):
        super().__init__()
        self.addSprite('spike', globe.Loader.getSprite('common', 'spike'))
        self.curSprite = self.getSprite('spike')
        self.width = 27
        self.height = 28
        self.hitDamage = 25
        self.updateMaxHealth(100)
    
    def update(self, el):
        super().update(el)
        self.pos = self.npos
        
    def draw(self):
        super().draw()
        tpos = globe.Camera.getDrawPos(self.npos)
        tpos = pygame.Rect(tpos, (self.width, self.height))
        #pygame.draw.rect(DISPLAYSURF, RED, tpos)