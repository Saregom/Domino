from .tile import *

class DoubleTile(Tile):
    def __init__(self, side):
        self.__side1 = side
        self.__side2 = side

    def printTile(self):
        print(self.__side1, self.__side2)

    #Metodo patron prototype
    def clone(self):
        return DoubleTile(self.__side1)

    #Getters, setters, actuan como los atributos, se llaman sin el parentesis
    @property
    def getSide1(self):
        return self.__side1
    
    @getSide1.setter
    def setSide1(self, side1):
        self.__side1 = side1

    @property
    def getSide2(self):
        return self.__side2
    
    @getSide2.setter
    def setSide2(self, side2):
        self.__side2 = side2