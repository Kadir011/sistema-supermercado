from django.forms import ModelForm
from Super.models import Venta

class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subtotal'].widget.attrs.update({
            'readonly': 'readonly',
        })
        self.fields['iva'].widget.attrs.update({
            'readonly': 'readonly',
        })
        self.fields['total'].widget.attrs.update({
            'readonly': 'readonly',
        })
    class Meta:
        model = Venta 
        fields = '__all__'

