from abc import ABC, abstractmethod

class Interface_game(ABC):
    @abstractmethod
    def verify_player(self): pass
