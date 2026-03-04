from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile  # Importamos tu modelo de perfil

class RegistroEmpleadoForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text="Requerido para la recuperación de clave"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        # 1. Guardamos el usuario pero sin persistir aún en PostgreSQL
        user = super().save(commit=False)
        
        # 2. Garantizamos que sea un usuario común (no superusuario ni staff)
        user.is_superuser = False
        user.is_staff = False
        
        if commit:
            user.save()  # Guardamos el usuario físicamente
            
            # 3. Creamos el perfil con la bandera de primer_ingreso
            # No se pone en el form porque el empleado no debe poder "desmarcarla" él mismo.
            UserProfile.objects.get_or_create(user=user, primer_ingreso=True)
            
        return user