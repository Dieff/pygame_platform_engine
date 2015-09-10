import src.globe as globe
from src.constants import *
from src.tile import *

class Room:
    def __init__(self, areaId, roomId):
        self.areaId = areaId
        self.roomId = roomId
        globe.Updater.registerDrawee(self.draw)
        globe.Updater.registerUpdatee(self.update)
        self.tiles = []
        self.backgroundTiles = []
        self.hasBackground = False
        
    def populateTiles(self):
        rows = self.roomData['data']['tiles']
        rCounter = 0
        cCounter = 0
        for row in rows:
            self.tiles.append([])
            for tile in row:
                tileData = globe.Loader.getTile(tile)
                tileX = cCounter*TILE_SIZE
                tileY = rCounter*TILE_SIZE
                if(tileData['Default']):
                    t = LevelBlock((tileX, tileY),(rCounter, cCounter), tileData)
                else:
                    t = Tile((tileX, tileY),(rCounter, cCounter), tileData, tileData['data'], False, tileData['animationTime'])
                    
                
                self.tiles[rCounter].append(t)
                cCounter += 1
            rCounter += 1
            cCounter = 0
            
    def populateBackgroundTiles(self):
        sets = self.roomData['data']['bgTiles']
        rCounter = 0
        cCounter = 0
        for row in sets:
            self.backgroundTiles.append([])
            for tile in row:
                tileData = globe.Loader.getTile(tile)
                tileX = cCounter*TILE_SIZE
                tileY = rCounter*TILE_SIZE
                newTile = BackgroundTile((rCounter, cCounter),(tileX,tileY),tileData['data'],tileData['animationTime'])
                self.backgroundTiles[rCounter].append(newTile)
                cCounter += 1
            rCounter+=1
            cCounter = 0
            
    def load(self):
        self.roomData = globe.Loader.getData(self.areaId, 'Rooms', self.roomId)
        self.populateTiles()
        if('bgTiles' in self.roomData['data']):
            if(len(self.roomData['data']['bgTiles'])>0):
                self.hasBackground = True
                self.populateBackgroundTiles()
        
    def update(self, elapsed_time):
        if(self.hasBackground):
            for row in self.backgroundTiles:
                for tile in row:
                    tile.update(elapsed_time)
        for row in self.tiles:
            for tile in row:
                tile.update(elapsed_time)
        
    def draw(self):
        if(self.hasBackground):
            for row in self.backgroundTiles:
                for tile in row:
                    tile.draw()
        for row in self.tiles:
            for tile in row:
                tile.draw()
                
    def getHeight(self):
        return len(self.tiles)*TILE_SIZE
        
    def getWidth(self):
        return len(self.tiles[0])*TILE_SIZE
    
    def getTile(self, tileIndex):
        if(tileIndex[0] < 0 or tileIndex[1]<0):
            return False
        if(tileIndex[1] < len(self.tiles) and tileIndex[0] < len(self.tiles[0])):
            return self.tiles[tileIndex[1]][tileIndex[0]]
        return False
    
    #returns a subset of tiles around a point, allowing for more efficient collision detection
    def getTilesAround(self, pos, TilesAround=2):
        xBot = int(TILE_SIZE * round(float(pos[0])/TILE_SIZE) / TILE_SIZE) - 2
        xTop = xBot + 5
        yBot = int(TILE_SIZE * round(float(pos[1])/TILE_SIZE) / TILE_SIZE) - 2
        yTop = yBot + 5
        
        if(xBot < 0):
            xBot = 0
        if(yBot < 0):
            yBot = 0
            
        if(yTop > len(self.tiles)):
            yTop = len(self.tiles)
        if(yTop < 2):
            yTop = 2
        if(xTop > len(self.tiles[0])):
            xTop = len(self.tiles[0])
        if(xTop < 2):
            xTop = 2
            
        rets = []
        for item in self.tiles[yBot:yTop]:
            rets += item[xBot:xTop]
        return rets
    
    def getPref(self, pref):
        if(not(pref in self.roomData['data'])):
            if(not(pref in self.roomData)):
                return False
            else:
                return self.roomData[pref]
        else:
            return self.roomData['data'][pref]
        