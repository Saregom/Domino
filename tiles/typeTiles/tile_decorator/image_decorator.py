from .tile_decorator import *

#Implementacion PATRON DECORATOR
class Image_decorator(Tile_decorator):
    def __init__(self, tile):
        super().__init__(tile)
        self.set_image()
        
    def print_tile(self):
        print(self.side1, self.side2)
        
    #DECORADOR: cambia imagen fichas normales por la imagen trasera de la ficha
    def set_image(self):
        self.image1 = pygame.image.load("assets/0.png").convert_alpha()
        self.image2 = pygame.image.load("assets/0.png").convert_alpha()
        
    #Metodo patron prototype
    def clone(self):
        return Image_decorator(self.tile)
