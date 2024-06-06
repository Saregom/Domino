from abc import ABC, abstractmethod

class Game_state(ABC):
    @abstractmethod
    def execute(self): pass
