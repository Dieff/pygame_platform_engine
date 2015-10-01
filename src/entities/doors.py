import pygame
import src.globe as globe
from src.entity import *
from src.constants import *

class InvisiDoor(Entity):
    def __init__(self):
        super().__init__()
        globe.Updater.registerEntityCollidee(self, ['nominal'], ['paused'])
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
    def addData(self, data):
        if(not('action' in data)):
            data['action'] = {}
            
        if('width' in data['action']):
            self.width = data['action']['width']
        
        if('height' in data['action']):
            self.height = data['action']['height']
        
        super().addData(data)
        
    def register(self):
        pass
        
    def processRoom(self, playerObj):
        if(self.data['action'] == ''):
                print('Error - no action defined for door at ', self.pos)
                return None
        
        myData = self.data['action']
        
        doRoom = False
        room = globe.Area.getRoomId()
        if('room' in myData):
            room = myData['room']
            doRoom = True
        
        newX = playerObj.pos[0]
        newY = playerObj.pos[1]
        if('newPosX' in myData):
            newX = myData['newPosX']
        if('newPosY' in myData):
            newY = myData['newPosY']    
        
        if(doRoom):
            print('load started')
            globe.Area.cinematicLoad(room, (newX, newY))
        
    def characterCollide(self, entityObj):
        print('char Collide', entityObj)
        if(entityObj.entityType == 'player'):
            self.processRoom(entityObj)


class Door(InvisiDoor):
    def __init__(self):
        super().__init__()
        globe.Updater.registerDrawee(self.draw)
        self.curSprite = globe.Loader.getSprite('common', 'door')
        self.width = 24
        
    def draw(self):
        pos = globe.Camera.getDrawPos(self.pos)
        super().draw(pos)
        
    def characterCollide(self, entityObj):
        key_states = pygame.key.get_pressed()
        if(key_states[pygame.K_DOWN]):
            super().characterCollide(entityObj)