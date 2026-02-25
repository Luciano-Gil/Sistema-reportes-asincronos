from celery import shared_task
import time

@shared_task
def reporte_prueba():
    time.sleep(5) # simula que el reporte tarda 5 segundos 
    return "Reporte  generado con exito"