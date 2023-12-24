import pygame as pg
from pygame.locals import *
from blocks_in_game import *
from gameoverpanel import *
from pausepanel import *

class GameScreen:
    level=0
    squareSize=35
    gridoutline=(54,54,54)
    gameboxX, gameboxY = -35, 0

    noOfRows,noOfCols,colOffset = 22,13,9
    prev_ind,prev_ind_count = -1,0
    playerScore,scoreDelay = -1,-1

    leftArrowX, leftArrowY = 280 - 45, 70 - 66 + 41.5
    rightArrowX, rightArrowY = 700 + 33, 70 - 64 + 41.5
    gridDangerLevel = 2
    dangerLineThickness = 5
    dangerlineStartX,dangerlineStartY = 280,70
    dangerlineEndX,dangerlineEndY = 700 + 35,70
    leftArrowShift, rightArrowShift = 0,0
    leftmostShift = 15
    arrowShiftIncr = 0
    lineThicknessCorrection = -dangerLineThickness/3

    canSendObject = -1
    incomingObject = None
    objectMoveDelay = -1
    delayTimer = -1
    unitOfTime = -1

    fullRows = []
    bfouter,bfinner = -1,-1
    bgMusicTimer = 0

    gameOverPause = 0

    pausePanel = None
    blockHitsGround = 0
    # bf - black flash, outer = no. of flashes
    # inner = duration between each flash

    '''
    1.5 min, 3 min, 4.5 min, 6 min, 7 min, 7.5 mins
    90, 180, 270, 360, 420, 450
    increase block fall speed at each threshold

    4.5 min, 7 min, 8 min
    270, 420, 480
    increase difficulty at each threshold
    '''

    def __init__(self,game):
        self.level = 1
        self.blockHitsGround = 1
        self.gameOver = 0
        self.gameOverPause = 2*game.fps
        self.isPaused = 0
        self.playerScore = 0
        self.scoreDelay = game.fps
        self.game_over_panel = None
        self.playGameOverSound = 1

        self.bfouter = 19
        self.bfinner = game.fps // 15
        self.pushDelay = game.fps // 3
        
        self.delayTimer = game.fps // 2
        self.canSendObject = 1
        self.objectMoveDelay = self.delayTimer
        self.game=game
        self.initializeGrid()
        self.levelThresholds()
        self.setUpDangerSigns()
        self.setUpTextAndNumbers()

        self.pausePanel = pausePanel()

    def setUpTextAndNumbers(self):
        self.score_text=pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('Score:',True,(255,255,255))
        self.scoreTextPos=(10,712)
        self.digit_mapping={
            0: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('0',True,(255,255,255)),
            1: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('1',True,(255,255,255)),
            2: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('2',True,(255,255,255)),
            3: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('3',True,(255,255,255)),
            4: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('4',True,(255,255,255)),
            5: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('5',True,(255,255,255)),
            6: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('6',True,(255,255,255)),
            7: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('7',True,(255,255,255)),
            8: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('8',True,(255,255,255)),
            9: pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('9',True,(255,255,255)),
        }
        self.digitPosX, self.digitSpace, self.digitPosY = 165, 25, 714
    
    def levelThresholds(self):
        self.blockSpeeds = [90, 180, 270, 360, 420, 450]
        self.dangerLineLevels = [270, 420, 480]
        self.blockSpeedsIndex,self.dangerLineLevelsIndex=-1,-1
    
    def moveBlockLeft(self):
        if self.checkValidPosition(self.incomingObject.gridX,self.incomingObject.gridY-1,self.incomingObject.orientationIndex,self.incomingObject.currShape):
            self.incomingObject.moveLeft()
    def moveBlockRight(self):
        if self.checkValidPosition(self.incomingObject.gridX,self.incomingObject.gridY+1,self.incomingObject.orientationIndex,self.incomingObject.currShape):
            self.incomingObject.moveRight()

    def increaseBlockFallSpeed(self):
        self.delayTimer -= 2

    def checkValidPosition(self,i,j,index,shape):
        if i<0: return True
        if j<self.colOffset: return False
        i_val,j_val=i+self.incomingObject.getObjectHeight(index),j-self.colOffset+self.incomingObject.getObjectWidth(index)
        if i_val>self.noOfRows or j_val>self.noOfCols:
            return False
        checktrue=True
        for item in shape:
            if self.objectGrid[i+item[0]][j+item[1]-self.colOffset]!=None:
                checktrue=False
                break
        return checktrue

    def blockFalls(self):
        i=self.incomingObject.gridX
        while self.checkValidPosition(i+1,self.incomingObject.gridY,self.incomingObject.orientationIndex,self.incomingObject.currShape):
            i+=1
        self.playerScore += int(((i-self.incomingObject.gridX)*self.delayTimer)/self.game.fps)
        self.incomingObject.gridX=i

    def correction(self):
        self.incomingObject.gridX=min(self.incomingObject.gridX,self.noOfRows-self.incomingObject.objectHeight)
        self.incomingObject.gridY=max(self.colOffset,self.incomingObject.gridY)
        self.incomingObject.gridY=min(self.incomingObject.gridY,self.colOffset+self.noOfCols-self.incomingObject.objectWidth)
    
    def indicesToCoordinates(self,i,j):
        # in left,top format
        return [self.gameboxX+self.squareSize*j,self.gameboxY+self.squareSize*i]
    
    def displayScore(self):
        self.game.screen.blit(self.score_text,self.scoreTextPos)

        num=self.playerScore
        numlis=[]
        if num==0:
            numlis=[0]
        else:
            while num>0:
                numlis.append(int(num%10))
                num//=10
        numlis.reverse()
        for i in range(len(numlis)):
            self.game.screen.blit(self.digit_mapping[numlis[i]],(self.digitPosX+i*self.digitSpace,self.digitPosY))
    
    def initializeGrid(self):
        self.objectGrid=[]
        self.rowcount=[]
        for i in range(self.noOfRows):
            self.rowcount.append(0)
            self.objectGrid.append(self.noOfCols*[None])

    def dangerLineCoordinates(self):
        return ((self.dangerlineStartX,self.dangerlineStartY+self.lineThicknessCorrection),(self.dangerlineEndX,self.dangerlineEndY+self.lineThicknessCorrection))
    
    def setUpDangerSigns(self):
        arrow=pg.image.load('Game Sprites/red arrow.png').convert_alpha()
        self.leftarrow=pg.transform.scale(arrow,(48,48))
        self.rightarrow=pg.transform.rotate(self.leftarrow,180)

        self.dangerFontSize = 50
        self.dangerWordposX, self.dangerWordposY = 799, 7

        self.dangerword = pg.font.SysFont('maturascriptcapitals',self.dangerFontSize).render('Danger!!',True,self.game.red)
        self.dangerInstructions = (
            pg.font.SysFont('hpsimplifiedbdit',24,pg.font.Font.bold).render('Height of the blocks\'',True,self.game.red),
            pg.font.SysFont('hpsimplifiedbdit',24,pg.font.Font.bold).render('stack MUST NOT',True,self.game.red),
            pg.font.SysFont('hpsimplifiedbdit',24,pg.font.Font.bold).render('cross the red line!',True,self.game.red)
        )

    def showDangerSigns(self):
        pg.draw.line(self.game.screen,self.game.red,*self.dangerLineCoordinates(),self.dangerLineThickness)
        self.game.screen.blit(self.leftarrow,(self.leftArrowX + self.leftArrowShift,self.leftArrowY+self.lineThicknessCorrection))
        self.game.screen.blit(self.rightarrow,(self.rightArrowX + self.rightArrowShift,self.rightArrowY+self.lineThicknessCorrection))

        self.shiftincr = (2*self.squareSize)/self.game.fps
        
        if self.leftArrowShift >= 0:
            self.arrowShiftIncr = -self.shiftincr
        elif self.leftArrowShift <= -self.leftmostShift:
            self.arrowShiftIncr = self.shiftincr

        self.leftArrowShift += self.arrowShiftIncr
        self.rightArrowShift -= self.arrowShiftIncr

        self.game.screen.blit(self.dangerword,(self.dangerWordposX,self.dangerWordposY))
        addY=0
        for item in self.dangerInstructions:
            self.game.screen.blit(item,(799,72+addY))
            addY+=32

    def increaseDifficulty(self):
        self.gridDangerLevel += 1
        self.leftArrowY += self.squareSize
        self.rightArrowY += self.squareSize
        self.dangerlineStartY += self.squareSize
        self.dangerlineEndY += self.squareSize
    
    def background(self):
        self.game.screen.fill((0,0,0))

        for i in range(self.noOfRows):
            for j in range(self.colOffset,self.colOffset+self.noOfCols):
                coordinates=self.indicesToCoordinates(i,j)
                pg.draw.rect(self.game.screen,self.game.bgcolours,[coordinates[0],coordinates[1],self.squareSize,self.squareSize])
                pg.draw.rect(self.game.screen,self.gridoutline,[coordinates[0],coordinates[1],self.squareSize,self.squareSize],1)

    def updateScore(self):
        if self.gameOver or self.isPaused:
            return
        if self.scoreDelay>0:
            self.scoreDelay -= 1
        else:
            self.scoreDelay = self.game.fps
            self.playerScore += 1

            if self.blockSpeedsIndex+1<len(self.blockSpeeds) and self.playerScore>=self.blockSpeeds[1+self.blockSpeedsIndex]:
                self.blockSpeedsIndex+=1
                self.increaseBlockFallSpeed()
            if self.dangerLineLevelsIndex+1<len(self.dangerLineLevels) and self.playerScore>=self.dangerLineLevels[1+self.dangerLineLevelsIndex]:
                self.dangerLineLevelsIndex+=1
                self.increaseDifficulty()

    def displayGameObject(self):
        for i in self.incomingObject.currShape:
            coordinates=self.indicesToCoordinates(self.incomingObject.gridX+i[0],self.incomingObject.gridY+i[1])
            pg.draw.rect(self.game.screen,self.incomingObject.objectColour,[coordinates[0],coordinates[1],self.squareSize,self.squareSize])
            pg.draw.rect(self.game.screen,'black',[coordinates[0],coordinates[1],self.squareSize,self.squareSize],2)

    def sendBlock(self):
        self.incomingObject = gameObject(self)
        self.objectMoveDelay = self.delayTimer
        self.canSendObject = 0

    def prepareBlackFlash(self):
        self.bfouter = 19
        self.bfinner = self.game.fps // 15

    def enableSendBlock(self):
        self.canSendObject = 1
        self.blockHitsGround = 1
    
    def engraveIntoGrid(self):
        if self.blockHitsGround:
            block_hit_ground.play()
            self.blockHitsGround = 0
        
        for i in self.incomingObject.currShape:
            self.rowcount[self.incomingObject.gridX+i[0]] += 1
            self.objectGrid[self.incomingObject.gridX+i[0]][-self.colOffset + self.incomingObject.gridY+i[1]]=self.incomingObject.objectColour

        self.fullRows=self.fullRowCount()
        if self.fullRows!=[]:
            self.canSendObject = -1
            self.prepareBlackFlash()
        else:
            for i in range(self.gridDangerLevel):
                if self.rowcount[i]>0:
                    self.gameIsOver()
                    return
            self.enableSendBlock()

    def gameIsOver(self):
        self.gameOver = 1
        self.callGameOver()
    
    def displayGrid(self):
        for i in range(self.noOfRows):
            skipthis=0
            if self.canSendObject==-1 and self.bfouter%2>0 and self.bfinner>0:
                skipthis=1

            if skipthis and self.canSendObject==-1 and i in self.fullRows:
                continue
            for j in range(self.noOfCols):
                if self.objectGrid[i][j]!=None:
                    coordinates=self.indicesToCoordinates(i,j+self.colOffset)
                    pg.draw.rect(self.game.screen,self.objectGrid[i][j],[coordinates[0],coordinates[1],self.squareSize,self.squareSize])
                    pg.draw.rect(self.game.screen,'black',[coordinates[0],coordinates[1],self.squareSize,self.squareSize],2)

        if self.canSendObject==-1:
            if self.bfouter==0:
                self.blackFlashDone()
            elif self.bfouter%2>0:
                if self.bfinner>0:
                    self.bfinner-=1
                else:
                    self.bfinner=self.game.fps // 15
                    self.bfouter-=1
            else:
                if self.bfinner>0:
                    self.bfinner-=1
                else:
                    self.bfinner=self.game.fps // 15
                    self.bfouter-=1
                    block_blink.play()

    def moveDownObject(self):
        if (self.incomingObject.gridX+self.incomingObject.objectHeight)==self.noOfRows:
            self.engraveIntoGrid()
        else:
            newX = 1 + self.incomingObject.gridX
            checktrue=1
            for item in self.incomingObject.currShape:
                if self.objectGrid[newX + item[0]][-self.colOffset + self.incomingObject.gridY + item[1]]!=None:
                    checktrue=0
                    break

            if not checktrue:
                self.engraveIntoGrid()
                return
            
            if self.objectMoveDelay>0:
                self.objectMoveDelay -= 1
            else:
                self.objectMoveDelay = self.delayTimer
                self.incomingObject.gridX += 1

    def pushDownRows(self):
        i=-1+self.noOfRows
        while i>=0 and self.rowcount[i]>0:
            i-=1
        while i>=0 and self.rowcount[i]==0:
            i-=1
        complete=0
        if i<0:
            complete=1

        if complete:
            self.fullRows=self.fullRowCount()
            if self.fullRows!=[]:
                self.prepareBlackFlash()
            else:
                for i in range(self.gridDangerLevel):
                    if self.rowcount[i]>0:
                        self.gameIsOver()
                        return
                block_hit_ground.play()
                self.enableSendBlock()
            return
        
        if self.pushDelay>0:
            self.pushDelay -= 1
        else:
            self.pushDelay = self.game.fps // 3
            
            # push down CAREFULLY !!
            for i in range(-1+self.noOfRows,0,-1):
                if self.rowcount[i]==0 and self.rowcount[i-1]>0:
                    self.objectGrid[i]=self.objectGrid[i-1]
                    self.rowcount[i]=self.rowcount[i-1]
                    
                    self.objectGrid[i-1]=self.noOfCols*[None]
                    self.rowcount[i-1]=0

    def displayIncomingObject(self):
        self.displayGameObject()
        if not self.gameOver and not self.isPaused:
            self.moveDownObject()
        
    def fullRowCount(self):
        tmp=[]
        for i in range(self.noOfRows):
            if self.rowcount[i]==self.noOfCols:
                tmp.append(i)
        return tmp
    
    def blackFlashDone(self):
        for i in self.fullRows:
            self.rowcount[i]=0
            self.objectGrid[i]=self.noOfCols*[None]

        self.fullRows=[]
        # push down rows
        self.pushDownRows()

    def callGameOver(self):
        self.game_over_panel = gameOverPanel(self.playerScore)
    
    def gameOverPanel(self):
        pg.draw.rect(self.game.screen,(160,60,250),[145,150,725,450],border_radius=15)
        self.game.screen.blit(self.gameover_text,(170,170))
        
    def run(self):
        self.background()
        self.displayScore()

        if self.bgMusicTimer==0 and not self.gameOver and not self.isPaused:
            self.bgMusicTimer = int(1+self.game.fps*ingame_bgmusic.get_length())
            ingame_bgmusic.play()
        else:
            self.bgMusicTimer=max(0,self.bgMusicTimer-1)
        
        if self.canSendObject==1:
            self.sendBlock()
            self.displayIncomingObject()
        elif self.canSendObject==0:
            self.displayIncomingObject()

        self.displayGrid()
        self.showDangerSigns()

        self.updateScore()

        if self.gameOver:
            if self.gameOverPause>0:
                self.gameOverPause-=1
                if self.playGameOverSound:
                    self.playGameOverSound = 0
                    if self.bgMusicTimer>0:
                        ingame_bgmusic.stop()
                    gameover_sound.play()
            else:
                retval = self.game_over_panel.start_display(self.game)
                if retval!=0:
                    return retval
            # 1 means retry, 2 means go back to main menu
        if self.isPaused:
            retval = self.pausePanel.display(self.game)
            if retval!=0:
                if self.bgMusicTimer>0:
                    ingame_bgmusic.stop()
                return retval
        return 0