#importacion del paquete que se encrga de la communicacion con la base de datos, models es el modulo que contiene las clasespara construir tablas(tipos de campo(texto,fecha ,etc) y logica orm)
from django.db import models

#biblioteca estándar (aplicación instalada) de Django que gestiona la seguridad y autenticación,User: Es una Clase Modelo ya fabricada que representa a un usuario registrado
from django.contrib.auth.models import User

class Reporte(models.Model):
    ESTADOS =[
        ('PENDIENTE', 'Pendiente'), 
        ('PROCESANDO', 'Procesando'),
        ('COMPLETADO', 'Completado'),
        ('ERROR', 'Error'),
    ]

    #Django verifica que el ID que guardes aquí exista previamente en la tabla User
    # si usuario que no existe, la base de datos lanzará un error de integridad
    usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    # Texto corto con límite de caracteres
    nombre_reporte= models.CharField(max_length=100)
    # Almacena la ruta del archivo en el servidor Docker,PostgreSQL no guarda el archivo, guarda un texto con la ruta
    #El archivo físico se guarda en la carpeta /app/media/informes/ dentro del contenedor Docker, la cual está vinculada 
    # a tu PC mediante el volumen que definimos en el YAML
    archivo= models.FileField(upload_to='informes/', null=True)
    # Campo con opciones cerradas y valor por defecto
    estado= models.CharField(max_length=20, choices=ESTADOS,default='PENDIENTE')
    fecha_creacion= models.DateTimeField(auto_now_add=True)

    # Cómo se identifica el objeto en el panel Admin o consola
    def __str__(self):
        return f"{self.nombre_reporte} - {self.estado}"


class UserProfile(models.Model):
    # el 'related_name' define como se eaccede desde el ususario: usuario.profile
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile' 
    )
    
  
    primer_ingreso = models.BooleanField(default=True) 

    def __str__(self):
        return f"Perfil de {self.user.username}"