import pygame as pg
from pygame.locals import *

class Button:
    posX,posY=0,0
    text=None
    bgcolour,textcolour=None,None
    bgcolour_clicked,bgbordercolour_hovered=None,None

    size,hoveredSize,borderThickness=26,30,6
    width,height,borderRadius=300,70,15

    def __init__(self,poss,text,starter):
        self.posX,self.posY=poss[0],poss[1]
        self.text=text
        self.bgcolour=starter.buttonbgcolour
        self.textcolour=starter.buttontextcolour
        self.bgcolour_clicked=starter.buttonClickbgColour
        self.bgbordercolour_hovered=starter.buttonHoverBorderColour

    def getCoordinates(self,textobj):
        return (self.posX+int((self.width-textobj.get_width())/2),self.posY+int((self.height-textobj.get_height())/2))
    
    def show(self,game,state):
        if state==0: # no hover
            pg.draw.rect(game.screen,self.bgcolour,[self.posX,self.posY,self.width,self.height],border_radius=self.borderRadius)
            textobj=pg.font.SysFont('kristenitc',self.size).render(self.text,True,self.textcolour,self.bgcolour)
            game.screen.blit(textobj,self.getCoordinates(textobj))
        elif state==1: # hover
            pg.draw.rect(game.screen,self.bgcolour,[self.posX,self.posY,self.width,self.height],border_radius=self.borderRadius)
            pg.draw.rect(game.screen,self.bgbordercolour_hovered,[self.posX,self.posY,self.width,self.height],self.borderThickness,border_radius=self.borderRadius)
            textobj=pg.font.SysFont('kristenitc',self.hoveredSize,pg.font.Font.bold).render(self.text,True,self.textcolour,self.bgcolour)
            game.screen.blit(textobj,self.getCoordinates(textobj))
        else: # click
            pg.draw.rect(game.screen,self.bgcolour_clicked,[self.posX,self.posY,self.width,self.height],border_radius=self.borderRadius)
            pg.draw.rect(game.screen,self.bgbordercolour_hovered,[self.posX,self.posY,self.width,self.height],self.borderThickness,border_radius=self.borderRadius)
            textobj=pg.font.SysFont('kristenitc',self.hoveredSize,pg.font.Font.bold).render(self.text,True,self.textcolour,self.bgcolour_clicked)
            game.screen.blit(textobj,self.getCoordinates(textobj))