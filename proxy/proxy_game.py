import pygame
from proxy.interface_game import Interface_game
from observer.subscriber_alert import Subsciber_alert
from observer.subscriber_end_game_alert import Subscriber_end_game_alert
from state.game_state import Game_state

# Publisher del patron OBSERVER   Y   #Clase Context del patron STATE
class Proxy_game(Interface_game):
    def __init__(self):
        self.subscribers = [Subsciber_alert(), Subscriber_end_game_alert()]

        self.alert_access_denied_alert = False
        self.player_need_tiles_alert = False
        self.bot_need_tiles_alert = False
        self.pass_turn = False

        self.state: Game_state

    def add_observer(self, observer):
        if observer not in self.subscribers:
            self.subscribers.append(observer)

    def remove_observer(self, observer):
        if observer in self.subscribers:
            self.subscribers.remove(observer)
            
    def verify_player(self, player_turn):
        if player_turn is "player": return True
        else: return False

    def alert(self, screen ,width, height, subscriber, info):
        for sub in self.subscribers:
            if isinstance(sub, Subsciber_alert) and isinstance(sub, subscriber): sub.alert(screen, width, height, self.state.execute())
            elif isinstance(sub, Subscriber_end_game_alert) and isinstance(sub, subscriber): sub.alert(screen, width, height, info)
    
    def set_state(self, newState):
        self.state = newState
