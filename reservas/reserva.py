from datetime import datetime, timedelta #Importa la herramienta para manejar fechas, horas y calculos de duración


class ReservaError(Exception): #Excepcion para manejo de errores de reserva mientras se implementa el archivo Excepciones
    pass



class Reserva: #Clase que representa y se encarga de gestionar la reserva en el sistema 
    

    # Lista global compartida por todas las reservas para simular almacenamiento de reservas activas
    reservas_registradas = []

    # Constructor, Inicializa una nueva reserva con sus datos principales
    def __init__(self, id_reserva, cliente, servicio, fecha_hora_inicio, duracion_horas):
        self.__id_reserva = id_reserva                  # Identificador único de la reserva
        self.__cliente = cliente                        # Objeto cliente asociado
        self.__servicio = servicio                      # Objeto servicio asociado
        self.__fecha_hora_inicio = fecha_hora_inicio    # Fecha y hora de inicio
        self.__duracion_horas = duracion_horas          # Duración en horas
        self.__estado = "Pendiente"                     # Estado inicial de la reserva

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

    # Validación de datos de reserva
    def validar_reserva(self): #Verifica que todos los datos ingresados sean correctos
        if not str(self.__id_reserva).strip(): ## El ID no puede estar vacío
            raise ReservaError("El ID de la reserva no puede estar vacío.")

        if self.__cliente is None or not hasattr(self.__cliente, "nombre"): #Verifica que exista cliente y que tenga atributo nombre
            raise ReservaError("La reserva debe tener un cliente válido.")

        if self.__servicio is None or not hasattr(self.__servicio, "describir"): #Verifica que exista servicio y tenga método describir
            raise ReservaError("La reserva debe tener un servicio válido.")

        if not isinstance(self.__fecha_hora_inicio, datetime): #Valida que la fecha sea un objeto datetime
            raise ReservaError("La fecha y hora de inicio no son válidas.")

        if self.__duracion_horas <= 0: #La duración debe ser mayor que cero
            raise ReservaError("La duración debe ser mayor a cero.")

    # Validar conflictos con otras reservas
    def validar_conflicto(self): #Comprueba si ya existe otra reserva en el mismo horario para el mismo servicio
        nueva_inicio = self.__fecha_hora_inicio #Define inicio y fin de la nueva reserva
        nueva_fin = nueva_inicio + timedelta(hours=self.__duracion_horas) 

        for reserva in Reserva.reservas_registradas: ##Recorre todas las reservas registradas
            if reserva.servicio == self.__servicio and reserva.estado != "Cancelada": #Compara reservas del mismo servicio y que no estén canceladas

                existente_inicio = reserva.fecha_hora_inicio #Obtiene horario de reserva existente
                existente_fin = existente_inicio + timedelta(hours=reserva.duracion_horas)

                # Valida cruce de horarios
                if nueva_inicio < existente_fin and nueva_fin > existente_inicio:
                    raise ReservaError(
                        f"Conflicto detectado: El servicio '{self.__servicio.nombre_servicio}' "
                        f"ya está reservado en ese horario."
                    )

    # Confirmar reserva
    def confirmar(self): #Valida y registra oficialmente la reserva
        self.validar_reserva() #Verifica datos correctos
        self.validar_conflicto() #Verifica disponibilidad

        self.__estado = "Confirmada" #Cambia estado a confirmada

        Reserva.reservas_registradas.append(self) #Guarda en lista global

        return f"Reserva {self.__id_reserva} confirmada exitosamente."

    # Cancelar reserva
    def cancelar(self): # Cambia el estado de una reserva a cancelada

        if self.__estado == "Cancelada": #Evita cancelar dos veces
            raise ReservaError("La reserva ya fue cancelada.")

        self.__estado = "Cancelada" #Actualiza estado
        return f"Reserva {self.__id_reserva} cancelada correctamente."

    # Procesar reserva
    def procesar(self): #Marca una reserva como completada

        if self.__estado != "Confirmada": #Solo reservas confirmadas pueden procesarse
            raise ReservaError("Solo se pueden procesar reservas confirmadas.")

        self.__estado = "Procesada" #Actualiza estado
        return f"Reserva {self.__id_reserva} procesada exitosamente."

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