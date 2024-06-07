from abc import ABC, abstractmethod

#factory interface
class TileFactory(ABC):
    @abstractmethod
    def create_tile(self, side1, side2):
        pass 