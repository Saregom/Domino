from .game_state import Game_state

class Pass_turn(Game_state):
    def execute(self): 
        return "No hay fichas para robar, cedo turno"