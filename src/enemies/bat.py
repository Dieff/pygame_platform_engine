from src.enemies.enemy import *
from src.constants import *
import src.globe as globe
import math

class Bat(Enemy):
    def __init__(self):
        super().__init__()
        self.hitDamage = 1
        self.addSprite('fly-left', globe.Loader.getSprite('common', 'bat-fly-left'))
        self.addSprite('fly-right', globe.Loader.getSprite('common', 'bat-fly-right'))
        self.curSprite = self.getSprite('fly-left')
        self.funcX = 0
        self.data = {}
        self.data['movement-amplitude'] = 100
        self.data['movement-duration'] = 5000
        self.width = 20
        self.height = 20
        
    def addData(self, data):
        if(not('action' in data)):
            data['action'] = {}
        if(not('movement-amplitude' in data['action'])):
            data['action']['movement-amplitude'] = self.data['movement-amplitude']
        if(not('movement-duration' in data['action'])):
            data['action']['movement-duration'] = self.data['movement-duration']
        super().addData(data)
        
        
    def update(self, elapsed):
        self.funcX += elapsed
        
        amp = self.data['action']['movement-amplitude']
        
        period = (2*math.pi/self.data['action']['movement-duration'])
        
        x=self.funcX
        
        yVel = period*amp*math.cos(period*self.funcX)
        
        self.vel = (self.vel[0], yVel)
        super().update(elapsed)
        
        if(self.npos.top < self.data['posY'] - self.data['action']['movement-amplitude']):
            self.npos = self.pos
        
        self.pos = self.npos