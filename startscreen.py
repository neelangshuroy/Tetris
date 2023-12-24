'''
Made by NEELANGSHU ROY
Student of B.Tech in Computer Science and Engineering at NIT Allahabad
Batch of 2021-25
'''

import pygame as pg
from pygame.locals import *
import random
from clickable_buttons import *
from shape_for_bg import *
from gamesounds import *

class startScreen:
    squareSize=0
    posX,posY,counter=0,0,0
    noOfRows,noOfCols=22,29
    bgrid=[]
    gridoutline=(54,54,54)
    borderBuffer=4.35

    topmost,newtiles,upperlimit=0,0,0
    movingTiles,buffer,stillTiles=[],[],[]

    buttonbgcolour,buttontextcolour=(160,60,250),(110,250,200)
    buttonHoverBorderColour,buttonClickbgColour=(240,250,50),(120,25,190)

    newgamebuttonPos,instructionsPos,exitbuttonPos=[360,250],[360,350],[360,450]
    allbuttons=[]
    basicButtonStates=[0,0,0]
    inAMode=-1

    showInstructionPanel,showExitPanel=0,0
    exitPanelAction=0

    openingMusicDuration = 0

    def __init__(self,game):
        self.game=game
        for i in range(self.noOfRows):
            self.bgrid.append([0]*self.noOfCols)
        self.allbuttons.append(Button(self.newgamebuttonPos,'NEW GAME',self))
        self.allbuttons.append(Button(self.instructionsPos,'INSTRUCTIONS',self))
        self.allbuttons.append(Button(self.exitbuttonPos,'EXIT',self))

        if game.playOpeningMusicOnce:
            game.playOpeningMusicOnce = 0
            self.openingMusicDuration = int(1+game.fps*opening_music.get_length())
            self.nowStartFading = 10 * game.fps
            self.fade_step = opening_music.get_volume()/self.nowStartFading
            opening_music.play()

    def setUpExitPanel(self):
        self.exitPanel_x,self.exitPanel_y=30,550
        self.exitPanelWidth,self.exitPanelHeight=955,110

        self.bgcolour,self.textcolour=(160,60,250),(110,250,200)
        self.borderRadius=15
        self.exitPanelResponseDelay=3
        self.yes_IsClicked=0
        self.yes_WasClicked=0
        self.no_IsClicked=0
        self.no_WasClicked=0
        self.exitTextSize=0
        self.exitOptionTextSize=30
        self.exitOptionTextSize_hovered=40
        self.exitOptionColour = (255,235,0)
        self.exitOptionHovered = (255,215,0)
        self.exitOptionClicked = (255,190,0)

        yesX,yesY=70,575
        noX,noY=745,575
        yesWidth,yesHeight=200,60
        self.yesTextTuple = (yesX,yesY,yesWidth,yesHeight)
        self.noTextTuple = (noX,noY,yesWidth,yesHeight)
    
    def setUpInstructionPanel(self):
        self.InstructionPanel_1,self.instructionPanel_2=None,None
        self.instructionPanel1_x,self.instructionPanel1_y=30,80
        self.instructionPanel2_x,self.instructionPanel2_y=690,80
        self.instructionPanelWidth,self.instructionPanelHeight=300,600

        self.esckey=pg.image.load('Game Sprites/esc key.jpg').convert_alpha()
        self.esckey=pg.transform.scale(self.esckey,(64,64))

        self.upkey=pg.image.load('Game Sprites/up key.png').convert_alpha()
        self.upkey=pg.transform.scale(self.upkey,(64,64))

        self.downkey=pg.image.load('Game Sprites/down key.png').convert_alpha()
        self.downkey=pg.transform.scale(self.downkey,(64,64))

        self.leftkey=pg.image.load('Game Sprites/left key.png').convert_alpha()
        self.leftkey=pg.transform.scale(self.leftkey,(64,64))

        self.rightkey=pg.image.load('Game Sprites/right key.png').convert_alpha()
        self.rightkey=pg.transform.scale(self.rightkey,(64,64))

        self.w_key=pg.image.load('Game Sprites/w key.png').convert_alpha()
        self.w_key=pg.transform.scale(self.w_key,(64,64))
        
        self.a_key=pg.image.load('Game Sprites/a key.png').convert_alpha()
        self.a_key=pg.transform.scale(self.a_key,(64,64))

        self.s_key=pg.image.load('Game Sprites/s key.png').convert_alpha()
        self.s_key=pg.transform.scale(self.s_key,(64,64))

        self.d_key=pg.image.load('Game Sprites/d key.png').convert_alpha()
        self.d_key=pg.transform.scale(self.d_key,(64,64))

        self.bgcolour,self.textcolour=(160,60,250),(110,250,200)
        self.borderRadius=15

        self.a_text=pg.font.SysFont('kristenitc',24).render('block moves left',True,self.textcolour)
        self.d_text=pg.font.SysFont('kristenitc',24).render('block moves right',True,self.textcolour)
        self.s_text=pg.font.SysFont('kristenitc',22).render('block falls instantly',True,self.textcolour)

        self.left_text=pg.font.SysFont('kristenitc',21).render('block rotates left',True,self.textcolour)
        self.right_text=pg.font.SysFont('kristenitc',21).render('block rotates right',True,self.textcolour)
        self.esc_text=pg.font.SysFont('kristenitc',21).render('Pause/Resume',True,self.textcolour)

    def beyondRoundBorder(self,i,j,x,y):
        return i<=x<=(i+self.borderBuffer) and j<=y<=(j+self.borderBuffer)
    def insideRectangle(self,i,j,width,height,x,y):
        return i<=x<=(i+width) and j<=y<=(j+height)
    def getAllRoundedCorners(self,i,j,width,height):
        return [[i,j],[i+width-self.borderBuffer,j],[i,j+height-self.borderBuffer],[i+width-self.borderBuffer,j+height-self.borderBuffer]]
    def insideButton(self,button,x,y):
        if not self.insideRectangle(button[0],button[1],Button.width,Button.height,x,y):
            return False
        getAll4 = self.getAllRoundedCorners(button[0],button[1],Button.width,Button.height)
        for item in getAll4:
            if self.beyondRoundBorder(*item,x,y):
                return False
        return True

    def insideNewGameButton(self,x,y):
        return self.insideButton(self.newgamebuttonPos,x,y)
    def insideInstructionsButton(self,x,y):
        return self.insideButton(self.instructionsPos,x,y)
    def insideExitButton(self,x,y):
        return self.insideButton(self.exitbuttonPos,x,y)
    
    def insideAnyButton(self,x,y):
        return self.insideNewGameButton(x,y) or self.insideInstructionsButton(x,y) or self.insideExitButton(x,y)
    
    def showAllButtons(self,states):
        for i in range(len(states)):
            self.displayButton(self.allbuttons[i],states[i])

    def displayButton(self,button,state):
        button.show(self.game,state)

    def allButtonsDisplay(self):
        if self.game.processResult==1:
            self.game.processResult=0
            if self.insideNewGameButton(self.game.events[0],self.game.events[1]):
                self.inAMode=0
            elif self.insideInstructionsButton(self.game.events[0],self.game.events[1]):
                self.inAMode=1
                self.setUpInstructionPanel()
            elif self.insideExitButton(self.game.events[0],self.game.events[1]):
                self.inAMode=2
                self.setUpExitPanel()
        if self.game.inProcess==0 and not self.insideAnyButton(self.game.events[0],self.game.events[1]):
            self.basicButtonStates=[0,0,0]
            if self.game.events[-1][0]:
                fullcheck=1
                if self.inAMode==1:
                    panel1_all4=self.getAllRoundedCorners(self.instructionPanel1_x,self.instructionPanel1_y,self.instructionPanelWidth,self.instructionPanelHeight)
                    ins1_bordercheck=0 # by default within border
                    for item in panel1_all4:
                        if self.beyondRoundBorder(*item,self.game.events[0],self.game.events[1]):
                            ins1_bordercheck=1 # 1 means beyond border
                            break
                    
                    tmp1=[self.instructionPanel1_x,self.instructionPanel1_y,self.instructionPanelWidth,self.instructionPanelHeight,self.game.events[0],self.game.events[1]]
                    if self.insideRectangle(*tmp1) and not ins1_bordercheck:
                        fullcheck=0

                    panel2_all4=self.getAllRoundedCorners(self.instructionPanel2_x,self.instructionPanel2_y,self.instructionPanelWidth,self.instructionPanelHeight)
                    ins2_bordercheck=0
                    for item in panel2_all4:
                        if self.beyondRoundBorder(*item,self.game.events[0],self.game.events[1]):
                            ins2_bordercheck=1
                            break
                    
                    tmp2=[self.instructionPanel2_x,self.instructionPanel2_y,self.instructionPanelWidth,self.instructionPanelHeight,self.game.events[0],self.game.events[1]]
                    if self.insideRectangle(*tmp2) and not ins2_bordercheck:
                        fullcheck=0
                elif self.inAMode==2:
                    panel_all4=self.getAllRoundedCorners(self.exitPanel_x,self.exitPanel_y,self.exitPanelWidth,self.exitPanelHeight)
                    bordercheck=0
                    for item in panel_all4:
                        if self.beyondRoundBorder(*item,self.game.events[0],self.game.events[1]):
                            bordercheck=1
                            break
                    
                    tmp=[self.exitPanel_x,self.exitPanel_y,self.exitPanelWidth,self.exitPanelHeight,self.game.events[0],self.game.events[1]]
                    if self.insideRectangle(*tmp) and not bordercheck:
                        fullcheck=0
                if fullcheck:   
                    self.inAMode=-1
            
            if self.inAMode>-1:
                self.basicButtonStates[self.inAMode]=2
        elif self.game.inProcess==0:
            if self.insideNewGameButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[1,0,0]
            elif self.insideInstructionsButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[0,1,0]
            elif self.insideExitButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[0,0,1]

            if self.inAMode>-1:
                self.basicButtonStates[self.inAMode]=2
        elif self.game.responseDelay>0: # 0.1 sec response delay
            if self.insideNewGameButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[2,0,0]
            elif self.insideInstructionsButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[0,2,0]
            elif self.insideExitButton(self.game.events[0],self.game.events[1]):
                self.basicButtonStates=[0,0,2]

        self.showAllButtons(self.basicButtonStates)

    def exitPanelDisplay(self):
        self.exitPanel=pg.draw.rect(self.game.screen,self.bgcolour,[self.exitPanel_x,self.exitPanel_y,self.exitPanelWidth,self.exitPanelHeight],border_radius=self.borderRadius)
        
        self.exit_text=pg.font.SysFont('kristenitc',int(self.exitTextSize)).render('ARE YOU SURE ?',True,self.textcolour)
        
        textX=30 + 955/2 - self.exit_text.get_width()/2
        textY=550 + 110/2 - self.exit_text.get_height()/2
        self.game.screen.blit(self.exit_text,(textX,textY))

        self.exitTextSize += 2.8
        self.exitTextSize = min(self.exitTextSize,40)

        if self.exitTextSize==40:
            yesTuple=[]
            for item in self.yesTextTuple:
                yesTuple.append(item)
            yesTuple.append(self.game.events[0])
            yesTuple.append(self.game.events[1])
            yesBorder=[yesTuple[0],yesTuple[1],yesTuple[-2],yesTuple[-1]]
            yesAll4=self.getAllRoundedCorners(*yesBorder)
            yesbordercheck=0
            for item in yesAll4:
                if self.beyondRoundBorder(*item,yesBorder[-2],yesBorder[-1]):
                    yesbordercheck=1
                    break

            if self.game.events[-1][0] and self.insideRectangle(*yesTuple) and not yesbordercheck and self.yes_IsClicked==0 and self.yes_WasClicked==0:
                self.yes_IsClicked=1
                buttonclick.play()
            if not self.game.events[-1][0] and self.yes_IsClicked==1:
                self.yes_IsClicked=0
                self.yes_WasClicked=1
            
            if not self.insideRectangle(*yesTuple) or yesbordercheck:
                pg.draw.rect(self.game.screen,self.exitOptionColour,self.yesTextTuple,border_radius=self.borderRadius)
                yestext=pg.font.SysFont('kristenitc',self.exitOptionTextSize).render('YES',True,(0,0,0))
            elif self.yes_IsClicked==0 and self.yes_WasClicked==0:
                pg.draw.rect(self.game.screen,self.exitOptionHovered,self.yesTextTuple,border_radius=self.borderRadius)
                yestext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('YES',True,(0,0,0))
            elif self.yes_IsClicked==1 or self.exitPanelResponseDelay>0:
                if self.yes_IsClicked==0:
                    self.exitPanelResponseDelay-=1
                pg.draw.rect(self.game.screen,self.exitOptionClicked,self.yesTextTuple,border_radius=self.borderRadius)
                yestext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('YES',True,(0,0,0))
            else:
                self.yes_WasClicked=0
                self.exitPanelResponseDelay=3
                pg.draw.rect(self.game.screen,self.exitOptionHovered,self.yesTextTuple,border_radius=self.borderRadius)
                yestext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('YES',True,(0,0,0))
                return -1

            noTuple=[]
            for item in self.noTextTuple:
                noTuple.append(item)
            noTuple.append(self.game.events[0])
            noTuple.append(self.game.events[1])
            noBorder=[noTuple[0],noTuple[1],noTuple[-2],noTuple[-1]]
            noAll4=self.getAllRoundedCorners(*noBorder)
            nobordercheck=0
            for item in noAll4:
                if self.beyondRoundBorder(*item,noBorder[-2],noBorder[-1]):
                    nobordercheck=1
                    break

            if self.game.events[-1][0] and self.insideRectangle(*noTuple) and not nobordercheck and self.no_IsClicked==0 and self.no_WasClicked==0:
                self.no_IsClicked=1
                buttonclick.play()
            if not self.game.events[-1][0] and self.no_IsClicked==1:
                self.no_IsClicked=0
                self.no_WasClicked=1
            
            if not self.insideRectangle(*noTuple) or nobordercheck:
                pg.draw.rect(self.game.screen,self.exitOptionColour,self.noTextTuple,border_radius=self.borderRadius)
                notext=pg.font.SysFont('kristenitc',self.exitOptionTextSize).render('NO',True,(0,0,0))
            elif self.no_IsClicked==0 and self.no_WasClicked==0:
                pg.draw.rect(self.game.screen,self.exitOptionHovered,self.noTextTuple,border_radius=self.borderRadius)
                notext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('NO',True,(0,0,0))
            elif self.no_IsClicked==1 or self.exitPanelResponseDelay>0:
                if not self.no_IsClicked:
                    self.exitPanelResponseDelay-=1
                pg.draw.rect(self.game.screen,self.exitOptionClicked,self.noTextTuple,border_radius=self.borderRadius)
                notext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('NO',True,(0,0,0))
            else:
                self.no_WasClicked=0
                self.exitPanelResponseDelay=3
                pg.draw.rect(self.game.screen,self.exitOptionHovered,self.noTextTuple,border_radius=self.borderRadius)
                notext=pg.font.SysFont('kristenitc',self.exitOptionTextSize_hovered,pg.font.Font.bold).render('NO',True,(0,0,0))
                return 1

            yesTextX = self.yesTextTuple[0] + self.yesTextTuple[2]/2 - yestext.get_width()/2
            yesTextY = self.yesTextTuple[1] + self.yesTextTuple[3]/2 - yestext.get_height()/2
            noTextX =self.noTextTuple[0] + self.noTextTuple[2]/2 - notext.get_width()/2
            noTextY = self.noTextTuple[1] + self.noTextTuple[3]/2 - notext.get_height()/2

            yestextpos = (yesTextX,yesTextY)
            notextpos = (noTextX,noTextY)

            self.game.screen.blit(yestext,yestextpos)
            self.game.screen.blit(notext,notextpos)
        
        return 0

    def instructionsDisplay(self):
        instructionPanel1_tuple=(self.instructionPanel1_x,self.instructionPanel1_y,self.instructionPanelWidth,self.instructionPanelHeight)
        self.InstructionPanel_1 = pg.draw.rect(self.game.screen,self.bgcolour,instructionPanel1_tuple,border_radius=self.borderRadius)
        instructionPanel2_tuple=(self.instructionPanel2_x,self.instructionPanel2_y,self.instructionPanelWidth,self.instructionPanelHeight)
        self.instructionPanel_2 = pg.draw.rect(self.game.screen,self.bgcolour,instructionPanel2_tuple,border_radius=self.borderRadius)

        self.game.screen.blit(self.w_key,(148,100))
        self.game.screen.blit(self.a_key, (69,179))
        self.game.screen.blit(self.s_key,(148,179))
        self.game.screen.blit(self.d_key,(227,179))

        self.game.screen.blit(self.a_key, (49,45 + 279))
        self.game.screen.blit(self.d_key, (49,45 + 368 + 15))
        self.game.screen.blit(self.s_key, (49,45 + 457 + 30))

        self.game.screen.blit(self.upkey,(148 + 660,100))
        self.game.screen.blit(self.leftkey, (69 + 660,179))
        self.game.screen.blit(self.downkey,(148 + 660,179))
        self.game.screen.blit(self.rightkey,(227 + 660,179))

        self.game.screen.blit(self.leftkey, (49 + 660,45 + 279))
        self.game.screen.blit(self.rightkey, (49 + 660,45 + 368 + 15))
        self.game.screen.blit(self.esckey, (49 + 660,45 + 457 + 30))

        self.game.screen.blit(self.a_text,(49 + 64 + 6,279 + 55))
        self.game.screen.blit(self.d_text,(49 + 64 + 6,279 + 55 + 64 + 40))
        self.game.screen.blit(self.s_text,(49 + 64 + 6,279 + 55 + 3 + 2*(64 + 40)))
        self.game.screen.blit(self.left_text,(660 + 49 + 64 + 6,279 + 55 + 4))
        self.game.screen.blit(self.right_text,(660 + 49 + 64 + 6,279 + 55 + 8 + 64 + 40))
        self.game.screen.blit(self.esc_text,(660 + 49 + 64 + 6,279 + 55 + 12 + 2*(64 + 40)))

    def signatureDisplay(self):
        fontSize=80
        fontStyle='segoeuisemibold'
        words=(
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('T',True,self.game.red),
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('E',True,self.game.orange),
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('T',True,self.game.yellow),
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('R',True,self.game.green),
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('I',True,self.game.cyan),
        pg.font.SysFont(fontStyle,fontSize,pg.font.Font.bold).render('S',True,self.game.rose)
        )

        posX,posY,incr=345,35,10
        add=0
        for item in words:
            self.game.screen.blit(item,(posX+add,posY))
            add += incr + item.get_width()

        myName=pg.font.SysFont('mingliuextb',fontSize-10,pg.font.Font.bold).render('by Neelangshu Roy',True,(255,255,255))
        self.game.screen.blit(myName,(215,145))
        pass
    
    def run(self):
        # 1 means start game, -1 means exit, 0 means no action
        self.upperlimit=2
        self.squareSize=self.game.squareSize
        self.counter+=1

        self.openingMusicDuration=max(0,self.openingMusicDuration-1)
        if self.openingMusicDuration>0 and self.openingMusicDuration<=self.nowStartFading:
            opening_music.set_volume(max(0,opening_music.get_volume()-self.fade_step))

        self.background()
        self.signatureDisplay()
        self.allButtonsDisplay()

        # self.exitPanelDisplay(game)
        if self.inAMode==0:
            if self.openingMusicDuration>0:
                self.openingMusicDuration = 0
                opening_music.stop()
            return 1 # start the game
        if self.inAMode==1:
            self.instructionsDisplay()
        if self.inAMode==2:
            self.exitPanelAction=self.exitPanelDisplay()
        
        if self.exitPanelAction!=0:
            if self.exitPanelAction>0:
                self.inAMode=-1
                self.exitPanelAction=0
            else:
                if self.openingMusicDuration>0:
                    self.openingMusicDuration = 0
                    opening_music.stop()
                return -1
        
        return 0
    
    def indicesToCoordinates(self,i,j):
        # in left,top format
        return [self.posX+self.squareSize*j,self.posY+self.squareSize*i]
    
    def isValidIndices(self,i,j):
        return i>=0 and i<self.noOfRows and j>=0 and j<self.noOfCols and self.bgrid[i][j]==0
    
    def background(self):
        self.game.screen.fill(self.game.bgcolours)
        for i in range(self.noOfRows):
            for j in range(self.noOfCols):
                coordinates=self.indicesToCoordinates(i,j)
                pg.draw.rect(self.game.screen,self.gridoutline,[coordinates[0],coordinates[1],self.squareSize,self.squareSize],1)
        
        if len(self.movingTiles)==0 and self.topmost==0:
            self.newtiles=random.randint(1,4)
            prev=0
            rem=self.noOfCols%self.newtiles
            q=int(self.noOfCols/self.newtiles)
            for i in range(self.newtiles):
                interval=q
                if rem>0:interval+=1
                rem-=1
                randind=random.randint(prev,prev+interval-4)
                prev+=interval

                newshape=Shape([0,randind],random.choice(self.game.allshapes),random.choice(self.game.allcolours))
                newshape.setGrid(self)
                self.movingTiles.append(newshape)
        
        if self.counter==(self.game.fps//2):
            self.counter=0
            for item in self.movingTiles:
                item.unsetGrid(self)
                cangodown=1
                for i in item.squaresCoordinates:
                    if not self.isValidIndices(item.shapeCoordinates[0]+1+i[0],item.shapeCoordinates[1]+i[1]):
                        if item.shapeCoordinates[0]<=self.upperlimit:
                            self.topmost=1
                        cangodown=0
                        break
                if cangodown==0:
                    item.setGrid(self)
                    self.buffer.append(item)
                else:
                    item.shapeCoordinates[0]+=1
                    item.setGrid(self)

            for i in self.buffer:
                self.movingTiles.remove(i)
                self.stillTiles.append(i)
            
            self.buffer.clear()

        [item.display(self) for item in self.movingTiles]
        [item.display(self) for item in self.stillTiles]
