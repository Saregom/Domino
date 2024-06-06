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

        self.removed = False
        self.disable = False

        self.valid_at_left = False
        self.valid_at_right = False

    def set_position(self, x, y):
        self.rect1.x = x
        self.rect1.y = y

    def set_horizontal(self):
        self.rect2.x = self.rect1.x+50
        self.rect2.y = self.rect1.y

    def set_horizontal_reverse(self):
        self.rect2.x = self.rect1.x-50
        self.rect2.y = self.rect1.y

    def set_vertical(self):
        self.rect2.x = self.rect1.x
        self.rect2.y = self.rect1.y+50

    def draw(self, screen):
        if self.disable:
            self.image1.set_alpha(80)
            self.image2.set_alpha(80)
        else:
            self.image1.set_alpha(255) #255: 100%
            self.image2.set_alpha(255)

        screen.blit(self.image1, self.rect1)
        screen.blit(self.image2, self.rect2)

    def is_class(self, get_class):
        return isinstance(self, get_class)


    @abstractmethod
    def set_image(self):
        pass

    @abstractmethod
    def print_tile(self):
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