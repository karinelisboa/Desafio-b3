from rest_framework import serializers
from .models import Cotacao

# Serializador para o modelo Cotacao, convertendo os dados para JSON
class CotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = ['ativo', 'preco', 'data_hora']
