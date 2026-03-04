from django.urls import path
from . import views  # importa las vistas 
from django.contrib.auth import views as auth_views #: importa todas las vistas de seguridad de Django (Login, Logout, cambio de contraseña)

urlpatterns = [
    path('', views.home, name='home'),
    # Ruta de Login(usa la lógica de Django y diseño visual)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Ruta de Logout(para cerrar la sesión de forma segura)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),


    #contraseñas
    path('usuarios/cambiar_contraseña/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('usuarios/recuperar_contraseña/', views.recuperar_contrasena, name='recuperar_contrasena'),
    #correo


]