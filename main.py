import pygame, sys, random

ANCHO = 1280
ALTO = 720

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('DOMINO')
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Fira code", 30)

fondo = pygame.image.load('assets/fondo.jpg').convert_alpha()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

while True:
    pantalla.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    reloj.tick(60)

