from .game_state import Game_state

class Game_over(Game_state):
    def execute(self): 
        return "El juego ha finalizado"