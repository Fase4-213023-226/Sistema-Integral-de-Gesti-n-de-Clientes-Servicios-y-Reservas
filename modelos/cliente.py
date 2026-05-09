from modelos.entidad_base import EntidadBase
from excepciones.excepciones import ErrorCliente, ErrorValidacion, ErrorParametroFaltante
from utils.logger import logger

class Cliente(EntidadBase):
    # Valores del constructor para inicializar los atributos del cliente
    def __init__(self, id_cliente, nombre, correo_electronico, telefono):
        try:
            self.__id_cliente = id_cliente
            self.__nombre = nombre
            self.__correo_electronico = correo_electronico
            self.__telefono = telefono
            self.validar_datos()
        except ErrorCliente:
            raise
        except Exception as e:
            logger.error("Error inesperado creando cliente %s: %s", id_cliente, e, exc_info=True)
            raise ErrorCliente("No se pudo crear el cliente.") from e

    # Método para representar el cliente como una cadena de texto legible para las pruebas
    def __str__(self):
        return f"Cliente con ID: {self.__id_cliente} y Nombre: {self.__nombre} fue creado exitosamente."

    # Modelo de información del cliente
    def mostrar_info(self):
        return (
            f"ID Cliente: {self.__id_cliente}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo Electronico: {self.__correo_electronico}\n"
            f"Telefono: {self.__telefono}"
        )
    
    # Método que valida si los datos del cliente son correctos
    def validar_datos(self):
        try:
            if self.__id_cliente is None:
                raise ErrorParametroFaltante("El ID del cliente es obligatorio.")

            if not str(self.__id_cliente).strip():
                raise ErrorValidacion("El ID del cliente no puede estar vacio.")

            if self.__nombre is None:
                raise ErrorParametroFaltante("El nombre del cliente es obligatorio.")

            if not str(self.__nombre).strip():
                raise ErrorValidacion("El nombre del cliente no puede estar vacio.")

            if self.__correo_electronico is None:
                raise ErrorParametroFaltante("El correo electronico es obligatorio.")

            if "@" not in self.__correo_electronico:
                raise ErrorValidacion("Correo electronico es invalido.")

            if self.__telefono is None:
                raise ErrorParametroFaltante("El telefono es obligatorio.")

            if not str(self.__telefono).isdigit():
                raise ErrorValidacion("El telefono solo puede contener números.")

            if len(str(self.__telefono)) < 10 or len(str(self.__telefono)) > 15:
                raise ErrorValidacion("El telefono debe tener solo entre 10 y 15 digitos.")
            
            return True

        # Si ocurre un error en el proceso de validación, se registra el error en el log y lanza una excepción
        except ErrorCliente:
            logger.warning(
                "Error de validacion de datos del cliente %s con numero %s",
                self.__nombre,
                self.__id_cliente,
                exc_info=True,
            )
            raise

        except Exception as e:
            logger.error(
                "Error inesperado validando cliente %s con numero %s: %s",
                self.__nombre,
                self.__id_cliente,
                e,
                exc_info=True,
            )
            raise ErrorCliente("Error inesperado al validar el cliente.") from e
    
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