from django import forms
from .models import Ativo

class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = [
            'nome',
            'codigo',
            'tipo_tunel',
            'limite_inferior',
            'limite_superior',
            'percentual_tunel',
            'periodicidade_minutos',
        ]
        widgets = {
            'tipo_tunel': forms.RadioSelect,
        }

    # Validação personalizada do formulário
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_tunel')
        limite_inf = cleaned_data.get('limite_inferior')
        limite_sup = cleaned_data.get('limite_superior')
        percentual = cleaned_data.get('percentual_tunel')

        if tipo == 'estatico' and (limite_inf is None or limite_sup is None):
            raise forms.ValidationError("Preencha os limites inferior e superior para o túnel estático.")
        elif tipo == 'dinamico' and percentual is None:
            raise forms.ValidationError("Preencha o percentual do túnel dinâmico.")
        return cleaned_data
