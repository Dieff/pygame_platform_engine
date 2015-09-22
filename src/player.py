from src.entity import *
from src.update import *
from src.constants import *
from src.utilities import *
from src.graphics import *
import pygame
import src.globe as globe
import math

class Player(HealthEntity):
    def __init__(self):
        super().__init__()
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['room-transition', 'paused'])
        globe.Updater.registerDrawee(self.draw)
        globe.Updater.registerRoomCollidee(self, ['nominal'], ['room-transition', 'paused'])
        
        self.width = 28
        self.height = 28
        
        self.jumpJuice = 0
        self.jumpCounter = 0
        
        self.old_states = dict()
        
        self.running = False
        
        self.maxJump = 230 #in milliseconds how long can you jump
        self.maxJumpTime = 50 #in milliseconds the time you can still jump after leaving ground
        self.jumpAcceleration = 0.02 #in pixels/ms^2
        
        self.gravity = 0.0015 #in pixels/ms^2
        
        self.yspeedLimit = 0.4#in pixels/ms
        self.xSpeedLimit = 0.2#in pixels/ms
        
        self.friction = 0.0015
        
        self.xAcceleration = 0.05#in pixels/ms^s
        
        self.hurtTime = 750 #in milliseconds
        
        self.colRecursionDepth = 0
        
        self.addSprite('stand-left', globe.Loader.getSprite('common', 'quote-stand-left'))
        self.addSprite('stand-right', globe.Loader.getSprite('common', 'quote-stand-right'))
        self.addSprite('walk-left', globe.Loader.getSprite('common', 'quote-walk-left'))
        self.addSprite('walk-right', globe.Loader.getSprite('common', 'quote-walk-right'))
        self.addSprite('jumping-right', globe.Loader.getSprite('common', 'quote-jumpUp-right'))
        self.addSprite('falling-right', globe.Loader.getSprite('common', 'quote-jumpDown-right'))
        self.addSprite('jumping-left', globe.Loader.getSprite('common', 'quote-jumpUp-left'))
        self.addSprite('falling-left', globe.Loader.getSprite('common', 'quote-jumpDown-left'))
        self.addSprite('hurt-left', globe.Loader.getSprite('common', 'quote-hurt-left'))
        self.addSprite('hurt-right', globe.Loader.getSprite('common', 'quote-hurt-right'))
        
        self.orientation = 'left'
        self.action = 'stand'
        
        self.curSprite = self.getSprite()
        
        self.onBottom = False
        self.oldOnBottom = False
        self.elapsed = 0
        
        self.isJumping = False
        
        self.invuln = False
        
        self.maxHealth = 100
        self.health = 100
                
    def getSprite(self):
        queryString = (self.action + '-' + self.orientation)
        return super().getSprite(queryString)
                
    def update(self, elapsedTime):
        self.elapsed = elapsedTime
        self.curSprite.update(elapsedTime)
            
        key_states = pygame.key.get_pressed()
        
        self.vel = (self.vel[0],self.vel[1] + self.gravity*elapsedTime)
        
        self.running = False
            
        if(key_states[pygame.K_UP]):
            self.vel = (self.vel[0], self.vel[1]-(0.1*elapsedTime))
            
        if(key_states[pygame.K_LEFT]):
            self.vel = (self.vel[0]-self.xAcceleration*elapsedTime, self.vel[1])
            self.running = True
            self.orientation = 'left'
            
        if(key_states[pygame.K_RIGHT]):
            self.vel = (self.vel[0]+self.xAcceleration*elapsedTime, self.vel[1])
            self.running = True
            self.orientation = 'right'
            
        if(key_states[pygame.K_f]):
            if(self.old_states[pygame.K_f]):
                self.jumpJuice = 0
                self.jumpCounter -= elapsedTime
                if(self.jumpCounter > 0 and self.jumpJuice <= 0):
                    self.isJumping = True
                    self.vel = (self.vel[0], self.vel[1]-(self.jumpAcceleration*elapsedTime)) #* self.jumpCounter)
                '''else:
                    key_states[pygame.K_f]'''
            elif(self.jumpJuice > 0):
                self.jumpCounter = self.maxJump
                self.jumpJuice = 0
                self.isJumping = True
        #this prevents double jump
        else:
            self.jumpCounter = 0
            
        self.jumpJuice -= elapsedTime

        if(self.vel[0] > self.xSpeedLimit):
            self.vel = (self.xSpeedLimit, self.vel[1])
        if(self.vel[0] < self.xSpeedLimit*-1):
            self.vel = (self.xSpeedLimit*-1, self.vel[1])
        if(self.vel[1] > self.yspeedLimit):
            self.vel = (self.vel[0], self.yspeedLimit)
        if(self.vel[1] < self.yspeedLimit*-1):
            self.vel = (self.vel[0], self.yspeedLimit*-1)
            
            
        self.setTempPosition(elapsedTime)
        self.old_states = []
        self.old_states = key_states
        
        self.colRecursionDepth = 0
        
        self.action = 'stand'
        if(self.invuln):
            self.action = 'hurt'
        elif(self.isJumping):
            self.action = 'jumping'
        elif(self.running and self.action == 'stand'):
            self.action = 'walk'

        if(self.getHealth() <= 0):
            self.kill()
        
    def draw(self):
        self.curSprite = self.getSprite()
        pdp = globe.Camera.getPlayerDrawPos()
        super().draw(pdp)
        
    def tileCollide(self, tiles):
        #A shitty fix for collision bugs
        #make this better!!!
        self.colRecursionDepth +=1
        if(self.colRecursionDepth > 25):
            print('ERROR caught in collision detection. crashing prevented. velocity killed')
            self.npos = self.pos
            self.setPermanentPosition()
            self.vel = (0,0)
            return True
        
        colHappened = False
        
        self.getCollidePoints()
        currect = self.npos
        for item in tiles:
            ir = item.getRect()
            if(currect.colliderect(ir)):
                if(item.properties['solid']):
                    self.getCollidePoints()
                    tileCenter = (ir.center)
                    #Creates an array of the distances between collidepoints and tile center
                    distances = [getDistance(self.top, tileCenter),getDistance(self.bottom, tileCenter),getDistance(self.left, tileCenter),getDistance(self.right,tileCenter)]
                    #determines smallest distance (index of smallest number in distances)
                    smallestIndex = distances.index(min(distances))
                    #does shit based on the collision side
                    if(smallestIndex == 0):
                        #Top collision
                        if(not(item.canCollisionOccur('top'))):
                            continue
                        #print('TOP')
                        dY = abs(self.npos.top - self.pos.top)
                        badY = abs(ir.bottom - self.npos.top)
                        okY = abs(dY - badY)
                        self.npos = pygame.Rect(self.npos.left, self.pos.top-okY, self.width, self.height)
                        self.vel = (self.vel[0], 0)
                            
                        self.jumpCounter = 0
                        self.jumpJuice = 0
                        
                        if(abs(self.npos.top - self.pos.top) >= TILE_SIZE):
                            print('ERROR in top side collision detection')
                            
                        colHappened = True

                    elif(smallestIndex == 1):
                        #Bottom collision
                        if(not(item.canCollisionOccur('bottom'))):
                            continue
                        #print('BOTTOM')
                        dY = abs(self.npos.bottom - self.pos.bottom)
                        badY = abs(ir.top - self.npos.bottom)
                        okY = abs(dY - badY)
                        self.npos = pygame.Rect(self.npos.left, self.pos.top+okY, self.width, self.height)
                        
                        
                        if(abs(self.vel[0]) >= self.friction*self.elapsed and not(self.running)):
                            if(self.vel[0] > 0):
                                self.vel = (self.vel[0] - self.friction*self.elapsed, self.vel[1])
                            else:
                                self.vel = (self.vel[0] + self.friction*self.elapsed, self.vel[1])
                        elif(not(self.running)):
                            self.vel = (0, self.vel[1])
                            
                        self.jumpJuice = self.maxJumpTime

                        colHappened = True
                        self.onBottom = True
                        self.isJumping = False
                        
                    elif(smallestIndex == 2):
                        #Left collision
                        if(not(item.canCollisionOccur('left'))):
                            continue
                        #print('LEFT')
                        dX = abs(self.npos.left - self.pos.left)
                        badX = abs(ir.right - self.npos.left)
                        okX = abs(dX - badX)
                        self.npos = pygame.Rect(self.pos.left-okX, self.npos.top, self.width, self.height)
                        self.vel = (0, self.vel[1])
                        
                        if(abs(self.npos.left - self.pos.left)>=TILE_SIZE):
                            print('ERROR in left side collision detection')
                        
                        colHappened = True
                        
                    else:
                        #Right Collision
                        if(not(item.canCollisionOccur('right'))):
                            continue
                        #print('RIGHT')
                        dX = abs(self.npos.right - self.pos.right)
                        badX = abs(ir.left - self.npos.right)
                        okX = abs(dX - badX)
                        self.npos = pygame.Rect(self.pos.left+okX, self.npos.top, self.width, self.height)
                        self.vel = (0, self.vel[1])
                    
                        if(abs(self.npos.left - self.pos.left)>=TILE_SIZE):
                            print('ERROR in right side collision detection')
                            
                        colHappened = True
                        
            #we run the tile collision algorithm until no more collisions are detected
            #occasionally things break and we get infinite recursion
            #this helps debug things
            if(colHappened):
                try:
                    self.tileCollide(tiles)
                except RuntimeError:
                    print('Error Caught in collision detection', self.colRecursionDepth)
                    return True
                self.colHappened = False
                        
                
        
        self.setPermanentPosition()
        
    def setInvincible(self):
        self.invuln = True
        
    def setMortal(self):
        self.invuln = False
        
    def hurt(self, damage, enemyPosition):
        if(not(self.invuln)):
            super().hurt(damage)
            self.setInvincible()
            self.hTimer = Timer(self.hurtTime, self.setMortal)
            enemyX = enemyPosition[0]
            myX = self.pos.center[0]
            if(myX - enemyX <= 0):
                self.vel = (-1*self.xSpeedLimit, -self.yspeedLimit)
            else:
                self.vel = (self.xSpeedLimit, -self.yspeedLimit)
            
        