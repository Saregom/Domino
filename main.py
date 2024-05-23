import pygame, sys, random
from typing import List

from tiles.factory.simpleTileFactory import SimpleTileFactory
from tiles.factory.doubleTileFactory import DoubleTileFactory
from tiles.typeTiles.simpleTile import SimpleTile
from tiles.typeTiles.doubleTile import DoubleTile
from tiles.typeTiles.tile import Tile
from tiles.typeTiles.tile_decorator.image_decorator import Image_decorator
from fondo_singleton.Fondo import Fondo


#---------------------- Inicializacion pygame, ventana y atributos
WIDHT = 1800
HEIGHT = 1013

pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption('DOMINO')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fira code", 30)

TIEMPO_SEGUNDO = pygame.USEREVENT + 1

#---------------------- Clase juego, inicilizacion de variables
class Game():
    def __init__(self):
        self.total_tiles = [] #Almacena las 28 fichas del domino

        self.player_tiles = []
        self.bot_tiles = []
        self.remaining_tiles = [] #Total de fichas sobrantes de la partida

        self.center_tile = []
        self.tiles_played_left = []
        self.tiles_played_right = []
        
        self.turno = "player"

        pygame.time.set_timer(TIEMPO_SEGUNDO, 3000)

    def show_tiles(self):
        if len(self.center_tile) != 0:
            self.center_tile[0].draw(screen)

game = Game()

#---------------------- Instancia unica del fondo, uso del patrón SINGLETON
fondo = Fondo.get_instance()

#---------------------- Seteo de fichas, implementacion PATRON ABSTRACT FACTORY, y PATRON PROTOTYPE
simpleFactory = SimpleTileFactory()
doubleFactory = DoubleTileFactory()

simpleTile = simpleFactory.create_tile(0, 1)
doubleTile = doubleFactory.create_tile(0)

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
        game.total_tiles.append(cloned_tile)

#----------------------Reparticion de fichas: tanto el juagdor como el bot cogen fichas de la lista de fichas restantes (lista, cantidad de fichas a coger)
game.remaining_tiles = game.total_tiles.copy()
def take_tiles(list: List, tiles_to_take):
    for i in range(tiles_to_take):
        random_tile = random.randint(0, len(game.remaining_tiles)-1)
        list.append(game.remaining_tiles.pop(random_tile))

take_tiles(game.player_tiles, 7)
take_tiles(game.bot_tiles, 7)

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
        
        width_position_tiles -= 55
        if not tile.removed:
            tile.draw(screen)
   
#---------------------- ubicar la ficha inicial (central)
def set_center_tile(tiles_list):
    pygame.time.set_timer(TIEMPO_SEGUNDO, 0)
    tile_center:Tile
    biggest_center = 0

    for j in range(2):
        for i in range(7):
            for tile in tiles_list[j]:
                if tile.side1 == i and tile.side2 == i and i > biggest_center:
                    biggest_center = i
                    tile_center = tile
                    break

    game.center_tile.append(DoubleTile(tile_center.side1))
    game.center_tile[0].set_position(WIDHT/2-25, HEIGHT/2-50)
    game.center_tile[0].setVertical()

    for j in range(2):
        for tile in tiles_list[j]:
            if tile == tile_center:
                if j == 0: game.turno = "bot"
                else: game.turno = "player"
                tile.removed = True

# for tile in game.player_tiles:
#     tile.printTile()

# print("")
# for tile in game.bot_tiles:
#     tile.printTile()
# print("")

#---------------------- Bucle de juego, (60fps)
following_mouse = False
current_tile:Tile = None

while True:
    fondo.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
#--------- Mover ficha con mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for tile in game.player_tiles:
                if tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos):
                    if event.button == pygame.BUTTON_LEFT:
                        current_tile = tile
                        following_mouse = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1):  # Botón izquierdo del mouse
                following_mouse = False

        # ---------- Tiempo inicial para poner ficha central
        if event.type == TIEMPO_SEGUNDO:
            set_center_tile([game.player_tiles, game.bot_tiles])
                        
    if following_mouse is True:
        mouse_pos = pygame.mouse.get_pos()
        current_tile.set_position(mouse_pos[0], mouse_pos[1])
        current_tile.setVertical()
        current_tile.draw(screen)

#--------- 
    set_Tiles(game.player_tiles, HEIGHT-120, False)
    set_Tiles(game.bot_tiles, 20, True)  

    game.show_tiles()  
    
    pygame.display.update()
    clock.tick(60)