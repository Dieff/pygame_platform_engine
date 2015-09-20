from src.enemies.enemy import *
from src.constants import *
import src.globe as globe

class Spike(Enemy):
    def __init__(self):
        super().__init__()
        self.addSprite('spike', globe.Loader.getSprite('common', 'spike'))
        self.curSprite = self.getSprite('spike')
        self.width = 20
        self.height = 28