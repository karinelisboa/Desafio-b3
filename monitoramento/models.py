from django.db import models


# Tabela da empresa/ação que está sendo monitorada
class Ativo(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    
    # Cria uma tupla de opções
    TIPO_TUNEL_CHOICES = (
        ('estatico', 'Estático'),
        ('dinamico', 'Dinâmico')
    )
    tipo_tunel = models.CharField(max_length=10, choices=TIPO_TUNEL_CHOICES) # Escolher entre os tuneis

    # Se o túnel for estático (limites manualmente definidos)
    limite_inferior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    limite_superior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Se o túnel for dinâmico,  percentual em cima do último preço salvo
    percentual_tunel = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # De quanto em quanto tempo buscar novas cotações
    periodicidade_minutos = models.PositiveIntegerField()

    def __str__(self):
        return self.codigo

# Tabela do preço do ativo naquele momento
class Cotacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name='cotacoes')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ativo.codigo} - {self.preco}'
