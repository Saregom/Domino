import pygame, sys, random
from tiles.typeTiles.simpleTile import SimpleTile
from tiles.typeTiles.doubleTile import DoubleTile
from tiles.typeTiles.tile import Tile
from tiles.typeTiles.decorator.image_decorator import Image_decorator
from typing import List

#---------------------- Inicializacion pygame, ventana y atributos
WIDHT = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption('DOMINO')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fira code", 30)

fondo = pygame.image.load('assets/fondo.jpg').convert_alpha()
fondo = pygame.transform.scale(fondo, (WIDHT, HEIGHT))



#---------------------- Seteo de fichas, implementacion PATRON PROTOTYPE
doubleTile = DoubleTile(0)
simpleTile = SimpleTile(0, 1)

total_tiles = [] #Almacena las 28 fichas del domino

for i in range(0, 7):
    for j in range(i, 7):
        cloned_tile: Tile
        if i != j:
            cloned_tile = simpleTile.clone()
        else:
            cloned_tile = doubleTile.clone()
        
        cloned_tile.side1 = i
        cloned_tile.side2 = j
        cloned_tile.set_image()
        total_tiles.append(cloned_tile)

#Reparticion de fichas
player_tiles: Tile = []
bot_tiles = []
remaining_tiles = total_tiles.copy() #Total de fichas sobrantes de la partida

#tanto el juagdor como el bot cogen fichas de la lista de fichas restantes (lista, cantidad de fichas a coger)
def take_tiles(list: List, tiles_to_take):
    for i in range(tiles_to_take):
        random_tile = random.randint(0, len(remaining_tiles)-1)
        list.append(remaining_tiles.pop(random_tile))

take_tiles(player_tiles, 7)
take_tiles(bot_tiles, 7)

#---------------------- ubicar fichas en tablero
def set_Tiles(tiles_list:List, height, is_bot):
    width_position_tiles = 190 #diferencia de posiciones de cada ficha en x

    for tile in tiles_list:
        tile:Tile
        if is_bot:
            tile = Image_decorator(tile)#patron DECORATOR, cambia imagen fichas
            tile.set_image()
        
        tile.set_position((WIDHT/2)-width_position_tiles, height) #(x, y)
        tile.setVertical()
        tile.draw(screen)
        width_position_tiles -= 55

#---------------------- Bucle de juego, (60fps)
while True:
    screen.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    set_Tiles(player_tiles, HEIGHT-120, False)
    set_Tiles(bot_tiles, 20, True)

    pygame.display.update()
    clock.tick(60)

