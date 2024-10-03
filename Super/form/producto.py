from django.forms import ModelForm
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







