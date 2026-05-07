
from servicios.servicio import Servicio
from datetime import datetime, timedelta #sirve para importar las clases necesarias para gestionar fechas, horas y realizar cálculos temporales.
from excepciones.excepciones import ServicioError
from utils.logger import logger  # logger para registrar errores

class ServicioAlquilerEquipos(Servicio): #sub calse de servicios que maneja el alquiler de los equipos

    def __init__(self, equipos): # guarda el listado de equipos
        self.equipos = equipos
        self.alquileres = {} #guarda los alquileres realizados (id_equipo, fecha) 

    def describir(self):#muestra el listado de equipos disponibles para alquilar, con su ID, nombre y precio por día
        texto = "Equipos:\n"
        for e in self.equipos:
            texto += f"{e['id']} - {e['nombre']} - ${e['precio_dia']}/día\n"
        return texto

    def calcular_costo(self, id_equipo, cantidad, fecha_inicio, dias):# calcula el costo del alquiler de un equipo, verificando su disponibilidad para las fechas solicitadas
        try:  # se intenta ejecutar todo el proceso de alquiler
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")#convierte la fecha de texto a un objeto datetime para facilitar los cálculos de fechas

            for e in self.equipos:#busca el equipo por su ID en la lista de equipos disponibles
                if e["id"] == id_equipo:

                    for i in range(dias):# recorre  los dias de alquiler para verificar la disponibilidad del equipo
                        dia = (inicio + timedelta(days=i)).strftime("%Y-%m-%d")#calcula la fecha de cada día del alquiler sumando i días a la fecha de inicio 
                        usadas = self.alquileres.get((id_equipo, dia), 0)#consulta cuantos equipos ya están alquilados para ese día

                        if usadas + cantidad > e["unidades"]:#verifica si hay unidades disponibles 
                            raise ServicioError("No disponible")#lanza error si no hay disponibilidad

                    for i in range(dias):#guarda el alquiler dia por dia
                        dia = (inicio + timedelta(days=i)).strftime("%Y-%m-%d")
                        self.alquileres[(id_equipo, dia)] = self.alquileres.get((id_equipo, dia), 0) + cantidad

                    return e["precio_dia"] * dias * cantidad#calcula el costo total del alquiler

            raise ServicioError("Equipo no existe")#si no se encuentra el equipo por su ID

        except ServicioError as e:  # captura el error
            logger.error(e)  # lo guarda en el archivo de logs
            raise  # evita que el programa se detenga