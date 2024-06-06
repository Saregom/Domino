import pygame, random
from typing import List

from tiles.typeTiles.tile import Tile
from tiles.factory.simpleTileFactory import SimpleTileFactory
from tiles.factory.doubleTileFactory import DoubleTileFactory
from tiles.typeTiles.doubleTile import DoubleTile

from proxy.interface_game import Interface_game

class Game(Interface_game):
    def __init__(self, total_player_points, total_bot_points, SET_CENTER_TILE_TIME):
        self.total_tiles = [] #Almacena las 28 fichas del domino

        self.remaining_tiles = [] #Total de fichas sobrantes de la partida
        self.player_tiles = []
        self.bot_tiles = []

        self.center_tile = []
        self.played_left_tiles = []
        self.played_right_tiles = []
        self.left_sides = []
        self.right_sides = []

        self.show_side_options = False
        self.tile_available_both_sides:Tile 
        
        self.player_turn = "player"
        self.playing_turn = True

        self.can_take_tile = False

        self.player_bot_can_play = [True, True] #[player perdio, bot perdio]
        self.finished = False

        self.total_player_points = total_player_points
        self.total_bot_points = total_bot_points

        pygame.time.set_timer(SET_CENTER_TILE_TIME, 1000)

    #--------- Seteo de fichas, implementacion PATRON ABSTRACT FACTORY, y PATRON PROTOTYPE
    def create_tiles(self):
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
                self.total_tiles.append(cloned_tile)

    #--------- (lista, cantidad de fichas a coger)
    def take_tiles(self, list:List, tiles_to_take):
        for i in range(tiles_to_take):
            random_tile = random.randint(0, len(self.remaining_tiles)-1)
            list.append(self.remaining_tiles.pop(random_tile)) # Se agrega una ficha aleatoria a la lista pasada y se elimina de las fichas restantes

    #--------- Reparticion de fichas: tanto el juagdor como el bot cogen fichas de la lista de fichas restantes 
    def distribute_tiles(self):
        self.remaining_tiles = self.total_tiles.copy() # Se almacenan la copia de todas las fichas

        # Verificar si hay una ficha doble, si no, vuelve a repartir fichas
        there_is_double = False
        while not there_is_double:  
            print("\nReparticion")
            self.player_tiles = []
            self.bot_tiles = []
            self.take_tiles(self.player_tiles, 7)
            self.take_tiles(self.bot_tiles, 7)

            for tiles_list in [self.player_tiles, self.bot_tiles]:
                for tile in tiles_list:
                    if tile.is_class(DoubleTile):
                        there_is_double = True

            if not there_is_double: print("No doble")

        random.shuffle(self.remaining_tiles) # Las fichas restantes se mezclan para que no esten en el orden en q se agregaron

    #---------------------- ubicar la ficha inicial (central)
    def set_center_tile(self, SET_CENTER_TILE_TIME):
        pygame.time.set_timer(SET_CENTER_TILE_TIME, 0) #detine el evento (0), para que se deje de llamar
        
        tiles_list = [self.player_tiles, self.bot_tiles]
        tile_center:Tile
        biggest_center = 0

        for j, list in enumerate(tiles_list):
            for i in range(7):
                for tile in list:
                    if tile.is_class(DoubleTile) and tile.side1 == i and i > biggest_center:
                        biggest_center = i
                        tile_center = tile
                        break

        self.center_tile.append(tile_center.clone())

        for j in range(2):
            for tile in tiles_list[j]:
                if tile == tile_center:
                    if j == 0: self.player_turn = "bot"
                    else: self.player_turn = "player"
                    tile.removed = True

        self.playing_turn = False

    def verify_player(self):
        pass
