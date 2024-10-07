from django.forms import ModelForm
from django.core.exceptions import ValidationError
from Super.models import Producto

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_expiracion'].widget.attrs.update({
            'readonly':'readonly'
        })

    class Meta:
        model = Producto 
        fields = ['imagen',
                  'codigo',
                  'marca',
                  'categoria',
                  'nombre',
                  'descripcion',
                  'precio',
                  'fecha_elaboracion',
                  'fecha_expiracion',
                  'estado']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise ValidationError("El precio debe ser un valor positivo.")
        return precio


