# Sistema Integral de Gestion de Clientes, Servicios y Reservas

Proyecto en Python orientado a objetos para gestionar clientes, servicios y reservas.
Incluye validaciones, manejo de excepciones personalizadas y registro de eventos en logs.

## Descripcion

El sistema simula operaciones comunes de negocio:
- Registro y validacion de clientes
- Calculo de costos de servicios
- Creacion y control de reservas
- Manejo de errores esperados y no esperados

## Estructura del proyecto

- main.py: ejecucion principal del sistema
- test.py: pruebas enfocadas en excepciones
- modelos/: entidades del dominio (ejemplo: cliente)
- servicios/: logica de servicios (salas, equipos, asesorias)
- reservas/: logica de reservas
- excepciones/: clases de excepciones personalizadas
- utils/logger.py: configuracion de logging
- logs/: salida de logs del sistema

## Requisitos

- Python 3.7 o superior
- Sin dependencias externas (solo libreria estandar)

## Ejecucion

Para correr la simulacion principal:

"python main.py"

Para ejecutar pruebas de errores:

"python test_errores.py"


## Validaciones y errores manejados

Entre los casos cubiertos se incluyen:
- Parametros faltantes (None)
- Campos vacios
- Formatos invalidos (correo, telefono)
- Valores inconsistentes (horas negativas, IDs inexistentes)
- Recursos no disponibles

## Logs

Los eventos del sistema se registran en:

"logs/app.log"

## Objetivo del proyecto

Servir como practica de:
- Programacion orientada a objetos
- Manejo robusto de excepciones
- Buenas practicas de validacion y trazabilidad con logs
