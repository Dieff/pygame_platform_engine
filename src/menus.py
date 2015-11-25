from src.constants import *
from src.entity import *
from src.utilities import *
import src.globe as globe
import sys

'''
Types

plain text
sprite <sprite name>
line break ;
'''
class TextItem(Entity):
    def __init__(self, myText='', textSize=12, outlineColor=GREY, textColor=WHITE, font='arial', startPos=False):
        super().__init__()
        self.pos.width = 0
        self.pos.height = 0
        self.textSize = textSize
        self.outlineColor = outlineColor
        self.textColor = textColor
        self.font = font
        self.originalText = myText
        
        splitText = self.originalText.split('<')
        
        imagesProcessed = []
        
        for item in splitText:
            if(item.find('>') != -1):
               a = item.split('>')
               imagesProcessed.append((globe.Loader.getSprite('common',a[0]), 'image'))
               imagesProcessed.append((a[1], 'text'))
            else:
                imagesProcessed.append((item, 'text'))
                
        lineBreaksProcessed = []
        
        for snippet in imagesProcessed:
            if(snippet[1] == 'text' and snippet[0].find(';')!=-1):
                curString = ''
                for item in snippet[0]:
                    if(item == ';'):
                        if(len(curString) > 0):
                            lineBreaksProcessed.append((curString, 'text'))
                        lineBreaksProcessed.append((';', 'break'))
                        curString = ''
                    else:
                        curString = curString + item
                if(len(curString) > 0):
                    lineBreaksProcessed.append((curString, 'text'))
                        
            else:
                lineBreaksProcessed.append(snippet)
            
        self.text = lineBreaksProcessed
        self.spacedText = []
        
        self.curWidth = 0
        self.width = 0
        self.height = 0
        
        self.doSpacing()
        
        if(startPos!=False):
            self.pos=startPos
        
    def doSpacing(self):
        widthCounter = 0
        heightCounter = 0
        curHeight = 0
        for item in self.text:
            
            if(item[1] == 'text'):
                font = pygame.font.SysFont(self.font, self.textSize, False, True,)
                text = font.render(item[0], 1, self.textColor, self.outlineColor)
                self.spacedText.append((item[0],item[1],(widthCounter, heightCounter)))
                widthCounter += text.get_width()
                if(text.get_height() > curHeight):
                    curHeight = text.get_height()
                    
                    
            if(item[1] == 'image'):
                self.spacedText.append((item[0],item[1],(widthCounter,heightCounter)))
                widthCounter += item[0].getWidth()
                if(item[0].getHeight() > curHeight):
                    curHeight = item[0].getHeight()
                    
                    
            if(item[1] == 'break'):
                if(self.curWidth < widthCounter):
                    self.curWidth = widthCounter
                widthCounter = 0
                heightCounter += curHeight
                curHeight = 0
                
        if(self.curWidth < widthCounter):
            self.curWidth = widthCounter
        self.width = self.curWidth
        self.height = heightCounter + curHeight
          
    def update(self, elapsedTime):
        for item in self.spacedText:
            if(item[1]=='image'):
                item[0].update(elapsedTime)     
        
    def draw(self):
        for item in self.spacedText:
            if(item[1]=='text'):
                font = pygame.font.SysFont(self.font, self.textSize, False, True,)
                text = font.render(item[0], 1, self.textColor, self.outlineColor)
                text.set_colorkey(GREY)
                DISPLAYSURF.blit(text, self.pos.move(item[2]))
            elif(item[1]=='image'):
                item[0].draw((self.pos.x +item[2][0], self.pos.y+item[2][1]))


'''
A selectable text, changes look if selected
'''
class MenuItem(TextItem):
    def __init__(self, text, onClick=False, selectAction=False, textSize=30):
        super().__init__(text, textSize=textSize)
        self.isSelected = False
        self.unSelect()
        self.act = onClick
        self.imHighlightedNow = selectAction
        
    def getSelectedStatus(self):
        return self.isSelected
    
    def Select(self):
        self.isSelected = True
        self.textColor = WHITE
        if(self.imHighlightedNow):
            self.imHighlightedNow()
        
    def unSelect(self):
        self.isSelected = False
        self.textColor = LIGHT_GREY

    def action(self):
        if(self.act):
            self.act()

'''
A set of selecteable texts
'''
class MenuList:
    def __init__(self, itms, forwardKey, reverseKey, selectKey, startPosition=(0,0), scrollDirection='vertical', isInfinite=False, textSize=30, textUnselectedColor=LIGHT_GREY, textSelectedColor=WHITE):
        self.items = []
        for mItem in itms:
            mMm = MenuItem(mItem[0], mItem[1], mItem[2], )
            self.items.append(mMm)
        
        self.fKey = forwardKey
        self.rKey = reverseKey
        self.sKey = selectKey
        self.inF = isInfinite
        self.direction = scrollDirection
        self.selectedIndex = 0
        self.previouslySelected = self.selectedIndex
        self.updateSelect()
        
        self.pos = pygame.Rect(startPosition,(0,0))
        
        self.fup = False
        self.fown = False
        self.fect = False
        
        self.ySpacing = 0
        self.xSpacing = 15
        
    def register(self):
        globe.Updater.registerUpdatee(self.update, ['nominal'])
        globe.Updater.registerDrawee(self.draw, ['nominal'])
    
    def getSelected(self):
        return self.items[self.selectedIndex]
    
    def updateSelect(self):
        self.items[self.previouslySelected].unSelect()
        self.items[self.selectedIndex].Select()
        self.previouslySelected = self.selectedIndex
    
    def update(self, elapsed):
        key_states = pygame.key.get_pressed()
        
        if(key_states[self.fKey]):
            if(self.fup == False):
                if(self.selectedIndex < len(self.items)-1):
                    self.selectedIndex+=1
                    self.updateSelect()
                elif(self.selectedIndex == len(self.items)-1 and self.inF == True):
                    self.selectedIndex = 0
                    self.updateSelect()
            self.fup = True 
        else:
            self.fup = False
        
        if(key_states[self.rKey]):
            if(self.fown == False):
                if(self.selectedIndex > 0):
                    self.selectedIndex-=1
                    self.updateSelect()
                elif(self.selectedIndex == 0 and self.inF == True):
                    self.selectedIndex = len(self.items)-1
                    self.updateSelect()
            self.fown = True
        else:
            self.fown = False
            
        if(key_states[self.sKey]):
            if(self.fect == False):
                self.items[self.selectedIndex].action()
            self.fect = True
        else:
            self.fect = False
    
        for item in self.items:
            item.update(elapsed)
    
    def draw(self):
        if(self.direction == 'vertical' or self.direction == 'Vertical'):
            yCounter = 0
            for item in self.items:
                item.pos.y = self.pos.y + yCounter
                item.draw()
                yCounter += item.height + self.ySpacing
        elif(self.direction == 'horizontal' or self.direction == 'Horizontal'):
            xCounter = 0
            for item in self.items:
                item.pos.x = self.pos.x + xCounter
                item.draw()
                xCounter += item.width + self.xSpacing


class TitleScreen:
    def __init__(self):
        self.topList = MenuList([('Play', False, self.buildPlay),('Options', False, self.buildOptions),('Credits', False, self.buildCredits),('Exit', False, self.buildExit)], pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RETURN, (100,50), isInfinite=True, scrollDirection='horizontal')
        self.buildPlay()

    def register(self):
        globe.Updater.registerUpdatee(self.update, ['started'])
        globe.Updater.registerDrawee(self.draw, ['started'])
        
    def update(self, el):
        self.topList.update(el)
        self.additionalList.update(el)
        
    def draw(self):
        self.topList.draw()
        self.additionalList.draw()
        
    def startGame(self):
        globe.State.addState('nominal')
        globe.Camera.start(globe.Updater.Player)
        globe.Area.initialCinematicLoad('starting-point', (32,356))
        globe.Updater.removeUpdatee(self.update)
        globe.Updater.removeDrawee(self.draw)
        
    def buildPlay(self):
        self.additionalList = MenuList([('Load Game', False, False),('New Game',self.startGame,False)], pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN, (50,50))
        
    def buildOptions(self):
        self.additionalList = MenuList([('Do Shit', False, False),('Do More Shit',False,False),('Shitt!!!!',False,False)], pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN, (50,50))
        
    def buildCredits(self):
        self.additionalList = TextItem('Look at these sprites and shit ; <kawaii-slime> ; <protag2-running-right>', startPos=pygame.Rect((50,50),(0,0)))
        #self.additionalList.pos = pygame.Rect((50,50),(0,0))
        
    def buildExit(self):
        self.additionalList = MenuList([('Really, Quit?', self.quit, False)], pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN, (50,50))
        
    def quit(self):
        pygame.quit()
        sys.exit()

'''
creates organized MenuLists

class Menu:
    def __init__(self):
        print('menu created')'''