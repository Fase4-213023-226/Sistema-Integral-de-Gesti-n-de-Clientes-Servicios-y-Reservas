from servicios.servicio import Servicio
from excepciones.excepciones import ServicioError
from utils.logger import logger  # logger para registrar errores

class ServicioReservaSalas(Servicio): #ServicioReservaSalas es una subclase que hereda todas las propiedades y métodos de la clase Servicio
                                      # # Esta clase maneja las reservas de salas
    def __init__(self, salas): # Guarda la lista de las salas 
        self.salas = salas
        self.ocupadas = set()   # Guarda qué salas ya están ocupadas (id, fecha)

    def describir(self): # Inicializa una cadena de texto con el encabezado
        texto = "Salas:\n" # Recorre la lista de salas almacenadas en el objeto
        for s in self.salas:# junta  el ID, nombre y precio por hora de cada sala al texto
            texto += f"{s['id']} - {s['nombre']} - ${s['precio_hora']}/hora\n" #devuelve el resumen completo 
        return texto

    def calcular_costo(self, id_sala, fecha, horas): # calcula los costos de la reserva de una sala 
        try:  # se intenta ejecutar el proceso de reserva
            for s in self.salas:
                if s["id"] == id_sala: # realiza una busqueda de la sala por su id

                    if (id_sala, fecha) in self.ocupadas: # verifica si la sala esta disponible para esas fechas 
                        raise ServicioError("Sala ocupada")  # lanza error si ya está ocupada

                    costo = s["precio_hora"] * horas  # Calcula el costo (precio por hora * horas)
                    self.ocupadas.add((id_sala, fecha))  # Guarda la reserva como ocupada
                    return costo  # Devuelve el costo total

            raise ServicioError("Sala no existe")  # si no encuentra la sala

        except ServicioError as e:  # captura el error
            logger.error(e)  # lo guarda en el log
            raise # evita que el programa falle