from .tile import *

class SimpleTile(Tile):
    def __init__(self, side1, side2):
        super().__init__()
        self.side1 = side1
        self.side2 = side2
        self.set_image()
        
    def printTile(self):
        print(self.side1, self.side2)

    def set_image(self):
        self.image1 = pygame.image.load("assets/"+str(self.side1)+".jpg").convert_alpha()
        self.image2 = pygame.image.load("assets/"+str(self.side2)+".jpg").convert_alpha()
        
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        
    #Metodo patron prototype
    def clone(self):
        return SimpleTile(self.side1, self.side2)