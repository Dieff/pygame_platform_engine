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
        
    def populateTiles(self):
        rows = self.roomData['data']['tiles']
        rCounter = 0
        cCounter = 0
        for row in rows:
            self.tiles.append([])
            for tile in row:
                tData = globe.Loader.getTile(tile)
                tileX = cCounter*TILE_SIZE
                tileY = rCounter*TILE_SIZE
                t = Tile((tileX, tileY),(rCounter, cCounter), tData['data'], False, tData, tData['animationTime'])
                self.tiles[rCounter].append(t)
                cCounter += 1
            rCounter += 1
            cCounter = 0
            
    def load(self):
        self.roomData = globe.Loader.getData(self.areaId, 'Rooms', self.roomId)
        self.populateTiles()
        
    def update(self, elapsed_time):
        for row in self.tiles:
            for tile in row:
                tile.update(elapsed_time)
        
    def draw(self):
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
        