from django.urls import path
from .views import AtivoCreateView, AtivoUpdateView, AtivoListView, CotacaoListView, CotacoesAtivoView

urlpatterns = [
    # Rota para listar todos os ativos
    path('ativos/', AtivoListView.as_view(), name='listar_ativos'),
    # Rota para criar um novo ativo
    path('ativos/novo/', AtivoCreateView.as_view(), name='criar_ativo'),
    # Rota para editar um ativo existente, com base no ID (pk) do ativo
    path('ativos/editar/<int:pk>/', AtivoUpdateView.as_view(), name='editar_ativo'),
    # Rota para visualizar as cotações associadas a um ativo específico, usando seu ID
    path('ativos/cotacoes/<int:pk>/', CotacoesAtivoView.as_view(), name='visualizar_cotacoes'),
    
    # API REST para listar todas as cotações
    path('api/cotacoes/', CotacaoListView.as_view(), name='listar_cotacoes'),
]