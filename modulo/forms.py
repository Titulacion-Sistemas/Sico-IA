from django import forms
from modulo.models import modulo

__author__ = 'Jhonsson'

class busquedas(forms.Form):

    def __init__(self, *args, **kwargs):
        super(busquedas, self).__init__(*args, **kwargs)


    dato = forms.CharField(
        required=True, initial='', label='Dato a Buscar',
        widget=forms.TextInput(
            attrs={
                'data-ng-model': 'dato'
            }
        ),
    )

    criterio = forms.ModelChoiceField(
        modulo.objects.filter(submodulo=modulo.objects.get(nombre='busquedas')),
        label='Criterio', empty_label=None,
        widget=forms.Select(
            attrs={
                'data-ng-model': 'criterio'
            }
        ),
        required=True
    )
