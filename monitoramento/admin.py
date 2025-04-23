from django.contrib import admin
from .models import Ativo, Cotacao

# Registro do modelo Ativo no painel de administração do Django
@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo_tunel', 'limite_inferior', 'limite_superior', 'percentual_tunel', 'periodicidade_minutos')
    search_fields = ('codigo', 'nome')

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('ativo', 'preco', 'data_hora')
    list_filter = ('ativo',)
    search_fields = ('ativo__codigo',)
