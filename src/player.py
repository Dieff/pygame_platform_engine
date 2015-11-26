from src.entity import *
from src.update import *
from src.constants import *
from src.utilities import *
from src.graphics import *
from src.menus import *
from src.accessories import *
import pygame
import src.globe as globe
import math

class Player(HealthEntity):
    def __init__(self):
        super().__init__()
        self.entityType = 'player'
        
        self.width = 22
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
        
        self.addSprite('stand-left', globe.Loader.getSprite('common', 'protagonist-stand-left'))
        self.addSprite('stand-right', globe.Loader.getSprite('common', 'protagonist-stand-right'))
        self.addSprite('jumping-right', globe.Loader.getSprite('common', 'protagonist-jumpUp-right'))
        self.addSprite('jumping-left', globe.Loader.getSprite('common', 'protagonist-jumpUp-left'))
        self.addSprite('hurt-left', globe.Loader.getSprite('common', 'protagonist-hurt-left'))
        self.addSprite('hurt-right', globe.Loader.getSprite('common', 'protagonist-hurt-right'))
        self.addSprite('falling-right', globe.Loader.getSprite('common', 'protagonist-falling-right'))
        self.addSprite('falling-left', globe.Loader.getSprite('common', 'protagonist-falling-left'))
        self.addSprite('walk-left', globe.Loader.getSprite('common', 'protagonist-running-left'))
        self.addSprite('walk-right', globe.Loader.getSprite('common', 'protagonist-running-right'))
        self.addSprite('start-left', globe.Loader.getSprite('common', 'protagonist-starting-left'))
        self.addSprite('start-right', globe.Loader.getSprite('common', 'protagonist-starting-right'))
        
        self.orientation = 'left'
        self.action = 'stand'
        
        self.runTime = 0
        
        self.curSprite = self.getSprite()
        
        self.onBottom = False
        self.oldOnBottom = False
        self.elapsed = 0
        
        self.isJumping = False
        
        self.fallingTime = 0
        
        self.invuln = False
        
        self.maxHealth = 100
        self.health = 100
        
        self.weapon = Gun()
        
        self.register()
        
        self.badTiles = []
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'], ['room-transition', 'paused'])
        globe.Updater.registerDrawee(self.draw, ['nominal'], [], 'player')
        globe.Updater.registerRoomCollidee(self, ['nominal'], ['room-transition', 'paused'])
        globe.Updater.addCollideableEntity(self, ['nominal'], ['room-transition', 'paused'])
                
    def getSprite(self):
        queryString = (self.action + '-' + self.orientation)
        return super().getSprite(queryString)
             
    def spawn(self, pos):
        super().spawn(pos)
        self.weapon.cleanse()
                
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
        
        if(self.running):
            self.runTime += elapsedTime
        else:
            self.runTime = 0
        
        self.action = 'stand'
        if(self.fallingTime > 100):
            self.action = 'falling'
        if(self.invuln):
            self.action = 'hurt'
        elif(self.isJumping):
            self.action = 'jumping'
            if(self.vel[1] > 0):
                self.action = 'falling'
        elif(self.running and self.action == 'stand'):
            self.action = 'walk'
            if(self.runTime < 400):
                self.action = 'start'

        if(self.getHealth() <= 0):
            self.kill()
        
        if(self.vel[1] > 0):
            self.fallingTime += elapsedTime
        else:
            self.fallingTime = 0
        
        self.weapon.update(elapsedTime, self.orientation, self.pos)
        
    def draw(self):
        self.curSprite = self.getSprite()
        pdp = globe.Camera.getPlayerDrawPos()
        super().draw(pdp)
        self.weapon.draw(pygame.Rect(pdp, (1,1)))
        
        '''for item in self.badTiles:
            print(globe.Camera.getDrawPos(item))
            pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(globe.Camera.getDrawPos(item), (32,32)))'''
        
    def tileCollide(self, tiles):
        '''experimental algorithm november 25
           step 1:
            for each side of a potential tile solve for the intersection between side(line segment) and velocity vector
           step 2:
            find the distance between the old position and this intersection point
           step 3:
            determine which distance is hte shortest, the first collision happens on that side
           step 4:
            now we know where a collision occurs and on which side
           step 5:
            profit
            
            
            RIGHT AND LEFT ARE CURRENTLY BROKEN WHEN COMPARED WITH TOP AND BOTTOM
            
            '''
        
        self.colRecursionDepth +=1
        if(self.colRecursionDepth > 25):
            print('ERROR caught in collision detection. crashing prevented. velocity killed')
            self.npos = self.pos
            self.setPermanentPosition()
            self.vel = (0,0)
            return True
        
        
        currentPosition = self.npos
        oldPosition = self.pos
        
        #this is to take a limit
        adjustedVelocity = (self.vel[0] + 0.00001, self.vel[1] + 0.00001)
        
        colHappened = False
        
        self.badTiles = []
        
        for colidedTile in tiles:
            tilePosition = colidedTile.getRect()
            if(currentPosition.colliderect(tilePosition) and colidedTile.properties['solid']):
                
                self.badTiles.append(tilePosition)
                
                if(colidedTile.canCollisionOccur('bottom')):
                   bottomIntersectDistance = math.sqrt((((oldPosition.bottom - tilePosition.top)*self.vel[0])/adjustedVelocity[1])**2 + (tilePosition.top-oldPosition.bottom)**2)
                else:
                    bottomIntersectDistance = 10000
                
                if(colidedTile.canCollisionOccur('top')):
                    topIntersectDistance = math.sqrt((((oldPosition.top - tilePosition.bottom)*self.vel[0])/adjustedVelocity[1])**2 + (tilePosition.bottom-oldPosition.top)**2)
                else:
                    topIntersectDistance = 10000
                
                if(colidedTile.canCollisionOccur('right')):
                    rightIntersectDistance = math.sqrt((oldPosition.right - tilePosition.left)**2 + ((((oldPosition.right - tilePosition.left)*self.vel[1])/(adjustedVelocity[0])))**2)
                else:
                    rightIntersectDistance = 10000
                    
                if(colidedTile.canCollisionOccur('left')):
                    leftIntersectDistance = math.sqrt((oldPosition.left - tilePosition.right)**2 + ((((oldPosition.left - tilePosition.right)*self.vel[1])/(adjustedVelocity[0])))**2)
                else:
                    leftIntersectDistance = 10000
                
                #print('b', bottomIntersectDistance, 't', topIntersectDistance, 'l', leftIntersectDistance, 'r', rightIntersectDistance)
                
                correctDistance = min(bottomIntersectDistance, topIntersectDistance, leftIntersectDistance, rightIntersectDistance)
        
                if(correctDistance >= TILE_SIZE):
                    pass
                elif(correctDistance == bottomIntersectDistance and correctDistance < TILE_SIZE):
                    #print('collision bottom')
                    dY = abs(self.npos.bottom - self.pos.bottom)
                    badY = abs(tilePosition.top - self.npos.bottom)
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
                    self.fallingTime = 0
                    self.isJumping = False
                        
                elif(correctDistance == topIntersectDistance and correctDistance < TILE_SIZE):
                    #print('collision top')
                    dY = abs(self.npos.top - self.pos.top)
                    badY = abs(tilePosition.bottom - self.npos.top)
                    okY = abs(dY - badY)
                    self.npos = pygame.Rect(self.npos.left, self.pos.top-okY, self.width, self.height)
                    self.vel = (self.vel[0], 0)
                    self.jumpCounter = 0
                    self.jumpJuice = 0
                    colHappened = True
                    
                elif(correctDistance == leftIntersectDistance and correctDistance < TILE_SIZE):
                    #print('collision left')
                    dX = abs(self.npos.left - self.pos.left)
                    badX = abs(tilePosition.right - self.npos.left)
                    okX = abs(dX - badX)
                    self.npos = pygame.Rect(self.pos.left-okX, self.npos.top, self.width, self.height)
                    self.vel = (0, self.vel[1])
                        
                    colHappened = True
                    
                    
                elif(correctDistance == rightIntersectDistance and correctDistance < TILE_SIZE):
                    #print('collision right')
                    dX = abs(self.npos.right - self.pos.right)
                    badX = abs(tilePosition.left - self.npos.right)
                    okX = abs(dX - badX)
                    self.npos = pygame.Rect(self.pos.left+okX, self.npos.top, self.width, self.height)
                    self.vel = (0, self.vel[1])
                
                    colHappened = True
                
                
        if(colHappened):
            self.tileCollide(tiles)
        else:
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
                
    def kill(self):
        globe.State.addState('death-scene')
        globe.State.pauseGame()
        self.unRegister()
        globe.Hud.displayMenu(GameOverScreen())