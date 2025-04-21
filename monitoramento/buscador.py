import yfinance as yf
from .models import Ativo, Cotacao
from django.utils import timezone

def buscar_cotacoes_e_salvar():
    """Busca as últimas cotações dos ativos cadastrados e salva apenas se for um minuto diferente da última cotação salva."""
    
    # Recupera todos os ativos cadastrados no banco
    ativos = Ativo.objects.all()  
    
    for ativo in ativos:
        # Instancia o ticker no formato aceito pelo Yahoo Finance (ex: PETR4.SA)
        ticker = yf.Ticker(f"{ativo.codigo}.SA")
        # Busca cotações do dia no intervalo de 1 minuto
        cotacoes = ticker.history(period='1d', interval='1m') 

        if not cotacoes.empty:
            # Pega o último preço de fechamento registrado
            preco_atual = cotacoes['Close'].iloc[-1]

            ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora').first()
            agora = timezone.now()

            # Salva apenas se ainda não existir uma cotação salva para o minuto atual
            if not ultima_cotacao or ultima_cotacao.data_hora.minute != agora.minute:
                Cotacao.objects.create(
                    ativo=ativo,
                    preco=preco_atual
                )
                print(f'Cotação salva para {ativo.codigo}: {preco_atual:.2f}')
