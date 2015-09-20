import json
import pygame
from src.constants import *
from src.entity import *
from src.graphics import *
import src.entityRegistry


import os.path

class Loader:
    def __init__(self):
        self.data = dict()
        self.finishedAreas = []
      
    def getNewEntity(self, entitiyId):
        return src.entityRegistry.getEntity(entitiyId)
        
    def loadJson(self, jsonPath):
        jFile = open(jsonPath,'r')
        jData = json.loads(jFile.read())
        jFile.close()
        return jData
    
    def loadImage(self, imagePath):
        img = pygame.image.load(imagePath).convert()
        img.set_colorkey(TRANSPARENT)
        return img
    
        
    def splitSurface(self, surface, w, h):
        '''This function splits a pygame surface into a list of smaller subsurfaces.
        The purpose of this function is to provide easy access to individual images
        in a larger imageset surface.
        
        The subsurface indexes in an imageset of 3 columns by 2 rows are distributed
        in the following manner:
        0 1 2
        3 4 5
        '''
        #print('height!!', surface.get_height())
        #print('width', surface.get_width())
    
        result = []
        for y in range(0, surface.get_height(), h):
            for x in range(0, surface.get_width(), w):
                result.append(surface.subsurface((x, y), (w, h)))
        return result
    
    def LoadDataFiles(self, type, areaId, path):
        jsonData = self.loadJson(os.path.join(path, type + '.json'))
        for item in jsonData:
            item['type'] = type
            
            #handle loading of data and make sure that any missing properties will be defined for later use
            if(type == 'Tiles'):
                if(not('animationTime' in item)):
                    item['animationTime'] = 1
                if(not('Default' in item)):
                    item['Default'] = False
                if(not(item['Default'])):  
                    item['data'] = []
                    mainImage = self.loadImage(os.path.join(path, item['file']))
                    splitImage = self.splitSurface(mainImage, TILE_SIZE, TILE_SIZE)
                    data = []
                
                    cols = mainImage.get_width()/TILE_SIZE
                
                    for frame in item['frames']:
                        xIndex = frame['rowX']
                        yIndex = frame['rowY']
                        data.append(splitImage[int(yIndex*cols + xIndex)])
                
                    item['data'] = data
                
                
            elif(type == 'Sprites'):
                mainImage = self.loadImage(os.path.join(path, item['file']))
                sizeX = item['frameWidth']
                sizeY = item['frameHeight']
                splitImage = self.splitSurface(mainImage, sizeX, sizeY)
                #rows = mainImage.get_height()/sizeX
                cols = mainImage.get_width()/sizeY
                
                #print(rows)
                #print(cols)
                
                data = []
                for sprite in item['frames']:
                    xIndex = sprite['rowX']
                    yIndex = sprite['rowY']
                    data.append(splitImage[int(yIndex*cols + xIndex)])
                    
                item['data'] = data
                
                if(not('animationTime' in item)):
                    item['animationTime'] = 1
                    
                
                
            elif(type == 'Rooms'):
                item['data'] = self.loadJson(os.path.join(path, item['file']))
                
                #print(item['data'])
                
                if(not('bgConstantScroll' in item['data'])):
                    item['data']['bgConstantScroll'] = False
                if(not('bgScollFactorX' in item['data'])):
                    item['data']['bgScollFactorX'] = 3 
                if(not('brScrollFactorY' in item['data'])):
                    item['data']['brScrollFactorY'] = 3
                if(not('bgTileSize' in item['data'])):
                    item['data']['bgTileSize'] = TILE_SIZE
                    
                if(not('entities' in item['data'])):
                    item['data']['doEntities'] = False
                else:
                    item['data']['doEntities'] = True
            
            self.data[areaId + '.' + type + '.' + item['name']] = item
            #print(self.data)
    
    def loadArea(self, area):        
        curPath = os.path.join(PATH_TO_AREAS, area)
        
        if(not(os.path.exists(curPath))):
           return False
       
        if(os.path.exists(os.path.join(curPath, 'Tiles'))):
           self.LoadDataFiles('Tiles', area, os.path.join(curPath, 'Tiles'))
           
        if(os.path.exists(os.path.join(curPath, 'Sprites'))):
           self.LoadDataFiles('Sprites', area, os.path.join(curPath, 'Sprites'))
           
        if(os.path.exists(os.path.join(curPath, 'Sounds'))):
           self.LoadDataFiles('Sounds', area, os.path.join(curPath, 'Sounds'))
           
        if(os.path.exists(os.path.join(curPath, 'Music'))):
           self.LoadDataFiles('Music', area, os.path.join(curPath, 'Music'))
           
        if(os.path.exists(os.path.join(curPath, 'Rooms'))):
           self.LoadDataFiles('Rooms', area, os.path.join(curPath, 'Rooms'))
       
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
            print('DATA NOT FOUND ', queryString)
            return False
        
    def getTile(self, code):
        for key in self.data:
            if(self.data[key]['type'] == 'Tiles'):
                if(self.data[key]['code'] == code):
                    return self.data[key]
                
        return self.getData('Default', 'Tiles', 'blank')
    
    def getSprite(self, area, name):
        spriteData = self.getData(area, 'Sprites', name)
        return Animation(spriteData['data'], spriteData['animationTime'], (0,0))

        