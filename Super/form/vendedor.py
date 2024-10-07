from django.forms import ModelForm
from django.core.exceptions import ValidationError
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

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit() or len(cedula) != 10:  # Validación de cédula
            raise ValidationError("La cédula debe tener 10 dígitos.")
        return cedula

