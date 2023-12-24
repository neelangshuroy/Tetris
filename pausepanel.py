'''
Made by NEELANGSHU ROY
Student of B.Tech in Computer Science and Engineering at NIT Allahabad
Batch of 2021-25
'''

import pygame as pg
from pygame.locals import *
from gamesounds import *
class pausePanel:
    def __init__(self):
        self.pausedText=pg.font.SysFont('mingliuextb',48,pg.font.Font.bold).render('Paused',True,(255,255,255))
        self.pausedTextPos = (10,10)

        self.borderBuffer = 4.35
        self.borderRadius = 15
        self.textColour = (110,250,200)
        self.buttonColour = (160,60,250)
        self.buttonHovered = (140,50,250)
        self.buttonClicked = (120,25,190)
        self.buttonWidth,self.buttonHeight = 200,50
        self.retryTextFontSize, self.gobackTextFontSize = 32, 20

        self.playRetrySound,self.playGoBackSound = 1,1

        self.retryText=pg.font.SysFont('kristenitc',self.retryTextFontSize).render('Restart',True,self.textColour)
        self.retryTextFocused=pg.font.SysFont('kristenitc',self.retryTextFontSize,pg.font.Font.bold).render('Restart',True,self.textColour)
        self.gobackText=pg.font.SysFont('kristenitc',self.gobackTextFontSize).render('Quit to Main Menu',True,self.textColour)
        self.gobackTextFocused=pg.font.SysFont('kristenitc',self.gobackTextFontSize,pg.font.Font.bold).render('Quit to Main Menu',True,self.textColour)

        self.retryPosX,self.retryPosY = 9,70

        self.retryTextPosX,self.retryTextPosY = self.retryPosX + self.buttonWidth/2 - self.retryText.get_width()/2,self.retryPosY + self.buttonHeight/2 - self.retryText.get_height()/2

        self.gobackPosX,self.gobackPosY = 9,130

        self.gobackTextPosX,self.gobackTextPosY = self.gobackPosX + self.buttonWidth/2 - self.gobackText.get_width()/2,self.gobackPosY + self.buttonHeight/2 - self.gobackText.get_height()/2

        self.retryClicked,self.gobackClicked = 0,0
        self.yesClicked,self.noClicked = 0,0

        self.yesnoColour = (255,235,0)
        self.yesnoHovered = (255,215,0)
        self.yesnoClicked = (255,190,0)

        self.yesnoTextPosX,self.yesnoTextPosY = 13,195

        self.yesOptionPosX,self.yesOptionPosY = 9,320
        self.noOptionPosX,self.noOptionPosY = 9,380
        
        self.areYouSure=(
            pg.font.SysFont('kristenitc',self.gobackTextFontSize,pg.font.Font.bold).render('Are you sure?',True,self.textColour),
            pg.font.SysFont('kristenitc',self.gobackTextFontSize,pg.font.Font.bold).render('Current progess',True,self.textColour),
            pg.font.SysFont('kristenitc',self.gobackTextFontSize,pg.font.Font.bold).render('will be lost.',True,self.textColour)
        )

        self.yesText=pg.font.SysFont('kristenitc',self.retryTextFontSize).render('Yes',True,(0,0,0))
        self.yesTextFocused=pg.font.SysFont('kristenitc',self.retryTextFontSize,pg.font.Font.bold).render('Yes',True,(0,0,0))
        self.noText=pg.font.SysFont('kristenitc',self.retryTextFontSize).render('No',True,(0,0,0))
        self.noTextFocused=pg.font.SysFont('kristenitc',self.retryTextFontSize,pg.font.Font.bold).render('No',True,(0,0,0))

        self.yesTextPosX,self.yesTextPosY = self.yesOptionPosX + self.buttonWidth/2 - self.yesText.get_width()/2,self.yesOptionPosY + self.buttonHeight/2 - self.yesText.get_height()/2
        self.noTextPosX,self.noTextPosY = self.noOptionPosX + self.buttonWidth/2 - self.noText.get_width()/2,self.noOptionPosY + self.buttonHeight/2 - self.noText.get_height()/2

        self.nowStart = 0

    def beyondRoundBorder(self,i,j,x,y):
        return i<=x<=(i+self.borderBuffer) and j<=y<=(j+self.borderBuffer)
    def insideRectangle(self,i,j,width,height,x,y):
        return i<=x<=(i+width) and j<=y<=(j+height)
    def getAllRoundedCorners(self,i,j,width,height):
        return [[i,j],[i+width-self.borderBuffer,j],[i,j+height-self.borderBuffer],[i+width-self.borderBuffer,j+height-self.borderBuffer]]
    
    def insideRetry(self,x,y):
        if not self.insideRectangle(self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight,x,y):
            return 0
        lis=self.getAllRoundedCorners(self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight)
        for item in lis:
            if self.beyondRoundBorder(*item,x,y):
                return 0
        return 1
    def insideGoBack(self,x,y):
        if not self.insideRectangle(self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight,x,y):
            return 0
        lis=self.getAllRoundedCorners(self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight)
        for item in lis:
            if self.beyondRoundBorder(*item,x,y):
                return 0
        return 1
    def insideYes(self,x,y):
        if not self.insideRectangle(self.yesOptionPosX,self.yesOptionPosY,self.buttonWidth,self.buttonHeight,x,y):
            return 0
        lis=self.getAllRoundedCorners(self.yesOptionPosX,self.yesOptionPosY,self.buttonWidth,self.buttonHeight)
        for item in lis:
            if self.beyondRoundBorder(*item,x,y):
                return 0
        return 1
    def insideNo(self,x,y):
        if not self.insideRectangle(self.noOptionPosX,self.noOptionPosY,self.buttonWidth,self.buttonHeight,x,y):
            return 0
        lis=self.getAllRoundedCorners(self.noOptionPosX,self.noOptionPosY,self.buttonWidth,self.buttonHeight)
        for item in lis:
            if self.beyondRoundBorder(*item,x,y):
                return 0
        return 1
    
    def displayRetry(self,game):
        if self.insideRetry(game.events[0],game.events[1]) and not self.retryClicked and not self.gobackClicked:
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.buttonClicked,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.buttonHovered,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.retryTextFocused,(self.retryTextPosX,self.retryTextPosY))
        elif self.retryClicked:
            pg.draw.rect(game.screen,self.buttonClicked,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.retryTextFocused,(self.retryTextPosX,self.retryTextPosY))
        else:
            pg.draw.rect(game.screen,self.buttonColour,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.retryText,(self.retryTextPosX,self.retryTextPosY))
    def displayGoBack(self,game):
        if self.insideGoBack(game.events[0],game.events[1]) and not self.retryClicked and not self.gobackClicked:
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.buttonClicked,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.buttonHovered,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gobackTextFocused,(self.gobackTextPosX,self.gobackTextPosY))
        elif self.gobackClicked:
            pg.draw.rect(game.screen,self.buttonClicked,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gobackTextFocused,(self.gobackTextPosX,self.gobackTextPosY))
        else:
            pg.draw.rect(game.screen,self.buttonColour,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gobackText,(self.gobackTextPosX,self.gobackTextPosY))
    
    def displayYes(self,game):
        if self.insideYes(game.events[0],game.events[1]):
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.yesnoClicked,[self.yesOptionPosX,self.yesOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.yesnoHovered,[self.yesOptionPosX,self.yesOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.yesTextFocused,(self.yesTextPosX,self.yesTextPosY))
        else:
            pg.draw.rect(game.screen,self.yesnoColour,[self.yesOptionPosX,self.yesOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.yesText,(self.yesTextPosX,self.yesTextPosY))
    def displayNo(self,game):
        if self.insideNo(game.events[0],game.events[1]):
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.yesnoClicked,[self.noOptionPosX,self.noOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.yesnoHovered,[self.noOptionPosX,self.noOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.noTextFocused,(self.noTextPosX,self.noTextPosY))
        else:
            pg.draw.rect(game.screen,self.yesnoColour,[self.noOptionPosX,self.noOptionPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.noText,(self.noTextPosX,self.noTextPosY))

    def displayOptions(self,game):
        self.displayRetry(game)
        self.displayGoBack(game)

    def display(self,game):
        game.screen.blit(self.pausedText,self.pausedTextPos)
        self.displayOptions(game)
        if self.retryClicked or self.gobackClicked:
            self.yesOrNo(game)
        return self.checkevents(game)
    
    def checkevents(self,game):
        if game.events[-1][0] and self.insideRetry(game.events[0],game.events[1]) and not self.gobackClicked:
            self.retryClicked = 1
            if self.playRetrySound:
                self.playRetrySound = 0
                buttonclick.play()
        if game.events[-1][0] and self.insideGoBack(game.events[0],game.events[1]) and not self.retryClicked:
            self.gobackClicked = 1
            if self.playGoBackSound:
                self.playGoBackSound = 0
                buttonclick.play()
        
        retval = 0
        if not game.events[-1][0] and (self.retryClicked or self.gobackClicked):
            self.nowStart = 1
        
        if self.nowStart:
            retval = self.yesOrNo_events(game)
        
        if retval==0:
            return 0
        elif retval==2:
            self.nowStart = 0
            self.retryClicked=0
            self.gobackClicked=0
            buttonclick.play()
            self.playRetrySound=1
            self.playGoBackSound=1
            return 0
        else:
            self.nowStart = 0
            self.gobackClicked=0
            buttonclick.play()
            self.playRetrySound=1
            self.playGoBackSound=1
            if self.retryClicked:
                self.retryClicked=0
                return 1
            else:
                return 2
    
    def yesOrNo(self,game):
        for i in range(len(self.areYouSure)):
            game.screen.blit(self.areYouSure[i],(self.yesnoTextPosX,self.yesnoTextPosY+i*40))
        self.displayYes(game)
        self.displayNo(game)

    def yesOrNo_events(self,game):

        if game.events[-1][0] and self.insideYes(game.events[0],game.events[1]):
            self.yesClicked = 1
        if game.events[-1][0] and self.insideNo(game.events[0],game.events[1]):
            self.noClicked = 1

        if not game.events[-1][0] and self.yesClicked:
            self.yesClicked=0
            self.noClicked=0
            return 1
        if not game.events[-1][0] and self.noClicked:
            self.yesClicked=0
            self.noClicked=0
            return 2
        return 0
