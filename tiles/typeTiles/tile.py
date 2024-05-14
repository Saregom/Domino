from abc import ABC, abstractmethod

class Tile(ABC):
    @abstractmethod
    def printTile(self):
        pass 

    @abstractmethod
    def clone(self):
        pass 