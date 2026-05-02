
from abc import ABC, abstractmethod


class EntidadBase(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass