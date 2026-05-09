class ErrorDominio(Exception):
    """Errores base para excepciones del dominio en general."""

class ErrorValidacion(ErrorDominio):
    """Errores de datos inválidos o formato incorrecto."""

class ErrorParametroFaltante(ErrorValidacion):
    """Errores para cuando falta un parámetro requerido."""

class ErrorDatos(ErrorDominio):
    """Errores relacionados con operaciones en datos."""

class ErrorCalculo(ErrorDominio):
    """Errores en cálculos."""

class ErrorServicioNoDisponible(ErrorDominio):
    """Errores que indican que un servicio o recurso no se encuentra disponible."""

class ErrorAutorizacion(ErrorDominio):
    """Errores por operaciones no permitidas."""

class ErrorCliente(ErrorDominio):
    """Errores relacionados con la entidad Cliente."""

class ErrorReserva(ErrorDominio):
    """Errores relacionados con las reservas."""

class ErrorServicio(ErrorDominio):
    """Errores generales de los servicios."""

class ErrorAsesoria(ErrorServicio):
    """Errores específicos para las asesorías."""

__all__ = [
    'ErrorDominio', 'ErrorValidacion', 'ErrorParametroFaltante', 'ErrorDatos',
    'ErrorCalculo', 'ErrorServicioNoDisponible', 'ErrorAutorizacion',
    'ErrorCliente', 'ErrorReserva', 'ErrorServicio', 'ErrorAsesoria'
]