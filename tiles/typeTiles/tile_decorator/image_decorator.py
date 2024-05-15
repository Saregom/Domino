from .tile_decorator import *

#Implementacion PATRON DECORATOR
class Image_decorator(Tile_decorator):
    def __init__(self, tile):
        super().__init__(tile)
        
    def printTile(self):
        print(self.side1, self.side2)
        
    #DECORADOR: cambia imagen fichas normales por la imagen trasera de la ficha
    def set_image(self):
        self.image1 = pygame.image.load("assets/0.jpg").convert_alpha()
        self.image2 = pygame.image.load("assets/0.jpg").convert_alpha()
        
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()

    #Metodo patron prototype
    def clone(self):
        return Tile_decorator(self.tile)