from src.entity import *
import src.globe as globe

class Enemy(HealthEntity):
    def __init__(self):
        super().__init__()
        
        self.hitDamage = 1
        self.entityType = 'enemy'
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['paused'])
        globe.Updater.registerDrawee(self.draw)
        globe.Updater.addCollideableEntity(self, ['nominal'], ['paused'])
        globe.Updater.registerEntityCollidee(self)
        
    def unRegister(self):
        globe.Updater.removeUpdatee(self.update)
        globe.Updater.removeDrawee(self.draw)
        globe.Updater.removeEntityCollidee(self)
        globe.Updater.removeCollideableEntity(self)
        
    def characterCollide(self, charObj):
        if(charObj.entityType == 'player'):
            charObj.hurt(self.hitDamage, self.pos.center)
        
    def draw(self):
        super().draw(globe.Camera.getDrawPos(self.pos))