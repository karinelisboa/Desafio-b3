import yfinance as yf
from .models import Ativo, Cotacao
from django.utils import timezone
from .notificador import verificar_limites_e_notificar

def buscar_cotacoes_e_salvar():
    """Busca as últimas cotações dos ativos cadastrados e salva apenas se for um minuto diferente da última cotação salva."""
    
    ativos = Ativo.objects.all()  
    
    for ativo in ativos:
        # Verifica se é hora de buscar nova cotação com base na periodicidade do ativo
        ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora').first()
        agora = timezone.now()
        

        if not ultima_cotacao or (agora - ultima_cotacao.data_hora).total_seconds() >= (ativo.periodicidade_minutos * 60):
            # Instancia o ticker no formato aceito pelo Yahoo Finance
            ticker = yf.Ticker(f"{ativo.codigo}.SA")
            # Busca cotações do dia no intervalo de 1 minuto
            cotacoes = ticker.history(period='1d', interval='1m') 

            if not cotacoes.empty:
                # Pega o último preço de fechamento registrado
                preco_atual = cotacoes['Close'].iloc[-1]

                # Salva a nova cotação
                nova_cotacao = Cotacao.objects.create(
                    ativo=ativo,
                    preco=preco_atual
                )
                print(f'Cotação salva para {ativo.codigo}: {preco_atual:.2f}')
                
                # Verifica se cruzou limites e envia notificação se necessário
                verificar_limites_e_notificar(ativo, preco_atual)