import pygame
import src.globe as globe
from src.entity import *
from src.constants import *

class Door(Entity):
    def __init__(self):
        super().__init__()
        globe.Updater.registerPlayerCollidee(self)
        self.curSprite = globe.Loader.getSprite('common', 'door')
        
    def draw(self):
        pos = globe.Camera.getDrawPos(self.pos)
        super().draw(pos)
        
    def playerCollide(self, playerObj):
        key_states = pygame.key.get_pressed()
        if(key_states[pygame.K_DOWN]):
        
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
                globe.Area.changeRoom(room)
        
            playerObj.spawn((newX,newY))