from django.forms import ModelForm
from django.core.exceptions import ValidationError
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
        fields = ['cliente', 'vendedor', 'fecha', 'subtotal', 'iva', 'dscto', 'total']

    def clean_dscto(self):
        dscto = self.cleaned_data.get('dscto')
        if dscto < 0 or dscto > 100:
            raise ValidationError("El descuento debe estar entre 0 y 100.")
        return dscto



