from django.contrib import admin
from .models import Ativo, Cotacao

@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo_tunel', 'limite_inferior', 'limite_superior', 'percentual_tunel', 'periodicidade_minutos')
    search_fields = ('codigo', 'nome')

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('ativo', 'preco', 'data_hora')
    list_filter = ('ativo',)
    search_fields = ('ativo__codigo',)
