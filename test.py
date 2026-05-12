"""
Pruebas para demostrar el manejo robusto de excepciones en el sistema.

Cubre casos de:
- Datos inválidos
- Parámetros faltantes
- Servicios no disponibles
- Intentos de reserva incorrectos
- Cálculos inconsistentes
"""

from modelos.cliente import Cliente
from servicios.reserva_sala import ServicioReservaSalas
from servicios.alquiler_equipo import ServicioAlquilerEquipos
from servicios.asesoria import ServicioAsesoria
from excepciones.excepciones import ErrorDominio
from utils.logger import logger


def test_cliente_validacion():
    # Prueba de validacion de datos del cliente en casos de error
    print("\n=== TEST: Validación de Cliente ===")

    casos = [
        ("ID no definido", lambda: Cliente(None, "Juan", "juan@example.com", "1234567890")),
        ("Nombre vacío", lambda: Cliente(1, "", "juan@example.com", "1234567890")),
        ("Email inválido", lambda: Cliente(1, "Juan", "juanexample.com", "1234567890")),
        ("Teléfono con letras", lambda: Cliente(1, "Juan", "juan@example.com", "12345abc90")),
        ("Teléfono muy corto", lambda: Cliente(1, "Juan", "juan@example.com", "123")),
        ("Completamente válido", lambda: Cliente(1, "Juan", "juan@example.com", "1234567890")),
    ]
    # Iterar sobre los casos de prueba y mostrar resultados
    for iterador, (descripcion, operacion) in enumerate(casos, start=1):
        try:
            operacion()
            print(f"{iterador}) {descripcion}: EXITOSO")
        except ErrorDominio as e:
            print(f"{iterador}) {descripcion}: {e}")


def test_servicio_sala():
    # Prueba de servicio de reserva de salas con casos de error
    print("\n=== TEST: Servicio de Reserva de Salas ===")

    salas = [
        {"id": 1, "nombre": "Sala A", "precio_hora": 50},
        {"id": 2, "nombre": "Sala B", "precio_hora": 80}
    ]
    servicio = ServicioReservaSalas(salas)

    casos = [
        ("ID sala None", lambda: servicio.calcular_costo(None, "2026-05-10", 2)),
        ("Fecha vacía", lambda: servicio.calcular_costo(1, "", 2)),
        ("Horas None", lambda: servicio.calcular_costo(1, "2026-05-10", None)),
        ("Horas negativas", lambda: servicio.calcular_costo(1, "2026-05-10", -5)),
        ("Sala no existe", lambda: servicio.calcular_costo(999, "2026-05-10", 2)),
        ("Reserva válida", lambda: servicio.calcular_costo(1, "2026-05-10", 2)),
        ("Sala ocupada", lambda: servicio.calcular_costo(1, "2026-05-10", 2)),
    ]

    for iterador, (descripcion, operacion) in enumerate(casos, start=1):
        try:
            resultado = operacion()
            print(f"{iterador}) {descripcion}: ${resultado}")
        except ErrorDominio as e:
            print(f"{iterador}) {descripcion}: {e}")


def test_servicio_equipo():
    # Prueba de servicio de alquiler de equipos con casos de error
    print("\n=== TEST: Servicio de Alquiler de Equipos ===")

    equipos = [
        {"id": 1, "nombre": "Laptop", "precio_dia": 30, "unidades": 3}
    ]
    servicio = ServicioAlquilerEquipos(equipos)

    casos = [
        ("ID equipo None", lambda: servicio.calcular_costo(None, 1, "2026-05-10", 2)),
        ("Cantidad None", lambda: servicio.calcular_costo(1, None, "2026-05-10", 2)),
        ("Fecha vacía", lambda: servicio.calcular_costo(1, 1, "", 2)),
        ("Días None", lambda: servicio.calcular_costo(1, 1, "2026-05-10", None)),
        ("Cantidad negativa", lambda: servicio.calcular_costo(1, -1, "2026-05-10", 2)),
        ("Equipo no existe", lambda: servicio.calcular_costo(999, 1, "2026-05-10", 2)),
        ("Alquiler válido", lambda: servicio.calcular_costo(1, 2, "2026-05-10", 2)),
        ("Exceso de unidades", lambda: servicio.calcular_costo(1, 5, "2026-05-10", 2)),
    ]

    for iterador, (descripcion, operacion) in enumerate(casos, start=1):
        try:
            resultado = operacion()
            print(f"{iterador}) {descripcion}: ${resultado}")
        except ErrorDominio as e:
            print(f"{iterador}) {descripcion}: {e}")


def test_servicio_asesoria():
    # Prueba de servicio de asesorías con casos de error
    print("\n=== TEST: Servicio de Asesorías ===")

    temas = [
        {"id": 1, "nombre": "Python", "precio_hora": 100},
        {"id": 2, "nombre": "JavaScript", "precio_hora": 80}
    ]
    servicio = ServicioAsesoria(temas)

    casos = [
        ("ID tema None", lambda: servicio.calcular_costo(None, 3)),
        ("Horas None", lambda: servicio.calcular_costo(1, None)),
        ("Horas negativas", lambda: servicio.calcular_costo(1, -2)),
        ("Tema no existe", lambda: servicio.calcular_costo(999, 3)),
        ("Asesoría válida", lambda: servicio.calcular_costo(1, 3)),
        ("Otra asesoría válida", lambda: servicio.calcular_costo(2, 2)),
    ]

    for iterador, (descripcion, operacion) in enumerate(casos, start=1):
        try:
            resultado = operacion()
            print(f"{iterador}) {descripcion}: ${resultado}")
        except ErrorDominio as e:
            print(f"{iterador}) {descripcion}: {e}")


def run_tests():
    # Datos de prueba para servicios
    print("--------------------------------------")
    print("|  PRUEBAS DE MANEJO DE EXCEPCIONES  |")
    print("--------------------------------------")

    try:
        test_cliente_validacion()
        test_servicio_sala()
        test_servicio_equipo()
        test_servicio_asesoria()

        print("\n--------------------------------------")
        print("Todas las pruebas completadas.")
        print("Revisa logs/app.log para ver los detalles de errors.")
        print("--------------------------------------")

        logger.info("Todas las pruebas de error completadas exitosamente")

    except Exception as e:
        logger.critical("Error ejecutando pruebas: %s", str(e), exc_info=True)
        print(f"\nERROR CRÍTICO en pruebas: {e}")


if __name__ == "__main__":
    run_tests()
