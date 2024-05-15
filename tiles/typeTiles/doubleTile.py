from .tile import *

class DoubleTile(Tile):
    def __init__(self, side):
        super().__init__()
        self.side1 = side
        self.side2 = side
        self.set_image()

    def printTile(self):
        print(self.side1, self.side2)

    def set_image(self):
        self.image1 = pygame.image.load("assets/"+str(self.side1)+".jpg").convert_alpha()
        self.image2 = pygame.image.load("assets/"+str(self.side1)+".jpg").convert_alpha()
        
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()

    #Metodo patron prototype
    def clone(self):
        return DoubleTile(self.side1)