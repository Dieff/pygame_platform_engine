import math
import src.globe as globe

class fps_meter:
    def __init__(self):
        self.last_measurements = []
        self.curFPS = '10'
        self.updateCounter = 0
    def update(self, newTick):
        self.updateCounter = self.updateCounter + 1
        self.last_measurements.append(newTick)
        if(len(self.last_measurements) > 10):
            self.last_measurements.pop(0)
        if(self.updateCounter == 10):
            self.curFPS = self.calculateFPS()
            self.updateCounter = 0

    def updateByMilli(self, elapsedMilliSeconds):
        self.update(1000/elapsedMilliSeconds)
    def calculateFPS(self):
        counter = 0
        total = 0
        for mment in self.last_measurements:
            total = total + mment
            counter = counter + 1
        return str(round(total/counter))
    def getFPS(self):
        return self.curFPS

class State:
    def __init__(self):
        self.states = []
        
    def getStates(self):
        return self.states
    
    def hasState(self, state):
        if(state in self.states):
            return True
        else:
            return False
        
    def addState(self, newState):
        if(not(self.hasState(newState))):
            self.states.append(newState)
        
    def removeState(self, state):
        self.states.remove(state)
        
    def pauseGame(self):
        self.addState('paused')
        
    def unPauseGame(self):
        self.removeState('paused')
        
class Timer:
    def __init__(self, time=False, onComplete=False):
        globe.Updater.registerUpdatee(self.update)
        self.curTime = 0
        self.goalTime = 0
        self.onComplete = False
        self.isRunning = False
        self.done = False
        if(time):
            self.set(time, onComplete)
            self.start()
        
    def set(self, time, onComplete=False):
        self.curTime = 0
        self.goalTime = time
        self.onComplete=onComplete
        self.isRunning = False
        self.done = False
        
    def update(self, elapsed):
        if(self.isRunning):
            self.curTime += elapsed
            if(self.done):
                return True
            if(self.curTime > self.goalTime):
                self.done = True
                #globe.Updater.removeUpdatee(self.update)
                if(self.onComplete):
                    self.onComplete()
                    
    def start(self):
        self.isRunning = True
        self.curTime = 0
        self.done = False
        
    def isDone(self):
        return self.done
    
    def pause(self):
        self.isRunning = False
        
    def unPause(self):
        self.isRunning = True
        
    def getElapsed(self):
        return self.curTime
    
    def getMax(self):
        return self.goalTime
        
def getDistance(pointA, pointB):
    dX = abs(pointB[0] - pointA[0])
    dY = abs(pointB[1] - pointA[1])
    return math.sqrt(dX**2 + dY**2)