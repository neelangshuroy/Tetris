import random
import copy

class gameObject:
    objectColour=None
    gridX,gridY=0,0
    allOrientations=None
    currShape=None
    orientationIndex=-1
    objectWidth=4
    objectHeight=4

    mapping = {
        0: 'square',
        1: 'rod',
        2: 'S shape',
        3: 'anti-S shape',
        4: 'T-shape'
    }

    def __init__(self,gamescreen):
        self.objectColour=random.choice(gamescreen.game.allcolours)

        myshape=random.randint(1,len(gamescreen.game.shapes)) - 1
        if myshape==gamescreen.prev_ind and gamescreen.prev_ind_count>1:
            tmp=[]
            for i in range(len(gamescreen.game.shapes)):
                if myshape==2:
                    if i!=2 and i!=3:
                        tmp.append(i)
                elif myshape==3:
                    if i!=2 and i!=3:
                        tmp.append(i)
                else:
                    tmp.append(i)
            myshape=random.choice(tmp)
        elif myshape==gamescreen.prev_ind:
            gamescreen.prev_ind_count += 1
        else:
            gamescreen.prev_ind = myshape
            gamescreen.prev_ind_count = 1
        
        self.allOrientations=[]
        for i in gamescreen.game.shapes[myshape]:
            self.allOrientations.append(copy.deepcopy(gamescreen.game.allshapes[i]))

        self.orientationIndex=random.randint(1,len(self.allOrientations)) - 1
        self.updateObjectWidth()
        self.updateObjectHeight()
        self.updateCurrShape()

        # i,j -> gridX is i, gridY is j
        self.gridX = -1
        self.gridY = gamescreen.colOffset + max(0, random.randint(1,gamescreen.noOfCols) - self.objectWidth)

    def getObjectWidth(self,i):
        maxwidth = -1
        for item in self.allOrientations[i]:
            maxwidth = max(maxwidth,1+item[1])
        return maxwidth
    def getObjectHeight(self,i):
        maxheight = -1
        for item in self.allOrientations[i]:
            maxheight = max(maxheight,1+item[0])
        return maxheight

    def updateObjectWidth(self):
        self.objectWidth = self.getObjectWidth(self.orientationIndex)
    def updateObjectHeight(self):
        self.objectHeight = self.getObjectHeight(self.orientationIndex)

    def updateCurrShape(self):
        self.currShape = self.allOrientations[self.orientationIndex]

    def rotateRight(self):
        self.orientationIndex = (1 + self.orientationIndex)%len(self.allOrientations)
        self.updateObjectWidth()
        self.updateObjectHeight()
        self.updateCurrShape()
    def rotateLeft(self):
        self.orientationIndex -= 1
        if self.orientationIndex < 0:
            self.orientationIndex = -1 + len(self.allOrientations)
        self.updateObjectWidth()
        self.updateObjectHeight()
        self.updateCurrShape()

    def rightRotatedObject(self):
        i=self.orientationIndex
        i=(i+1)%len(self.allOrientations)
        return [i,self.allOrientations[i]]
    def leftRotatedObject(self):
        i=self.orientationIndex
        if i==0: return [-1+len(self.allOrientations),self.allOrientations[-1]]
        return [i-1,self.allOrientations[i-1]]

    def moveLeft(self):
        self.gridY -= 1
    def moveRight(self):
        self.gridY += 1