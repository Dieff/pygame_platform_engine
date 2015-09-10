import src.globe as globe

class Updater:
    def __init__(self):
        self.updatees = []
        self.drawees = []
        self.roomCollidees = []
        self.playerCollidees = []
        self.mutualCollidees = []
        self.Player = False
        
    def update(self, elapsedTime):
        for updateFunction in self.updatees:
            updateFunction(elapsedTime)
            
    def draw(self):
        for drawFunc in self.drawees:
            drawFunc()
            
    def roomCollide(self):
        for item in self.roomCollidees:
            item.tileCollide(globe.Room.getTilesAround(item.pos))
            
    def playerCollide(self):
        for item in self.playerCollidees:
            itemRect = item.getNextPos()
            if(itemRect.colliderect(self.Player.getNextPos())):
                item.playerCollide(self.Player)
        
    def setPlayer(self, player):
        self.Player = player
        
    def registerUpdatee(self, updateFunc):
        self.updatees.append(updateFunc)
        
    def removeUpdatee(self, updateFunc):
        self.updatees.remove(updateFunc)
        
    def registerDrawee(self, drawFunc):
        self.drawees.append(drawFunc)
        
    def removeDrawee(self, drawFunc):
        self.drawees.remove(drawFunc)
        
    def registerRoomCollidee(self, PhysicesEntityBasedObject):
        self.roomCollidees.append(PhysicesEntityBasedObject)
        
    def removeRoomCollidee(self, PhysicesEntityBasedObject):
        self.roomCollidees.remove(PhysicesEntityBasedObject)
        
    def registerPlayerCollidee(self, entityBasedObject):
        self.playerCollidees.append(entityBasedObject)
        
    def removePlayerCollidee(self, entityBasedObject):
        self.playerCollidees.remove(entityBasedObject)
    