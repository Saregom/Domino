from tiles.typeTiles.tile import *

#Implementacion PATRON DECORATOR
class Tile_decorator(Tile):
    def __init__(self, tile):
        super().__init__()
        self.tile = tile
        self.side1 = self.tile.side1
        self.side2 = self.tile.side2

    def printTile(self):
        print(self.side1, self.side2)
        
    def set_image(self):
        pass

    #Metodo patron prototype
    def clone(self):
        return Tile_decorator(self.tile)