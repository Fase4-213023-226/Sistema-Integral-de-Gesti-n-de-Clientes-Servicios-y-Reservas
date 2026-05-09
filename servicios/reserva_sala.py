from servicios.servicio import Servicio
from excepciones.excepciones import (
    ErrorCalculo,
    ErrorParametroFaltante,
    ErrorAutorizacion,
    ErrorServicioNoDisponible,
    ErrorValidacion,
)
from utils.logger import logger  # logger para registrar errores

class ServicioReservaSalas(Servicio): #ServicioReservaSalas es una subclase que hereda todas las propiedades y métodos de la clase Servicio
                                      # # Esta clase maneja las reservas de salas
    def __init__(self, salas): # Guarda la lista de las salas 
        self.salas = salas or []
        self.ocupadas = set()   # Guarda qué salas ya están ocupadas (id, fecha)

    def describir(self): # Inicializa una cadena de texto con el encabezado
        texto = "Salas:\n" # Recorre la lista de salas almacenadas en el objeto
        for s in self.salas:# junta  el ID, nombre y precio por hora de cada sala al texto
            texto += f"{s['id']} - {s['nombre']} - ${s['precio_hora']}/hora\n" #devuelve el resumen completo 
        return texto

    def calcular_costo(self, id_sala, fecha, horas): # calcula los costos de la reserva de una sala 
        try:  # se intenta ejecutar el proceso de reserva
            if id_sala is None:
                raise ErrorParametroFaltante("Debe indicar el id de la sala.") # verifica que se haya proporcionado el ID de la sala

            if not fecha:
                raise ErrorParametroFaltante("Debe indicar la fecha de reserva.") # verifica que se haya proporcionado la fecha de reserva

            if horas is None:
                raise ErrorParametroFaltante("Debe indicar la cantidad de horas.") # verifica que se haya proporcionado la cantidad de horas

            if not isinstance(horas, (int, float)) or horas <= 0:
                raise ErrorValidacion("La cantidad de horas debe ser mayor que cero.") # verifica que la cantidad de horas sea un número positivo

            for s in self.salas:
                if s["id"] == id_sala: # realiza una busqueda de la sala por su id

                    if (id_sala, fecha) in self.ocupadas: # verifica si la sala esta disponible para esas fechas 
                        raise ErrorAutorizacion("Sala ocupada")  # lanza error si ya está ocupada

                    if "precio_hora" not in s:
                        raise ErrorCalculo("La sala no tiene precio por hora configurado.")

                    costo = s["precio_hora"] * horas  # Calcula el costo (precio por hora * horas)
                    self.ocupadas.add((id_sala, fecha))  # Guarda la reserva como ocupada
                    return costo  # Devuelve el costo total

            raise ErrorServicioNoDisponible("Sala no existe")  # si no encuentra la sala

        except (ErrorParametroFaltante, ErrorValidacion, ErrorAutorizacion, ErrorServicioNoDisponible, ErrorCalculo) as e: # captura el error
            logger.error("Error calculando costo de sala %s en fecha %s: %s", id_sala, fecha, e, exc_info=True) # lo guarda en el log
            raise # evita que el programa falle

        except Exception as e: # captura cualquier error inesperado
            logger.error("Error inesperado calculando costo de sala %s: %s", id_sala, e, exc_info=True)
            raise ErrorCalculo("No se pudo calcular el costo de la sala.") from e