from abc import ABC, abstractmethod

class Interface_subscriber(ABC):
    @abstractmethod
    def alert(self, message):
        pass