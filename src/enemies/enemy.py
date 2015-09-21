from src.entity import *
import src.globe as globe

class Enemy(HealthEntity):
    def __init__(self):
        super().__init__()
        
        self.hitDamage = 1
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['paused'])
        globe.Updater.registerDrawee(self.draw)
        globe.Updater.registerPlayerCollidee(self, ['nominal'], ['paused'])
        
    def unRegister(self):
        globe.Updater.removeUpdatee(self.update)
        globe.Updater.removeDrawee(self.draw)
        globe.Updater.removePlayerCollidee(self)
        
    def playerCollide(self, playerObj):
        playerObj.hurt(self.hitDamage, self.pos.center)
        
    def draw(self):
        super().draw(globe.Camera.getDrawPos(self.pos))