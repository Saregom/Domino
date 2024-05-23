import pygame

class Fondo(object):
    _instance = None
    
    def __init__(self):
        if Fondo._instance is not None:
            raise Exception("Esta clase es un Singleton. Usa get_instance() para obtener la instancia.")
        self.image = pygame.image.load('assets/fondo.jpg')

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def draw(self, screen):
        screen.blit(self.image, (0, 0))