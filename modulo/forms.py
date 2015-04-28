# coding=utf-8
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
                'class': "form-control input-lg may",
                'name': "dato",
                'data-ng-model': 'dato',
                'autofocus': 'true',
                'tabindex': '0',
                'show-focus': "true"
            }
        ),
    )

    criterio = forms.ModelChoiceField(
        modulo.objects.filter(submodulo=modulo.objects.get(nombre='busquedas')),
        label='Criterio', empty_label=None,
        widget=forms.Select(
            attrs={
                'class': "form-control input-lg may",
                'name': "criterio",
                'data-ng-model': 'criterio',
                'data-ng-change': 'seleccion(criterio)'
            }
        ),
        required=True
    )

    def clean(self):
        cleaned_data = super(busquedas, self).clean()
        tb = cleaned_data.get("tipoBusq")
        c = cleaned_data.get("consulta")

        if c and tb:
            # Only do something if both fields are valid so far.
            if tb == '1':
                if not c.isdigit() or len(c) > 8:
                    raise forms.ValidationError("Error, Cuenta ingresada no válida.")

            if tb == '2':
                if not c.isdigit() or len(c) >= 11:
                    raise forms.ValidationError("Error, Número de medidor ingresado no válido.")

            if tb == '3':
                if c.isdigit():
                    raise forms.ValidationError("Error, Nombre de ciente no valido.")

            if tb == '4':
                sp = c.split('.')
                if len(sp) != 5 \
                    or (not sp[0].isdigit()) \
                    or (not sp[1].isdigit()) \
                    or (not sp[2].isdigit()) \
                    or (not sp[3].isdigit()) \
                    or (not sp[4].isdigit()):

                    raise forms.ValidationError("Error, Geocódigo incorrecto.")

                elif len(sp[0]) > 2 or len(sp[0]) < 1 \
                    or len(sp[1]) > 2 or len(sp[1]) < 1 \
                    or len(sp[2]) > 2 or len(sp[2]) < 1 \
                    or len(sp[3]) > 3 or len(sp[3]) < 1 \
                    or len(sp[4]) > 7 or len(sp[4]) < 1:

                    raise forms.ValidationError("Error, Geocódigo no válido.")

                # Always return the full collection of cleaned data.
        return cleaned_data
