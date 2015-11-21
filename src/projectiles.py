from src.constants import *
from src.entity import *
from src.utilities import *
import src.globe as globe

class Projectile(PhysicsEntity):
    def __init__(self, startPos, startVel, duration):
        super().__init__()
        self.lifeTime = Timer(duration, self.kill, True)
        self.spawn(startPos)
        self.vel = startVel
        
        self.pos.width = 4
        self.pos.height = 4
        
        self.npos = self.pos
        
        self.kil = False
        
        self.entityType = 'bullet'
        
        self.damage = 10
        
    def register(self):
        super().register()
        globe.Updater.addCollideableEntity(self, ['nominal'], ['paused'])
        globe.Updater.registerEntityCollidee(self)
        
    def unRegister(self):
        super().unRegister()
        globe.Updater.removeEntityCollidee(self)
        globe.Updater.removeCollideableEntity(self)
       
    def update(self, el):
        super().update(el)
        
    def kill(self):
        self.unRegister()
        self.kil = True
        
    def explode(self):
        self.kill()
        
    def draw(self):
        self.setPermanentPosition()
        tpos = globe.Camera.getDrawPos(self.pos)
        tpos = pygame.Rect(tpos, (self.pos.width, self.pos.height))
        pygame.draw.rect(DISPLAYSURF, RED, tpos)
        
    def tileCollide(self, tiles):
        for tile in tiles:
            if(tile.properties['solid'] and self.npos.colliderect(tile.getRect())):
                print('boom')
                self.explode()
                
    def characterCollide(self, charObj):
        if(charObj.entityType == 'enemy'):
            charObj.hurt(self.damage)
            self.explode()