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
                t = Tile((tileX, tileY),(rCounter, cCounter), [tData['data']], False, tData)
                self.tiles[rCounter].append(t)
                cCounter += 1
            rCounter += 1
            cCounter = 0
            
    def load(self):
        self.roomData = globe.Loader.getData(self.areaId, 'Rooms', self.roomId)
        print(self.roomData)
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