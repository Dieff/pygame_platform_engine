class Updater:
    def __init__(self):
        self.updatees = []
        self.drawees = []
        
    def registerUpdatee(self, updateFunc):
        self.updatees.append(updateFunc)
        
    def removeUpdatee(self, updateFunc):
        self.updatees.remove(updateFunc)
        
    def registerDrawee(self, drawFunc):
        self.drawees.append(drawFunc)
        
    def removeUpdatee(self, drawFunc):
        self.drawees.remove(drawFunc)
        
    def update(self, elapsedTime):
        for updateFunction in self.updatees:
            updateFunction(elapsedTime)
            
    def draw(self):
        for drawFunc in self.drawees:
            drawFunc()
            
    