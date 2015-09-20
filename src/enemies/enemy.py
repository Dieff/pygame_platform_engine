from src.entity import *
import src.globe as globe

class Enemy(PhysicsEntity):
    def __init__(self):
        super().__init__()
        
        self.hitDamage = 0
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['paused'])
        globe.Updater.registerDrawee(self.draw)
        globe.Updater.registerPlayerCollidee(self, ['nominal'], ['paused'])
        print('regged')
        
    def playerCollide(self, playerObj):
        print('Fuck you player!!!!!!')
        
    def draw(self):
        super().draw(globe.Camera.getDrawPos(self.pos))