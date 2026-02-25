import os
from celery import Celery

# sincronizacion , se le dice  a Python donde esta el manual de reglas de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONFIG_GENERAL.settings')

# instanciacion: se crea al  Celery con el nombre del proyecto
app = Celery('PROYECTO-REPORTES')

# unificacion se le dice  a Celery que lea los ajustes que empiecen con 'CELERY' en settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# mapeo, es el radar que busca automaticamente los archivos tasks.py
app.autodiscover_tasks()