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
        
        self.width = 4
        self.height = 4
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
        
    def kill(self):
        self.unRegister()
        self.kil = True
        
    def explode(self):
        self.kill()
        
    def draw(self):
        self.setPermanentPosition()
        tpos = globe.Camera.getDrawPos(self.pos)
        tpos = pygame.Rect(tpos, (self.width, self.height))
        pygame.draw.rect(DISPLAYSURF, RED, tpos)
        
    def tileCollide(self, tiles):
        testPos = pygame.Rect((self.npos.left, self.npos.top), (self.width, self.height))
        
        for tile in tiles:
            if(tile.properties['solid'] and testPos.colliderect(tile.getRect())):
                self.explode()
                
    def characterCollide(self, charObj):
        if(charObj.entityType == 'enemy'):
            charObj.hurt(self.damage)
            self.explode()