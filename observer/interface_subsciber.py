from abc import ABC, abstractmethod

class AbstractSubscriber(ABC):
    @abstractmethod
    def alert(self, message):
        pass