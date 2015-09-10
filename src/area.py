import src.globe as globe
from src.room import *
from src.constants import *

class Area:
    def __init__(self):
        self.areaId = ''
        self.roomId = ''
        self.Room = Room()
        globe.Room = self.Room
        
    def getRoomId(self):
        return self.roomId
        
    def getRoom(self):
        return self.Room    
    
    def loadArea(self, areaId):
        self.areaId = areaId
        globe.Loader.loadArea(areaId)
        
    def changeRoom(self, roomId):
        self.roomId = roomId
        self.Room.load(self.areaId, roomId)