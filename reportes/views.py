#  función render para poder mostrar el archivo HTML(template)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#Importa un formulario pre-construido por Django que incluye los campos necesarios 
# para crear un usuario (Nombre de usuario y contraseña doble) y maneja la seguridad 
# de las claves en la base de datos PostgreSQL.
from django.contrib.auth.forms import UserCreationForm

#Es una función que "espera" a que las URLs estén cargadas antes de redirigir. Se 
# usa en clases porque, al momento de leer el código, Django aún no conoce todas las rutas, y 
# reverse_lazy evita errores de carga.
from django.urls import reverse_lazy

#Importa las vistas genéricas de Django. Estas son plantillas de código que ya saben cómo 
# hacer tareas comunes, como mostrar una lista, editar un objeto o, en este caso, crear un nuevo registro.
from django.views import generic

@login_required # decorador que protege la vista,  si no se esta  logueado, manda al login
def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):

    return render(request, 'home.html')

class SignUpView(generic.CreateView):
    """Esta clase hereda de generic.CreateView, lo que significa que ya hereda
      automáticamente toda la lógica para recibir datos de un formulario y guardarlos en la base de datos.
    """

    #Le dice a la vista: "Usa este formulario específico para pedir los datos al empleado".
    form_class = UserCreationForm

    #Define que, si el registro en PostgreSQL es exitoso, el sistema debe enviar 
    # al usuario automáticamente a la página de inicio de sesión.
    success_url = reverse_lazy('login')

    #Indica cuál es el archivo HTML que debe dibujar este formulario en la pantalla del navegador.
    template_name = '' \
    'signup.html'