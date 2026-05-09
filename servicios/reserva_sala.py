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

            sala_encontrada = None
            for s in self.salas:
                if s["id"] == id_sala:
                    sala_encontrada = s
                    break

            if sala_encontrada is None:
                raise ErrorServicioNoDisponible("Sala no existe")

        # Si ocurre un error en el proceso de validación, se registra el error en el log y lanza una excepción
        except (ErrorParametroFaltante, ErrorValidacion):
            logger.error("Parametro o validacion invalida para sala %s en fecha %s", id_sala, fecha, exc_info=True)
            raise
        except ErrorServicioNoDisponible:
            logger.error("Sala %s no disponible", id_sala, exc_info=True)
            raise
        except Exception as e:
            logger.error("Error inesperado validando sala %s: %s", id_sala, str(e), exc_info=True)
            raise ErrorCalculo("No se pudo validar la sala.") from e
        else:
            try:
                if (id_sala, fecha) in self.ocupadas:
                    raise ErrorAutorizacion("Sala ocupada") # verifica si la sala ya está ocupada en la fecha solicitada

                if "precio_hora" not in sala_encontrada:
                    raise ErrorCalculo("La sala no tiene precio por hora configurado.") # verifica que la sala tenga un precio por hora configurado
                
                # Si todo es correcto, calcula el costo multiplicando el precio por hora de la sala por la cantidad de horas solicitadas
                costo = sala_encontrada["precio_hora"] * horas
                self.ocupadas.add((id_sala, fecha)) # marca la sala como ocupada para esa fecha
                logger.info("Costo calculado para sala %s: $%s", id_sala, costo)
                return costo

            # Si ocurre un error en el proceso de reserva, se registra el error en el log relacionado a la sala
            except ErrorAutorizacion:
                logger.warning("Intento de reservar sala ocupada %s en fecha %s", id_sala, fecha, exc_info=True)
                raise
            except ErrorCalculo:
                logger.error("Error de calculo para sala %s", id_sala, exc_info=True)
                raise
            except Exception as e:
                logger.error("Error inesperado calculando costo de sala %s: %s", id_sala, str(e), exc_info=True)
                raise ErrorCalculo("No se pudo calcular el costo de la sala.") from e