import pygame as pg
from pygame.locals import *

class Shape:
    shapeCoordinates,squaresCoordinates,colour=None,None,None

    def __init__(self,xytuple,shapetuple,colour):
        self.shapeCoordinates=xytuple
        self.squaresCoordinates=shapetuple
        self.colour=colour

    def setGrid(self,starter):
        for item in self.squaresCoordinates:
            starter.bgrid[self.shapeCoordinates[0]+item[0]][self.shapeCoordinates[1]+item[1]]=1
    def unsetGrid(self,starter):
        for item in self.squaresCoordinates:
            starter.bgrid[self.shapeCoordinates[0]+item[0]][self.shapeCoordinates[1]+item[1]]=0

    def display(self,starter):
        for item in self.squaresCoordinates:
            coordinates=starter.indicesToCoordinates(self.shapeCoordinates[0]+item[0],self.shapeCoordinates[1]+item[1])
            pg.draw.rect(starter.game.screen,self.colour,[coordinates[0],coordinates[1],starter.game.squareSize,starter.game.squareSize])
            pg.draw.rect(starter.game.screen,'black',[coordinates[0],coordinates[1],starter.game.squareSize,starter.game.squareSize],2)