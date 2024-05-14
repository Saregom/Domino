from abc import ABC, abstractmethod
from tileFactory import *
from typeTiles.doubleTile import *

class DoubleTileFactory(TileFactory):
    def create_tile(self, side):
        return DoubleTile(side)