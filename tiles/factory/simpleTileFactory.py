from abc import ABC, abstractmethod
from .tileFactory import *
from tiles.typeTiles.simpleTile import *

class SimpleTileFactory(TileFactory):
    def create_tile(self, side1, side2):
        return SimpleTile(side1, side2)