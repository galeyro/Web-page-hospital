from abc import ABC, abstractmethod

class ICitaService(ABC):

    @abstractmethod
    def buscar_disponibilidad(self, fecha, especialidad):
        pass
