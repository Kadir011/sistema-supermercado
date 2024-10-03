from django.forms import ModelForm
from Super.models import Vendedor

class VendedorForm(ModelForm):
    class Meta:
        model = Vendedor
        fields = ['codigo', 
                  'nombre',
                  'apellido',
                  'cedula',
                  'telefono',
                  'fecha_nacimiento',
                  'genero'] 
        
