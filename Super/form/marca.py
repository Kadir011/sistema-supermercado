from django.forms import ModelForm
from Super.models import Marca 

class MarcaForm(ModelForm):
    class Meta:
        model = Marca 
        fields = '__all__' 


