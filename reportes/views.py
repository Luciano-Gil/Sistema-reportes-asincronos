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

# --- Herramientas Estándar de Python ---
import random  # Para elegir caracteres al azar en la clave temporal
import string  # Provee los listados de letras y números (ascii_letters, digits)

# --- Atajos y Mensajería de Django ---
from django.shortcuts import render, redirect  # Para dibujar el HTML y saltar entre páginas (login, dashboard)
from django.contrib import messages  # Para mostrar los carteles de "Contraseña actualizada" o "Error"

# --- Gestión de Usuarios y Seguridad ---
from django.contrib.auth.models import User  # El modelo que representa a los empleados en PostgreSQL
from django.contrib.auth.forms import PasswordChangeForm  # El formulario oficial de Django para validar claves nuevas
from django.contrib.auth import update_session_auth_hash  # Evita que el sistema te saque (logout) al cambiar la clave

# --- Infraestructura de Correo Electrónico ---
from django.core.mail import EmailMultiAlternatives  # Permite enviar correos que tengan texto y diseño HTML a la vez
from django.template.loader import render_to_string  # Toma tu archivo .html de mail y lo convierte en texto para enviar
from django.conf import settings  # Para leer tu correo oficial (DEFAULT_FROM_EMAIL) desde el archivo settings.py

# --- Base de Datos y Transacciones ---
from django.db import transaction  # El "seguro" que cancela el cambio de clave si el mail no llega a enviarse

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


############################################################################################################
# Cambio-contraseña, recuperar contraseña, mail


def generar_contraseña_temporal(longitud=8):
    """funcion que genera  contraseña alfanumerica """
    caracteres = ascii_letters + digits
    nueva_pass = "".join(random.choice(caracteres) for i in range(longitud))
    return nueva_pass


def cambiar_contraseña(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # accede y desactiva la bandera en el Perfil
            # si el usuario fue forzado a cambiar la contraseña (primer_ingreso esta en el profile)
            if user.profile.primer_ingreso:
                
                #desactiva la bandera
                user.profile.primer_ingreso = False
                
                # guardar el objeto profile (no el objeto user)
                user.profile.save() 
            
            # mantiene al usuario logueado despue que cambio la
            messages.success(request, 'Contraseña  actualizada')
            
            return redirect('dashboard')
            
    else:
       #inicializa el formulario para el usuario logueado
        form = PasswordChangeForm(request.user)

    contexto = {'form': form, 'titulo': 'Cambiar Contraseña'}
    return render(request, 'usuario/cambiar_contraseña.html', contexto)


def recuperar_contraseña(request):
    """ funcion que gestiona la solicitude de recuperacion , genera una clave
    activando el userprofile y manda el mail
    
    """
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            usuario = User.objects.get(email=email)
            
            with transaction.atomic():
                #genera la contraseña y actualiza
                nueva_pass = generar_contraseña_temporal(longitud=8)
                usuario.set_password(nueva_pass) 
                usuario.save() 
                
                # forza el cambiio al activar la bandera
                usuario.profile.primer_ingreso = True
                usuario.profile.save() 
                
                # envio de correo
                contexto_email = {
                    'usuario_nombre': usuario.username,
                    'nueva_pass': nueva_pass,
                }
                
              
                html_content = render_to_string('emails/correo.html', contexto_email)
                
                email_obj = EmailMultiAlternatives(
                    subject="Recuperación de contraseña y acceso Temporal",
                    body=f"Nueva contraseña temporal : {nueva_pass}. Debes cambiarla al ingresar",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                email_obj.attach_alternative(html_content, "text/html")
                email_obj.send() 
            
            messages.success(request, "Se ha enviado una nueva contraseña temporal a tu correo")
            
        except User.DoesNotExist:
            messages.error(request, "El correo ingresado no esta asociado a una cuenta")
        
        return redirect('login') 

    return render(request, 'usuario/recuperar_contraseña.html')

