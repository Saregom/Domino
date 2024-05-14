from abc import ABC, abstractmethod

class TileFactory(ABC):
    @abstractmethod
    def create_tile(self, side1, side2):
        pass 