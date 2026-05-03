from abc import ABC, abstractmethod

#La clase Servicio actúa como un molde (Clase Abstracta)
#Sirve para que todas las clases hijas tengan estos métodos

class Servicio(ABC):
    @abstractmethod
    def describir(self):
        pass

    @abstractmethod    
    def calcular_costo(self, *args):
        pass