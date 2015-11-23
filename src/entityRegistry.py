from src.entity import *
from src.entities.doors import *
from src.characters.bat import *
from src.characters.spike import *

Entities = {
            "door":Door,
            "invisiDoor":InvisiDoor ,
            "bat":Bat,
            "spike":Spike
            }

def getEntity(entityName):
    if(not(entityName in Entities)):
        print('Entity not found. Name: ', entityName)
        return Entity
    return Entities[entityName]()