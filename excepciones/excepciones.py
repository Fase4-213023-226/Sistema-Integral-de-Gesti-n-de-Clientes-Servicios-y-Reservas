class ClienteError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class ReservaError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class ServicioError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class AsesoriaError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)