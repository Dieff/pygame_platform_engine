import src.globe as globe
from src.room import *
from src.constants import *
from src.utilities import *
from src.hud import *
import pygame

class Area:
    def __init__(self):
        self.areaId = ''
        self.roomId = ''
        self.Room = Room()
        globe.Room = self.Room
        
        self.newRoom = False
        self.fadingIn = False
        self.fadingOut = False
        
        self.timer = Timer()
        
    def getRoomId(self):
        return self.roomId
        
    def getRoom(self):
        return self.Room    
    
    def loadArea(self, areaId):
        self.areaId = areaId
        globe.Loader.loadArea(areaId)
        
    def changeRoom(self, roomId=False):
        if(roomId):
            self.roomId = roomId
        elif(self.newRoomId):
            self.roomId = roomId
            
        self.Room.load(self.areaId, self.roomId)
        globe.Hud.displayText(1000, self.Room.getDisplayName(), (WINDOWWIDTH / 3, 100))
        
    def initialCinematicLoad(self, newRoomId, newPlayerLocation):
        self.newRoomId = newRoomId
        self.cine = True
        self.npl = newPlayerLocation
        globe.State.pauseGame()
        self.fadingIn = True
        self.timer.set(200)
        self.timer.start()
        globe.Updater.registerDrawee(self.transition, ['nominal','paused'],[], 'hud')
        self.changeRoom(self.newRoomId)
        if(self.npl):
            globe.Updater.spawnPlayer(self.npl)
        
    def cinematicLoad(self, newRoomId, newPlayerLocation):
        self.newRoomId = newRoomId
        self.cine = True
        self.npl = newPlayerLocation

        globe.State.pauseGame()
        self.fadingOut = True
        self.fadingIn = False
        
        self.timer.set(200)
        self.timer.start()
        globe.Updater.registerDrawee(self.transition, ['nominal','paused'],[], 'hud')
        
    def transition(self):
        if(self.timer.isDone()):
            if(self.fadingOut):
                #half way done
                self.fadingOut = False
                self.fadingIn = True
                self.changeRoom(self.newRoomId)
                DISPLAYSURF.fill(BLACK)
                if(self.npl):
                    globe.Updater.spawnPlayer(self.npl)
                self.timer.start()
            elif(self.fadingIn):
                #all done
                #I fucking love python. This function removes itself from the draw queue
                globe.Updater.removeDrawee(self.transition)
                self.fadingIn = False
                globe.State.unPauseGame()
        else:
            elapsed = self.timer.getElapsed()
            numberOfPanels = 10
            completeRatio = elapsed/self.timer.getMax()
            panelDistance = int(WINDOWWIDTH/numberOfPanels)
            if(self.fadingOut):
                rectSize = completeRatio*panelDistance
                for i in range(numberOfPanels):
                    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(i*panelDistance, 0, rectSize, WINDOWHEIGHT))
            else:
                for i in range(numberOfPanels):
                    xOrd = i*panelDistance + (panelDistance*completeRatio)
                    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(xOrd, 0, ((i+1)*panelDistance)-xOrd, WINDOWHEIGHT))
            
        