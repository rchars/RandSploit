from abc import ABC, abstractmethod


class KeywordIface(ABC):
        def __init__(self, name):
                self.name = name

        @abstractmethod
        def complete(self):
                pass

        @abstractmethod
        def execute(self):
                pass