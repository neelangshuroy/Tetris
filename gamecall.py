import sys
import pygame as pg
from pygame.locals import *
from startscreen import *
from gamescreen import *

class Game:
    mode=-1
    events=None
    
    fps=0
    screen,fpsclock=None,None

    inProcess,processResult,responseDelay=0,0,3

    bgcolours=(29,25,30)
    squareSize=35
    # events=[0,0,[0,0,0]]
    
    red=(255,40,30)
    yellow=(235,245,30)
    orange=(255,100,55)
    blue=(30,125,180)
    cyan=(80,240,240)
    green=(70,245,55)
    rose=(240,80,245)

    allcolours=(red,yellow,orange,blue,cyan,green,rose)
    allshapes=(((0,0),(0,1),(1,0),(1,1)),#square
               ((0,0),(0,1),(0,2),(0,3)),((0,0),(1,0),(2,0),(3,0)),#rod
               ((0,0),(1,0),(1,1),(2,1)),((1,0),(1,1),(0,1),(0,2)),#S shape
               ((0,1),(1,0),(1,1),(2,0)),((0,0),(0,1),(1,1),(1,2)),#anti-S shape
               ((0,1),(1,0),(1,1),(1,2)),((0,0),(1,0),(1,1),(2,0)),((0,0),(0,1),(0,2),(1,1)),((0,1),(1,0),(1,1),(2,1))#T-shape
               )
    shapes={
        0 : [0],
        1 : [1,2],
        2 : [3,4],
        3 : [5,6],
        4 : [7,8,9,10]
    }

    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris Game by Neelangshu Roy')
        self.screen=pg.display.set_mode((1015,770))
        self.fps=30
        self.fpsclock=pg.time.Clock()

        self.mode=0
        self.playOpeningMusicOnce = 1

        self.run()

        pg.quit()
        sys.exit()

    def isStartScreen(self):
        return self.mode==0
    
    def isInGame(self):
        return self.mode==1
    
    def isPaused(self):
        return self.mode==2

    def switchToGameMode(self):
        self.mode=1

    def switchToPause(self):
        self.mode=2

    def switchToStartScreen(self):
        self.mode=0
    
    def eventdetector(self):
        quit=0
        for event in pg.event.get():
            if event.type==QUIT:
                quit=1
                break
            
            if self.isInGame() and self.gamescreen.canSendObject == 0:
                if event.type==KEYDOWN:
                    # print('some key pressed')
                    if event.key==K_a:
                        self.gamescreen.moveBlockLeft()
                    if event.key==K_d:
                        self.gamescreen.moveBlockRight()
                    if event.key==K_s:
                        self.gamescreen.blockFalls()
                    
                    if event.key==K_LEFT:
                        count=0
                        while count<4 and not self.gamescreen.checkValidPosition(self.gamescreen.incomingObject.gridX,self.gamescreen.incomingObject.gridY-count,*self.gamescreen.incomingObject.leftRotatedObject()):
                            count+=1
                        if count<4:
                            self.gamescreen.incomingObject.gridY-=count
                            self.gamescreen.incomingObject.rotateLeft()
                    if event.key==K_RIGHT:
                        count=0
                        while count<4 and not self.gamescreen.checkValidPosition(self.gamescreen.incomingObject.gridX,self.gamescreen.incomingObject.gridY-count,*self.gamescreen.incomingObject.rightRotatedObject()):
                            count+=1
                        if count<4:
                            self.gamescreen.incomingObject.gridY-=count
                            self.gamescreen.incomingObject.rotateRight()

                    self.gamescreen.correction()
            if self.isInGame() and not self.gamescreen.gameOver:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamescreen.isPaused = not self.gamescreen.isPaused        

        x,y=pg.mouse.get_pos()
        ans=[x,y,pg.mouse.get_pressed()]
        if quit: ans.append(-1)
        return ans
        # different type of event checker functions are
        # needed here, for every type of if statement
        # in run() function of class Game

    def showStartScreen(self):
        self.startscreen=startScreen(self)
        while True:
            self.events=self.eventdetector()
            if len(self.events)>3:
                return -1

            timeToChange=self.startscreen.run()
            if timeToChange!=0:
                pg.display.flip()
                self.fpsclock.tick(self.fps)
                return timeToChange
            elif self.events[-1][0] and self.startscreen.insideAnyButton(self.events[0],self.events[1]) and self.inProcess==0:
                self.inProcess=1
                buttonclick.play()
            elif not self.events[-1][0] and not self.startscreen.insideAnyButton(self.events[0],self.events[1]) and self.inProcess==1:
                self.inProcess=0
            elif not self.events[-1][0] and self.inProcess==1:
                if self.responseDelay>0:
                    self.responseDelay-=1
                else:
                    self.responseDelay=3
                    self.inProcess=0
                    self.processResult=1
            
            pg.display.flip()
            self.fpsclock.tick(self.fps)

    def startGame(self):
        self.gamescreen=GameScreen(self)
        while True:
            self.events=self.eventdetector()
            if len(self.events)>3:
                break

            # self.gamescreen.user_event()
            gameplay_retval = self.gamescreen.run()
            if gameplay_retval<0:
                break
            elif gameplay_retval==1:
                return 0
            elif gameplay_retval==2:
                return 1

            pg.display.flip()
            self.fpsclock.tick(self.fps)

        return -1 # quit by default
    
    def run(self):
        begin=self.showStartScreen()
        while begin>-1:
            self.switchToGameMode()
            begin=self.startGame()
            # -1 means quit from here
            # 0 means retry
            # 1 means back to main menu
            if begin>0:
                self.switchToStartScreen()
                begin=self.showStartScreen()
                # will be 1 or -1 obviously
        return