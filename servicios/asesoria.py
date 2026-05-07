from servicios.servicio import Servicio
from excepciones.excepciones import ServicioError
from utils.logger import logger  # se importa el logger para guardar errores en el archivo de logs

class ServicioAsesoria(Servicio):#sub clase de servicios que maneja las asesorías

    def __init__(self, temas):#guarda el listamos de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        self.temas = temas

    def describir(self):#muestra el listado de temas disponibles para asesoría, con su ID, nombre y precio por hora
        texto = "Asesorías:\n"
        for t in self.temas:
            texto += f"{t['id']} - {t['nombre']} - ${t['precio_hora']}/hora\n"#devuelve el resumen completo de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        return texto

    def calcular_costo(self, id_tema, horas):#calcula el costo de una asesoría, buscando el tema por su ID y multiplicando su precio por hora por la cantidad de horas solicitadas
        try:  # se usa try para intentar ejecutar el código y capturar errores
            for t in self.temas:
                if t["id"] == id_tema:#realiza una busqueda del tema por su ID en la lista de temas disponibles
                    return t["precio_hora"] * horas#calcula el costo de una asesoría

            raise ServicioError("Tema no existe")#si no se encuentra el tema por su ID, se lanza un error indicando que el tema no existe

        except ServicioError as e:  # captura el error personalizado
            logger.error(e)  # guarda el error en el archivo de logs
            raise  # evita que el programa se rompa