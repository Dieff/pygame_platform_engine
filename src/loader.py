import json
import pygame
from src.constants import *

class Loader:
    def getJson(self, jsonPath):
        jFile = open(jsonPath,'r')
        jData = json.loads(jFile.read())
        jFile.close()
        return jData
    
    def loadImage(self, imagePath):
        img = pygame.image.load(imagePath).convert()
        img.set_colorkey(TRANSPARENT)
        return img
    
    def load(self):
        print(self.getJson('Data/Default/Tiles/Tiles.json'))