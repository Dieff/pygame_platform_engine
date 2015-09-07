import json
import pygame
from src.constants import *
import os.path

class Loader:
    def __init__(self):
        self.data = dict()
        self.finishedAreas = []
        
    def loadJson(self, jsonPath):
        jFile = open(jsonPath,'r')
        jData = json.loads(jFile.read())
        jFile.close()
        return jData
    
    def loadImage(self, imagePath):
        img = pygame.image.load(imagePath).convert()
        img.set_colorkey(TRANSPARENT)
        return img
    
    def LoadDataFiles(self, type, areaId, path):
        jsonData = self.loadJson(os.path.join(path, type + '.json'))
        for item in jsonData:
            item['type'] = type
            
            #handle loading of data and make sure that any missing properties will be defined for later use
            if(type == 'Tiles'):
                item['data'] = []
                for frame in item['files']:
                    item['data'].append(self.loadImage(os.path.join(path, frame)))
                
                if(not('animationTime' in item)):
                    item['animationTime'] = 1
                
                
            elif(type == 'Sprites'):
                item['data'] = self.loadImage(os.path.join(path, item['file']))
            elif(type == 'Rooms'):
                item['data'] = self.loadJson(os.path.join(path, item['file']))
            
            self.data[areaId + '.' + type + '.' + item['name']] = item
            #print(self.data)
    
    def loadArea(self, area):        
        curPath = os.path.join(PATH_TO_AREAS, area)
        
        if(not(os.path.exists(curPath))):
           return False
       
        if(os.path.exists(os.path.join(curPath, 'Tiles'))):
           self.LoadDataFiles('Tiles', area, os.path.join(curPath, 'Tiles'))
           
        if(os.path.exists(os.path.join(curPath, 'Rooms'))):
           self.LoadDataFiles('Rooms', area, os.path.join(curPath, 'Rooms'))
           
        if(os.path.exists(os.path.join(curPath, 'Sprites'))):
           self.LoadDataFiles('Sprites', area, os.path.join(curPath, 'Sprites'))
           
        if(os.path.exists(os.path.join(curPath, 'Sounds'))):
           self.LoadDataFiles('Sounds', area, os.path.join(curPath, 'Sounds'))
           
        if(os.path.exists(os.path.join(curPath, 'Music'))):
           self.LoadDataFiles('Music', area, os.path.join(curPath, 'Music'))
       
        self.finishedAreas.append(area)
        
    def LoadAreas(self, areas):
        for area in areas:
            self.loadArea(area)
        
    def getData(self, area, type, name):
        done = False
        for item in self.finishedAreas:
            if(item == area):
                done = True
                
        if(not(done)):
            self.loadArea(area)
            
        queryString = area + '.' + type + '.' + name
        
        if(queryString in self.data):
            return self.data[queryString]
        else:
            return False
        
    def getTile(self, code):
        for key in self.data:
            if(self.data[key]['type'] == 'Tiles'):
                if(self.data[key]['code'] == code):
                    return self.data[key]
                
        return self.getData('Default', 'Tiles', 'blank')

        