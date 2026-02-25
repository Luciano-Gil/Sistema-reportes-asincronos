#  función render para poder mostrar el archivo HTML(template)
from django.shortcuts import render

#  tarea  creada en tasks.py para poder darle ordenes al Worker
from .tasks import reporte_prueba


def inicio_reporte(request):
    
    # .delay() instruccion que  envia la tarea al buzon (Redis) de forma asíncrona
    # Django no espera a que la tarea termine, la deja en el buzon y sigue a la siguiente linea
    reporte_prueba.delay() 
    
    # se envia  una respuesta inmediata al navegador cargando el template index.html
    # en el navegador se ve la pagina cargada al instante, mientras el Worker trabaja en segundo plano
    return render(request, 'reportes/index.html')