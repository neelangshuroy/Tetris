import pygame as pg
from pygame.locals import *
from gamesounds import *
class gameOverPanel:
    bgcolour=(160,60,250)
    borderRadius=15
    mainPanelposX,mainPanelposY = 145, 150
    mainPanelWidth,mainPanelHeight = 725, 450
    gameOverTextposX,gameOverTextposY = -1,-1
    gameOverTextFontSize = -1
    gameOverTextColour = (255,190,45)
    gameover_text = None
    playerScore = -1
    newHighScore = -1
    isANewHighScore = 0
    highScoreMusicDuration = 0
    
    def __init__(self,score):
        with open('highscore.txt') as f:
            num=int(f.read())
        if num<score:
            self.isANewHighScore = 1
            self.newHighScore = 1
            self.playerScore = score
            with open('highscore.txt','w') as f:
                f.write(str(score))
        else:
            self.newHighScore = 0
            self.playerScore = num
        self.digitmapping={
            0: '0',1: '1',2: '2',3: '3',4: '4',
            5: '5',6: '6',7: '7',8: '8',9: '9'
        }
        self.scorelis=[]
        if self.playerScore==0:
            self.scorelis=[0]
        else:
            while self.playerScore>0:
                self.scorelis.append(self.playerScore%10)
                self.playerScore //= 10
            self.scorelis.reverse()
        
        self.digposX,self.digposY = 667,392
        self.digposX -= (32*((-1+len(self.scorelis))//2) + 16*(1-len(self.scorelis)%2))
        self.highScoreTextposTuple = (552,322)

        self.newImage = None
        self.newImageSize = 76
        self.sizeToggle=0
        self.newImageFontHigh,self.newImageFontLow = 0,0

        self.gameOverTextDelay = 30
        self.gameOverTextposX, self.gameOverTextposY = 492, 220
        self.gameOverTextposXdelta, self.gameOverTextposYdelta = (492-180)/30,(220-170)/30
        self.gameOverTextFontSizeDelta = (76-4)/30
        self.gameOverTextFontSize = 4

        self.borderBuffer = 4.35
        self.buttonColour = (255,235,0)
        self.buttonHovered = (255,215,0)
        self.buttonClicked = (255,190,0)
        self.buttonWidth,self.buttonHeight = 290,65
        self.retryTextFontSize, self.gobackTextFontSize = 32, 20
        
        self.retryText=pg.font.SysFont('kristenitc',self.retryTextFontSize).render('Retry',True,(0,0,0))
        self.retryTextFocused=pg.font.SysFont('kristenitc',self.retryTextFontSize,pg.font.Font.bold).render('Retry',True,(0,0,0))
        self.gobackText=pg.font.SysFont('kristenitc',self.gobackTextFontSize).render('Go Back to Main Menu',True,(0,0,0))
        self.gobackTextFocused=pg.font.SysFont('kristenitc',self.gobackTextFontSize,pg.font.Font.bold).render('Go Back to Main Menu',True,(0,0,0))
        
        self.retryPosX,self.retryPosY = 210,330
        self.retryTextPosX,self.retryTextPosY = 210 + 290/2 - self.retryText.get_width()/2,330 + 65/2 - self.retryText.get_height()/2
        self.gobackPosX,self.gobackPosY = 210,430
        self.gobackTextPosX,self.gobackTextPosY = 210 + 290/2 - self.gobackText.get_width()/2,430 + 65/2 - self.gobackText.get_height()/2

        self.scoreTextColour = (240,255,235)
        self.scoreTextSize = 44
        self.highScoreText=pg.font.SysFont('arialblack',self.scoreTextSize).render('High Score',True,self.scoreTextColour)

        self.retryClicked,self.gobackClicked = 0,0

        if self.newHighScore:
            self.loadImageForNewHighScore()

    def loadImageForNewHighScore(self):
        self.newImage=pg.image.load('Game Sprites/new.png').convert_alpha()
        self.newImageFontHigh,self.newImageFontLow = 90,76

    def isNewHighScore(self,game):
        thisImage=pg.transform.scale(self.newImage,(self.newImageSize,self.newImageSize))
        game.screen.blit(thisImage,(720,445))
        if self.sizeToggle:
            self.newImageSize-=1
        else:
            self.newImageSize+=1

        if self.newImageSize==self.newImageFontHigh or self.newImageSize==self.newImageFontLow:
            self.sizeToggle = not self.sizeToggle
    
    def checkevents(self,game):
        if game.events[-1][0] and self.insideRetry(game.events[0],game.events[1]):
            if not self.retryClicked:
                buttonclick.play()
            self.retryClicked = 1
        if game.events[-1][0] and self.insideGoBack(game.events[0],game.events[1]):
            if not self.gobackClicked:
                buttonclick.play()
            self.gobackClicked = 1
        
        if not game.events[-1][0] and self.retryClicked:
            if self.highScoreMusicDuration>0:
                new_highscore.stop()
            return 1
        if not game.events[-1][0] and self.gobackClicked:
            if self.highScoreMusicDuration>0:
                new_highscore.stop()
            return 2
        
        self.highScoreMusicDuration = max(0,self.highScoreMusicDuration-1)
        return 0
    
    def display(self,game):
        pg.draw.rect(game.screen,self.bgcolour,[self.mainPanelposX,self.mainPanelposY,self.mainPanelWidth,self.mainPanelHeight],border_radius=self.borderRadius)
        game.screen.blit(self.gameover_text,(self.gameOverTextposX,self.gameOverTextposY))
        self.displayOptions(game)
        self.displayHighScore(game)
        return self.checkevents(game)
    
    def start_display(self,game):
        if self.gameOverTextDelay==0:
            if self.isANewHighScore==1:
                self.isANewHighScore = -1
                self.highScoreMusicDuration = int(1+game.fps*new_highscore.get_length())
                new_highscore.play()
            return self.display(game)
        else:
            if self.gameOverTextDelay==1:
                self.gameOverTextDelay=0
                self.gameOverTextposX, self.gameOverTextposY = 180, 170
                self.gameOverTextFontSize = 76
            else:
                self.gameOverTextDelay-=1
                self.gameOverTextposX -= self.gameOverTextposXdelta
                self.gameOverTextposY -= self.gameOverTextposYdelta
                self.gameOverTextFontSize += self.gameOverTextFontSizeDelta
            
            self.gameover_text=pg.font.SysFont('ravie',int(self.gameOverTextFontSize)).render('Game Over !!!',True,self.gameOverTextColour)
            
            pg.draw.rect(game.screen,self.bgcolour,[self.mainPanelposX,self.mainPanelposY,self.mainPanelWidth,self.mainPanelHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gameover_text,(self.gameOverTextposX,self.gameOverTextposY))
            return 0

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
    
    def displayRetry(self,game):
        if self.insideRetry(game.events[0],game.events[1]):
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.buttonClicked,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.buttonHovered,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.retryTextFocused,(self.retryTextPosX,self.retryTextPosY))
        else:
            pg.draw.rect(game.screen,self.buttonColour,[self.retryPosX,self.retryPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.retryText,(self.retryTextPosX,self.retryTextPosY))
    def displayGoBack(self,game):
        if self.insideGoBack(game.events[0],game.events[1]):
            if game.events[-1][0]:
                pg.draw.rect(game.screen,self.buttonClicked,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            else:
                pg.draw.rect(game.screen,self.buttonHovered,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gobackTextFocused,(self.gobackTextPosX,self.gobackTextPosY))
        else:
            pg.draw.rect(game.screen,self.buttonColour,[self.gobackPosX,self.gobackPosY,self.buttonWidth,self.buttonHeight],border_radius=self.borderRadius)
            game.screen.blit(self.gobackText,(self.gobackTextPosX,self.gobackTextPosY))
    
    def displayOptions(self,game):
        self.displayRetry(game)
        self.displayGoBack(game)

    def displayHighScore(self,game):
        game.screen.blit(self.highScoreText,self.highScoreTextposTuple)
        for i in range(len(self.scorelis)):
            game.screen.blit(pg.font.SysFont('arialblack',self.scoreTextSize).render(self.digitmapping[self.scorelis[i]],True,self.scoreTextColour),(self.digposX+i*32,self.digposY))
        if self.newHighScore:
            self.isNewHighScore(game)