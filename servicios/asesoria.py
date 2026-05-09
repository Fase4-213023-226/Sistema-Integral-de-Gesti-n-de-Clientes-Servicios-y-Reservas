from servicios.servicio import Servicio
from excepciones.excepciones import (
    ErrorCalculo,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
    ErrorValidacion,
)
from utils.logger import logger  # se importa el logger para guardar errores en el archivo de logs

class ServicioAsesoria(Servicio):#sub clase de servicios que maneja las asesorías

    def __init__(self, temas):#guarda el listamos de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        self.temas = temas or []

    def describir(self):#muestra el listado de temas disponibles para asesoría, con su ID, nombre y precio por hora
        texto = "Asesorías:\n"
        for t in self.temas:
            texto += f"{t['id']} - {t['nombre']} - ${t['precio_hora']}/hora\n"#devuelve el resumen completo de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        return texto

    def calcular_costo(self, id_tema, horas):#calcula el costo de una asesoría, buscando el tema por su ID y multiplicando su precio por hora por la cantidad de horas solicitadas
        try:  # se usa try para intentar ejecutar el código y capturar errores
            if id_tema is None:
                raise ErrorParametroFaltante("Debe indicar el id del tema.") # verifica que se haya proporcionado el ID del tema

            if horas is None:
                raise ErrorParametroFaltante("Debe indicar la cantidad de horas.") # verifica que se haya proporcionado la cantidad de horas

            if not isinstance(horas, (int, float)) or horas <= 0:
                raise ErrorValidacion("Las horas deben ser mayores que cero.") # verifica que la cantidad de horas sea un numero positivo

            for t in self.temas:
                if t["id"] == id_tema:#realiza una busqueda del tema por su ID en la lista de temas disponibles
                    if "precio_hora" not in t:
                        raise ErrorCalculo("El tema no tiene precio por hora configurado.") # verifica que el tema tenga un precio por hora configurado

                    return t["precio_hora"] * horas#calcula el costo de una asesoría

            raise ErrorServicioNoDisponible("Tema no existe")#si no se encuentra el tema por su ID, se lanza un error indicando que el tema no existe

        except (ErrorParametroFaltante, ErrorValidacion, ErrorServicioNoDisponible, ErrorCalculo) as e:  # captura el error personalizado
            logger.error("Error calculando asesoria %s: %s", id_tema, e, exc_info=True)
            raise  # evita que el programa se rompa

        except Exception as e: # captura cualquier error inesperado
            logger.error("Error inesperado calculando asesoria %s: %s", id_tema, e, exc_info=True)
            raise ErrorCalculo("No se pudo calcular el costo de la asesoria.") from e # lanza un error de cálculo si se recibe cualquier error inesperado