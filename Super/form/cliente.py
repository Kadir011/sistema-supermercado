from django.forms import ModelForm
from Super.models import Cliente 

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 
                  'nombre',
                  'apellido',
                  'cedula',
                  'telefono',
                  'fecha_nacimiento',
                  'genero']
        
