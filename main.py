from servicios.reserva_sala import ServicioReservaSalas
from servicios.alquiler_equipo import ServicioAlquilerEquipos
from servicios.asesoria import ServicioAsesoria
from modelos.cliente import Cliente
from excepciones.excepciones import ErrorDominio
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
    try:
        servicio_salas = ServicioReservaSalas(salas)
        servicio_equipos = ServicioAlquilerEquipos(equipos)
        servicio_asesoria = ServicioAsesoria(temas)
        logger.info("Servicios inicializados exitosamente")
    except Exception as e:
        logger.critical("No se pudieron inicializar los servicios: %s", str(e), exc_info=True)
        print(f"ERROR CRÍTICO: No se pudieron inicializar los servicios")
        return

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
    errores_totales = 0
    operaciones_exitosas = 0

    for i, operacion in enumerate(operaciones, 1):
        try:
            resultado = operacion()
        except ErrorDominio as e:
            # Excepciones del dominio conocidas
            logger.warning("Operacion %d - Error esperado del dominio: %s", i, str(e), exc_info=True)
            print(f"Operacion {i} - ERROR (esperado): {e}") # Se muestra el error esperado para cada operación que se sabe que fallará
            errores_totales += 1 # Suma al contador de errores
            continue
        except Exception as e:
            # Excepciones inesperadas
            logger.error("Operacion %d - Error inesperado: %s", i, str(e), exc_info=True)
            print(f"Operacion {i} - ERROR (inesperado): {e}") # Se muestra el error inesperado para cada operación que no se esperaba que fallara
            errores_totales += 1 # Suma al contador de errores
            continue
        else:
            # Operación exitosa
            logger.info("Operacion %d exitosa: %s", i, str(resultado))
            print(f"Operacion {i} exitosa: {resultado}") # Se muestra el resultado exitoso para cada operación que se esperaba que tuviera éxito
            operaciones_exitosas += 1 # Suma al contador de operaciones exitosas
        finally:
            # Siempre se ejecuta
            pass

    # Print del resumen final de las operaciones
    print(f"\n========= RESUMEN DE OPERACIONES =========")
    print(f"Total operaciones: {len(operaciones)}")
    print(f"Exitosas: {operaciones_exitosas}")
    print(f"Errores: {errores_totales}")
    print(f"========= FIN DE SIMULACION DE OPERACIONES =========\n")

    logger.info("Simulacion completada. Exitosas: %d, Errores: %d", operaciones_exitosas, errores_totales) # Se registra el resumen de la simulación en los logs

    return operaciones_exitosas, errores_totales # Se devuelven los contadores para usos futuros


def main(): # Función principal que inicia la aplicación
    try:
        logger.info("Iniciando aplicación")
        print("Iniciando aplicación...\n")

        simular_operaciones()

    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
        print("\nAplicación interrumpida por el usuario.")
    except Exception as e:
        logger.critical("Error crítico desconocido en main: %s", str(e), exc_info=True)
        print(f"ERROR CRÍTICO: {e}")
        print("La aplicación continuará activa para que puedan revisarse los logs.")
    finally:
        logger.info("Finalizando aplicación")
        print("\nAplicación finalizada. Consulte los logs para más detalles.")


if __name__ == "__main__":
    main()