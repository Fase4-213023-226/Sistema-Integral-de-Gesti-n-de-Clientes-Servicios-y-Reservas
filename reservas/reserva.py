from datetime import datetime, timedelta #Importa la herramienta para manejar fechas, horas y calculos de duración
from modelos.entidad_base import EntidadBase
from excepciones.excepciones import ErrorReserva
import logging

#class ReservaError(Exception): #Excepcion para manejo de errores de reserva mientras se implementa el archivo Excepciones
#    pass

logger = logging.getLogger(__name__)


class Reserva(EntidadBase): #Clase que representa y se encarga de gestionar la reserva en el sistema 
    

    # Lista global compartida por todas las reservas para simular almacenamiento de reservas activas
    reservas_registradas = []

    # Constructor, Inicializa una nueva reserva con sus datos principales
    def __init__(self, id_reserva, cliente, servicio, fecha_hora_inicio, duracion_horas):
        try:
            super().__init__()

            if cliente is None:
                raise ErrorReserva("El cliente no puede ser nulo")
            
            self.__id_reserva = id_reserva
            self.id_entidad = id_reserva
            
            if not isinstance(fecha_hora_inicio, datetime):
                raise ErrorReserva("La fecha debe ser de tipo datetime")

            if not isinstance(duracion_horas, (int, float)):
                raise ErrorReserva("La duración debe ser numérica")
            
            
            self.__id_reserva = id_reserva                  # Identificador único de la reserva
            self.__cliente = cliente                        # Objeto cliente asociado
            self.__servicio = servicio                      # Objeto servicio asociado
            self.__fecha_hora_inicio = fecha_hora_inicio    # Fecha y hora de inicio
            self.__duracion_horas = duracion_horas          # Duración en horas
            self.servicios_contratados = []
            self.__estado = "Pendiente"                     # Estado inicial de la reserva
            

            logger.info(f"Reserva creada ID: {id_reserva} para el cliente: {cliente.nombre}")

        except Exception as e:
            logger.error(f"Error al crear reserva: {str(e)}")
            raise ErrorReserva(f"Error al inicializar la reserva: {str(e)}")
        

    # Método para mostrar información de la reserva
    def mostrar_info(self):
        fecha_fin = self.__fecha_hora_inicio + timedelta(hours=self.__duracion_horas) #Calcula la hora final sumando duracion a la hora inicial
        nombre_servicio = type(self.__servicio).__name__ #Obtiene automáticamente el nombre de la clase del servicio

        return ( #Retorna la información
            f"ID Reserva: {self.__id_reserva}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {nombre_servicio}\n"
            f"Inicio: {self.__fecha_hora_inicio}\n"
            f"Fin: {fecha_fin}\n"
            f"Duración: {self.__duracion_horas} hora(s)\n"
            f"Estado: {self.__estado}"
        )
    
    def procesar_reserva(self, servicio, **kwargs):
        try:
            costo = servicio.calcular_costo(**kwargs)

            registro = {
                "servicio": servicio,
                "costo": costo,
                "detalles": kwargs
            }

            self.servicios_contratados.append(registro)
            logger.info(f"Servicio {type(servicio).__name__} añadido a reserva {self.id_reserva}")
            return f"Servicio {type(servicio).__name__} añadido correctamente a la reserva."

        except Exception as e:
            logger.critical(f"Error crítico en reserva {self.id_reserva}: {str(e)}")
            raise ErrorReserva("Error interno al procesar la reserva.")
        

    # Validación de datos de reserva
    def validar_reserva(self): #Verifica que todos los datos ingresados sean correctos
        try:
            if not str(self.id_reserva).strip():
                raise ErrorReserva("El ID de la reserva no puede estar vacío.")

            if self.cliente is None or not hasattr(self.cliente, "nombre"):
                raise ErrorReserva("La reserva debe tener un cliente válido.")

            if not isinstance(self.fecha_hora_inicio, datetime):
                raise ErrorReserva("La fecha de inicio debe ser válida.")

            fecha_fin = self.fecha_hora_inicio + timedelta(hours=self.duracion_horas)

            if fecha_fin <= self.fecha_hora_inicio:
                raise ErrorReserva("La fecha de fin debe ser posterior a la de inicio.")

        except ErrorReserva as e:
            logger.warning(f"Validación general fallida en reserva {self.id_reserva}: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Error inesperado en validación general: {str(e)}")
            raise ErrorReserva("Error en validación de la reserva.")

    # Validar conflictos con otras reservas
    def validar_conflicto(self): #Comprueba si ya existe otra reserva en el mismo horario para el mismo servicio
        try:
             # Fecha final de la reserva actual
            fecha_fin_actual = (
            self.fecha_hora_inicio +
            timedelta(hours=self.duracion_horas))

            # Recorrer reservas ya registradas
            for reserva in Reserva.reservas_registradas:

                # Evitar compararse consigo misma
                if reserva.id_reserva == self.id_reserva:
                    continue

                # Fecha final de la reserva existente
                fecha_fin_reserva = (
                    reserva.fecha_hora_inicio +
                    timedelta(hours=reserva.duracion_horas))

                # Validación de cruce de horarios
                conflicto = (
                    self.fecha_hora_inicio < fecha_fin_reserva
                    and
                    fecha_fin_actual > reserva.fecha_hora_inicio)

                if conflicto:
                    raise ErrorReserva(f"Conflicto detectado con la reserva {reserva.id_reserva}")

            logger.info(f"Reserva {self.id_reserva} validada sin conflictos.")
            return "Reserva validada sin conflictos."

        except ErrorReserva as e:

            logger.warning(str(e))
            raise

        except Exception as e:

            logger.error(f"Error validando conflicto de reserva: {str(e)}")
            raise ErrorReserva("Error al validar conflicto de reserva.")


    # Confirmar reserva
    def confirmar(self): #Valida y registra oficialmente la reserva
        try:
            self.validar_reserva() #Verifica datos correctos

            self.validar_conflicto() #Verifica disponibilidad
            if not self.servicios_contratados:
                raise ErrorReserva("No se puede confirmar una reserva sin servicios.")

            self.__estado = "CONFIRMADA" #Cambia estado a confirmada
            Reserva.reservas_registradas.append(self) #Guarda en lista global

            logger.info(f"Reserva {self.id_reserva} CONFIRMADA exitosamente.")
            return f"Reserva {self.id_reserva} Confirmada exitosamente."

        except ErrorReserva as e:
            logger.error(f"Error al confirmar reserva {self.id_reserva}: {str(e)}")
            raise
        

    # Cancelar reserva
    def cancelar(self): # Cambia el estado de una reserva a cancelada
        try:
            if self.__estado == "COMPLETADA": #Evita cancelar dos veces
                raise ErrorReserva("No se puede cancelar una reserva ya finalizada.")

            self.__estado = "CANCELADA" #Actualiza estado

            logger.info(f"Reserva {self.id_reserva} CANCELADA.")
            return f"Reserva {self.id_reserva} cancelada correctamente."

        except ErrorReserva as e:
            logger.warning(f"Cancelación inválida {self.id_reserva}: {str(e)}")
            raise


    # Procesar reserva
    def procesar(self): #Marca una reserva como completada
        try:
            if self.__estado != "CONFIRMADA": #Solo reservas confirmadas pueden procesarse
                raise ErrorReserva("Solo se pueden completar reservas confirmadas.")

            self.__estado = "COMPLETADA" #Actualiza estado

            logger.info(f"Reserva {self.id_reserva} COMPLETADA.")
            return f"Reserva {self.id_reserva} completada correctamente."

        except ErrorReserva as e:
            logger.error(f"Error al completar reserva {self.id_reserva}: {str(e)}")
            raise

    def obtener_total(self):
        try:
            return sum(s["costo"] for s in self.servicios_contratados)

        except Exception as e:
            logger.error(f"Error calculando total en reserva {self.id_reserva}: {str(e)}")
            raise ErrorReserva("Error al calcular el total.")
        
    def mostrar(self):
        try:
            resumen = f"\n--- DETALLE DE RESERVA {self.id_reserva} ---\n"
            resumen += f"Cliente: {self.cliente.nombre} | Estado: {self.__estado}\n"
            resumen += "Servicios:\n"

            for s in self.servicios_contratados:
                resumen += f" > {s['servicio'].describir()} -> subtotal: ${s['costo']}\n"

            resumen += f"TOTAL FINAL: ${self.obtener_total()}\n"
            return resumen

        except Exception as e:
            logger.error(f"Error mostrando reserva {self.id_reserva}: {str(e)}")
            return "Error al mostrar la información."

    def __str__(self):
        try:
            return (
                f"Reserva {self.id_reserva} [{self.__estado}] - "
                f"Cliente: {self.cliente.nombre} - Total: ${self.obtener_total()}"
            )
        except Exception:
            return f"Reserva {self.id_reserva} [ERROR AL MOSTRAR]"

    # Simulación de operación
    @staticmethod
    def simular_operacion(): #Muestra todas las reservas registradas
        print("=== Reservas Registradas ===")
        if not Reserva.reservas_registradas:
            print("No hay reservas registradas.")
        else: #Si existen reservas, muestra cada una
            for reserva in Reserva.reservas_registradas:
                print(reserva.mostrar_info())
                print("-" * 40)

    # Propiedades seguras 
    @property #Permiten acceso controlado a atributos privados
    def id_reserva(self):
        return self.__id_reserva

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def fecha_hora_inicio(self):
        return self.__fecha_hora_inicio

    @property
    def duracion_horas(self):
        return self.__duracion_horas

    @property
    def estado(self):
        return self.__estado