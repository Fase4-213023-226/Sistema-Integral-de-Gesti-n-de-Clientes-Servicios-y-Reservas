import os
import logging

# Crear la carpeta logs si no existe
os.makedirs('logs', exist_ok=True) # Crear carpeta logs si no existe

logging.basicConfig(
    filename='logs/eventos.log', # Archivo de log donde se guardarán los eventos
    level=logging.DEBUG, # Nivel Debug para capturar todo
    format='%(asctime)s - %(levelname)s - %(message)s' # Formato del mensaje de log
)

logger = logging.getLogger() # Instancia del Logger