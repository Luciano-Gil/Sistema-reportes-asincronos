from django.contrib import admin
from .models import Reporte # Importamos tu modelo desde el archivo vecino

admin.site.register(Reporte) # Registramos el modelo en el sitio de administración