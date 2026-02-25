from django.urls import path
from . import views  # importa las vistas 

urlpatterns = [

    path('', views.inicio_reporte, name='inicio'),
]