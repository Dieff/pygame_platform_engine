import src.globe as globe
from src.entity import *
from src.constants import *

class Updater:
    def __init__(self):
        self.updatees = []
        
        self.bDraws = []
        self.eDraws = []
        self.pDraws = []
        self.aDraws = []
        self.hDraws = []
        
        self.roomCollidees = []
        self.entityCollidees = []
        self.entities = []
        self.Player = False
        
    def spawnPlayer(self, newLoc):
        if(self.Player):
            self.Player.spawn(newLoc)
        
    def getPlayerHealth(self):
        return self.Player.getHealth()
    
    def getPlayerMaxHealth(self):
        return self.Player.getMaxHealth()
        
    def register(self, registryList, registryObject, yesStates, noStates, otherInfo={}):
        entry = {'object':registryObject,'yesStates':yesStates,'noStates':noStates, 'other':otherInfo}
        registryList.append(entry)
        
    def remove(self, removeList, garbage):
        for item in removeList:
            if(item['object'] == garbage):
                removeList.remove(item)
        
    def objectPermitteable(self, registreeObject):
        yesStates = registreeObject['yesStates']
        noStates = registreeObject['noStates']
        allow = False
        for item in yesStates:
            if(globe.State.hasState(item)):
                allow = True
        for item in noStates:
            if(globe.State.hasState(item)):
                allow = False
        return allow
        
    def update(self, elapsedTime):
        for victim in self.updatees:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object'](elapsedTime)
            
    def draw(self):
        for victim in self.bDraws:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object']()
        for victim in self.eDraws:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object']()
        for victim in self.pDraws:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object']()
        for victim in self.aDraws:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object']()
        for victim in self.hDraws:
            if(not(self.objectPermitteable(victim))):
                continue
            victim['object']()
            
    def roomCollide(self):
        for item in self.roomCollidees:
            if(not(self.objectPermitteable(item))):
                continue
            item['object'].tileCollide(globe.Room.getTilesAround(item['object'].pos))
            
    def entityCollide(self):
        for pto in self.entityCollidees:
            if(not(self.objectPermitteable(pto))):
                continue
            for entity in self.entities:
                
                tpos = globe.Camera.getDrawPos(entity['object'].getNextPosition())
                tpos = pygame.Rect(tpos, (entity['object'].width, entity['object'].height))
                pygame.draw.rect(DISPLAYSURF, GREEN, tpos)
                
                
                if(not(pto['object'] == entity['object']) and pto['object'].getNextPosition().colliderect(entity['object'].getNextPosition())):
                    pto['object'].characterCollide(entity['object'])

    def setPlayer(self, player):
        self.Player = player
        
    def registerUpdatee(self, updateFunc, yesStates=['nominal'], noStates=[]):
        self.register(self.updatees, updateFunc, yesStates, noStates)
        
    def removeUpdatee(self, updateFunc):
        self.remove(self.updatees, updateFunc)
        
    def registerDrawee(self, drawFunc, yesStates=['nominal'], noStates=[], group='entities'):
        if(group == 'back'):
            self.register(self.bDraws, drawFunc, yesStates, noStates)
        elif(group == 'player'):
            self.register(self.pDraws, drawFunc, yesStates, noStates)
        elif(group == 'accessories'):
            self.register(self.aDraws, drawFunc, yesStates, noStates)
        elif(group == 'hud'):
            self.register(self.hDraws, drawFunc, yesStates, noStates)
        else:
            self.register(self.eDraws, drawFunc, yesStates, noStates)
        
    def removeDrawee(self, drawFunc):
        self.remove(self.bDraws, drawFunc)
        self.remove(self.eDraws, drawFunc)
        self.remove(self.pDraws, drawFunc)
        self.remove(self.aDraws, drawFunc)
        self.remove(self.hDraws, drawFunc)
        
    def registerRoomCollidee(self, PhysicsEntityBasedObject, yesStates=['nominal'], noStates=[]):
        self.register(self.roomCollidees, PhysicsEntityBasedObject, yesStates, noStates)
        
    def removeRoomCollidee(self, PhysicesEntityBasedObject):
        self.remove(self.roomCollidees, PhysicesEntityBasedObject)
        
    def registerEntityCollidee(self, entityBasedObject, yesStates=['nominal'], noStates=[]):
        self.register(self.entityCollidees, entityBasedObject, yesStates, noStates)
        
    def removeEntityCollidee(self, entityBasedObject):
        self.remove(self.entityCollidees, entityBasedObject)
    
    def addCollideableEntity(self, entity, yesStates=['nominal'], noStates=[]):
        print(entity)
        self.register(self.entities, entity, yesStates, noStates)
        
    def removeCollideableEntity(self, entity):
        self.remove(self.entities, entity)
                    