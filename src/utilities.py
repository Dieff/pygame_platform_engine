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
        self.state = 'nominal'
    def getState(self):
        return self.state
    def setState(self, newState):
        self.state = newState