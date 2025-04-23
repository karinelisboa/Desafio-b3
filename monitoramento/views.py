from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cotacao, Ativo
from .serializers import CotacaoSerializer
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import AtivoForm

# Classe para listar todas as cotações, utilizando a API do Django Rest Framework
class CotacaoListView(APIView):
    def get(self, request):
        cotacoes = Cotacao.objects.all()
        serializer = CotacaoSerializer(cotacoes, many=True)
        return Response(serializer.data)

# Classe para listar todos os ativos, utilizando uma ListView do Django
class AtivoListView(ListView):
    model = Ativo
    template_name = 'monitoramento/ativo_list.html'

# Classe para criar um novo ativo
class AtivoCreateView(CreateView):
    model = Ativo
    form_class = AtivoForm
    template_name = 'monitoramento/ativo_form.html'
    success_url = reverse_lazy('listar_ativos')

# Classe para atualizar um ativo existente
class AtivoUpdateView(UpdateView):
    model = Ativo
    form_class = AtivoForm
    template_name = 'monitoramento/ativo_form.html'
    success_url = reverse_lazy('listar_ativos')

# Classe para visualizar as cotações de um ativo específico
class CotacoesAtivoView(DetailView):
    model = Ativo
    template_name = 'monitoramento/cotacoes_view.html'
    context_object_name = 'ativo'
    
    # Método para adicionar as cotações do ativo ao contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cotacoes'] = self.object.cotacoes.all().order_by('-data_hora')[:100]
        return context