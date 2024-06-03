import pygame
from tiles.typeTiles.tile import Tile
from tiles.proxy.interface_game import Interface_game

class Game(Interface_game):
    
    def __init__(self, SET_CENTER_TILE_TIME):
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

        pygame.time.set_timer(SET_CENTER_TILE_TIME, 1000)
        

    def verify_player(self):
        if self.player_turn is "player":
            return True
        else:
            return False
            
