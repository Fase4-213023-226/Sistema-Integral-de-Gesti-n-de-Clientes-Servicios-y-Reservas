from modelos.entidad_base import EntidadBase

class Cliente(EntidadBase):
    # Valores del constructor para inicializar los atributos del cliente
    def __init__(self, id_cliente, nombre, correo_electronico, telefono):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__correo_electronico = correo_electronico
        self.__telefono = telefono

    # Modelo de información del cliente
    def mostrar_info(self):
        return (
            f"ID Cliente: {self.__id_cliente}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo Electrónico: {self.__correo_electronico}\n"
            f"Teléfono: {self.__telefono}"
        )
    
    # Método que valida si los datos del cliente son correctos
    def validar_datos(self):
        if not str(self.__id_cliente).strip():
            raise ValueError("El ID del cliente no puede estar vacio.")

        if not self.__nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacio.")

        if "@" not in self.__correo_electronico:
            raise ValueError("Correo electrónico es inválido.")

        if not self.__telefono.isdigit():
            raise ValueError("El teléfono solo puede contener números.")

        if len(self.__telefono) < 10 or len(self.__telefono) > 15:
            raise ValueError("El teléfono debe tener solo entre 10 y 15 dígitos.")
    
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