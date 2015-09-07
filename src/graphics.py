from src.constants import *
import src.globe as globe

class Animation:
    def __init__(self, frames, duration, startingLocation, scrollObj=False):
        self.frames = frames
        self.frameDuration = duration
        self.timeCounter = 0
        self.curSpriteIndex = 0
        self.loc = startingLocation
        self.scrollObj = scrollObj
        
    def getCurSprite(self):
        return self.frames[self.curSpriteIndex]
        
    def update(self, elapsed_time, loc=False):
        self.timeCounter += elapsed_time
        if(loc):
            self.loc = loc
        
        if(self.timeCounter > self.frameDuration and len(self.frames) > 0):
            self.curSpriteIndex += 1
            if(self.curSpriteIndex == len(self.frames)):
                self.curSpriteIndex = 0
        
    def draw(self):
        if(self.scrollObj):
            pos = globe.Camera.getDrawPos(self.loc)
        else:
            pos = self.loc
        if(globe.Camera.amOnScreen(pos)):
            DISPLAYSURF.blit(self.getCurSprite(), pos);
        
        
class Camera:
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        globe.Updater.registerUpdatee(self.update)
        self.idealPlayerPos = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.realPlayerPos = self.idealPlayerPos
        self.scollingX = False
        self.scrollingY = False
        
    def start(self, player):
        self.player = player
        self.oldPos = player.pos
        
    def update(self, elapsed_time):
        #Handling x scroll
        if(globe.Room.getWidth() <= WINDOWWIDTH):
            self.realPlayerPos = (self.player.pos[0], self.realPlayerPos[1])
        elif(self.player.pos[0] > WINDOWWIDTH/2 and self.player.pos[0] <= globe.Room.getWidth() - (WINDOWWIDTH /2)):
            self.offsetX = self.player.pos[0] - self.idealPlayerPos[0]
            self.realPlayerPos = (self.idealPlayerPos[0], self.realPlayerPos[1])
        else:
            self.realPlayerPos = (self.player.pos[0], self.realPlayerPos[1])
            if(self.player.pos[0] > globe.Room.getWidth() - (WINDOWWIDTH /2)):
                self.realPlayerPos = (WINDOWWIDTH - (globe.Room.getWidth() - self.player.pos[0]),self.realPlayerPos[1])
                self.offsetX = globe.Room.getWidth() - (WINDOWWIDTH)
            else:
                self.offsetX = 0
            
        #Handling Y scroll    
        if(globe.Room.getHeight() <= WINDOWHEIGHT):
            self.realPlayerPos = (self.realPlayerPos[0], self.player.pos[1])
        elif(self.player.pos[1] > WINDOWHEIGHT/2 and self.player.pos[1] <= globe.Room.getHeight() - (WINDOWHEIGHT /2)):    
            self.offsetY = self.player.pos[1] - self.idealPlayerPos[1]
            self.realPlayerPos = (self.realPlayerPos[0], self.idealPlayerPos[1])
        else:
            self.realPlayerPos = (self.realPlayerPos[0], self.player.pos[1])
            if(self.player.pos[1] > globe.Room.getHeight() - (WINDOWHEIGHT /2)):
                self.realPlayerPos = (self.realPlayerPos[0], (WINDOWHEIGHT - (globe.Room.getHeight() - self.player.pos[1])))
                self.offsetY = globe.Room.getHeight() - (WINDOWHEIGHT)
            else:
                self.offsetY = 0
        
    def getDrawPos(self, pos):
        return (pos[0] - self.offsetX, pos[1] - self.offsetY)
    
    def getPlayerDrawPos(self):
        return self.realPlayerPos
    
    def fillScreen(self):
        DISPLAYSURF.fill(BLACK)
        
    def amOnScreen(self, position, tolerance = TILE_SIZE):
        if(position[0] > WINDOWWIDTH + tolerance):
            return False
        if(position[1] > WINDOWHEIGHT + tolerance):
            return False
        return True