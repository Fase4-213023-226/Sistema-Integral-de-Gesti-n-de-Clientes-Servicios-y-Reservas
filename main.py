from servicios.reserva_sala import ServicioReservaSalas
from servicios.alquiler_equipo import ServicioAlquilerEquipos
from servicios.asesoria import ServicioAsesoria
from modelos.cliente import Cliente
from utils.logger import logger
    
def simular_operaciones():
    print("========= INICIO DE SIMULACION DE OPERACIONES =========\n")

    # Datos base utilizados para las operaciones de prueba
    salas = [
        {"id": 1, "nombre": "Sala A", "precio_hora": 50},
        {"id": 2, "nombre": "Sala B", "precio_hora": 80}
    ]

    equipos = [
        {"id": 1, "nombre": "Laptop", "precio_dia": 30, "unidades": 5}
    ]

    temas = [
        {"id": 1, "nombre": "Python", "precio_hora": 100}
    ]

    # Instancia de servicios
    servicio_salas = ServicioReservaSalas(salas)
    servicio_equipos = ServicioAlquilerEquipos(equipos)
    servicio_asesoria = ServicioAsesoria(temas)

    operaciones = [

        # 1 válido
        lambda: Cliente(1, "Juan", "juan@gmail.com", "1234567890"),

        # 2 inválido (Error: nombre vacío)
        lambda: Cliente(2, "", "correo", "abc"),

        # 3 válido
        lambda: servicio_salas.calcular_costo(1, "2026-05-10", 2),

        # 4 inválido (Error: sala ocupada)
        lambda: servicio_salas.calcular_costo(1, "2026-05-10", 2),

        # 5 inválido (Error: sala no existe)
        lambda: servicio_salas.calcular_costo(99, "2026-05-10", 2),

        # 6 válido
        lambda: servicio_equipos.calcular_costo(1, 2, "2026-05-10", 2),

        # 7 inválido (Error: exceso de unidades)
        lambda: servicio_equipos.calcular_costo(1, 10, "2026-05-10", 2),

        # 8 inválido (Error: equipo no existe)
        lambda: servicio_equipos.calcular_costo(99, 1, "2026-05-10", 1),

        # 9 válido
        lambda: servicio_asesoria.calcular_costo(1, 3),

        # 10 inválido (Error: tema no existe)
        lambda: servicio_asesoria.calcular_costo(99, 2),
    ]

    # Loop para ejecutar las operaciones y mostrar resultados
    for i, operacion in enumerate(operaciones, 1):
        try:
            resultado = operacion()
            logger.info(f"Operacion {i} fue exitosa: {resultado}") # Registro de éxito en el log
            print(f"Operacion {i} fue exitosa: {resultado}") # Impresión del resultado de la operación
        except Exception as e:
            logger.error(f"Operacion {i} ha fallado: {e}") # Registro del error en el log
            print(f"Operacion {i} ha fallado: {e}") # Impresión del error ocurrido durante la operación

    print("\n========= FIN DE SIMULACION DE OPERACIONES =========")


if __name__ == "__main__":
    simular_operaciones()