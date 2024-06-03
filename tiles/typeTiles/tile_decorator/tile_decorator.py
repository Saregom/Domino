from tiles.typeTiles.tile import *

#Implementacion PATRON DECORATOR
class Tile_decorator(Tile):
    def __init__(self, tile):
        super().__init__()
        self.side1 = tile.side1
        self.side2 = tile.side2
        self.rect1 = tile.rect1
        self.rect2 = tile.rect2
        
        self.removed = tile.removed
        # tile.removed = self.removed

    def printTile(self):
        print(self.side1, self.side2)
        
    def set_image(self):
        pass

    #Metodo patron prototype
    def clone(self):
        return Tile_decorator(self.tile)