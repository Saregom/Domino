from .tileFactory import *
from tiles.typeTiles.simpleTile import *

#factory concreta
class SimpleTileFactory(TileFactory):
    def create_tile(self, side1, side2):
        return SimpleTile(side1, side2)