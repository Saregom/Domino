import pygame
from abc import ABC, abstractmethod #ABC: Abstract Base Clase

#Clase abstracta o interface
class Tile(ABC):
    def __init__(self):
        self.side1: int
        self.side2: int
        self.image1: pygame.surface
        self.image2: pygame.surface
        self.rect1: pygame.Rect
        self.rect2: pygame.Rect
        

    def set_position(self, x, y):
        self.rect1.x = x
        self.rect1.y = y

    def setHorizontal(self):
        self.rect2.y = self.rect1.y
        self.rect2.x = self.rect1.x+50

    def setVertical(self):
        self.rect2.x = self.rect1.x
        self.rect2.y = self.rect1.y+50

    def draw(self, screen):
        screen.blit(self.image1, self.rect1)
        screen.blit(self.image2, self.rect2)

    


    @abstractmethod
    def set_image(self):
        pass

    @abstractmethod
    def printTile(self):
        pass 

    @abstractmethod
    def clone(self):
        pass 

    # #Getters, setters, actuan como los atributos, se llaman sin el parentesis
    # @property
    # def getSide1(self):
    #     return self.__side1
    
    # @getSide1.setter
    # def setSide1(self, side1):
    #     self.__side1 = side1
    #     self.set_image()

    # @property
    # def getSide2(self):
    #     return self.__side2
    
    # @getSide2.setter
    # def setSide2(self, side2):
    #     self.__side2 = side2