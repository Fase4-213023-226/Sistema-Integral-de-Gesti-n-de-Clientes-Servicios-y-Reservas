from modelos.entidad_base import EntidadBase
from excepciones.excepciones import ClienteError
from utils.logger import logger

class Cliente(EntidadBase):
    # Valores del constructor para inicializar los atributos del cliente
    def __init__(self, id_cliente, nombre, correo_electronico, telefono):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__correo_electronico = correo_electronico
        self.__telefono = telefono
        self.validar_datos()

    # Método para representar el cliente como una cadena de texto legible para las pruebas
    def __str__(self):
        return f"Cliente con ID: {self.__id_cliente} y Nombre: {self.__nombre} fue creado exitosamente."

    # Modelo de información del cliente
    def mostrar_info(self):
        return (
            f"ID Cliente: {self.__id_cliente}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo Electrónico: {self.__correo_electronico}\n"
            f"Telefono: {self.__telefono}"
        )
    
    # Método que valida si los datos del cliente son correctos
    def validar_datos(self):
        try:
            if not str(self.__id_cliente).strip():
                raise ClienteError("El ID del cliente no puede estar vacio.")

            if not self.__nombre.strip():
                raise ClienteError("El nombre del cliente no puede estar vacio.")

            if "@" not in self.__correo_electronico:
                raise ClienteError("Correo electrónico es inválido.")

            if not self.__telefono.isdigit():
                raise ClienteError("El telefono solo puede contener números.")

            if len(self.__telefono) < 10 or len(self.__telefono) > 15:
                raise ClienteError("El telefono debe tener solo entre 10 y 15 dígitos.")
            
            return True

        # Si ocurre un error en el proceso de validación, se registra el error en el log y lanza una excepción
        except ClienteError as e:
            logger.error(f"Error de validación de datos del cliente {self.__nombre} con número {self.__id_cliente}: {e}")
            raise
    
    # Métodos para acceder a los atributos del cliente de forma segura
    @property
    def id_cliente(self):
        return self.__id_cliente
    @property
    def nombre(self):
        return self.__nombre
    @property
    def correo_electronico(self):
        return self.__correo_electronico
    @property
    def telefono(self):
        return self.__telefono