import yfinance as yf
from .models import Ativo, Cotacao
from django.utils import timezone
from django.db import transaction, OperationalError
import time
from .notificador import verificar_limites_e_notificar

def buscar_cotacoes_e_salvar():
    """Busca as últimas cotações dos ativos cadastrados e salva apenas se for um minuto diferente da última cotação salva."""
    ativos = Ativo.objects.all()
    
    for ativo in ativos:
        try:
            # Verifica se é hora de buscar nova cotação com base na periodicidade do ativo
            ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora').first()
            agora = timezone.now()
            data_hora_atual = agora.replace(second=0, microsecond=0)
            
            if not ultima_cotacao or (agora - ultima_cotacao.data_hora).total_seconds() >= (ativo.periodicidade_minutos * 60):
                # Instancia o ticker no formato aceito pelo Yahoo Finance
                ticker = yf.Ticker(f"{ativo.codigo}.SA")
                
                # Busca cotações do dia no intervalo de 1 minuto
                cotacoes = ticker.history(period='1d', interval='1m')
                
                if not cotacoes.empty:
                    # Pega o último preço de fechamento registrado
                    preco_atual = cotacoes['Close'].iloc[-1]
                    
                    
                    max_retries = 3
                    retry_delay = 1 
                    
                    for attempt in range(max_retries):
                        try:
                            # Verifica se já existe cotação neste minuto e cria se não existir
                            cotacao_existente = None
                            with transaction.atomic():
 
                                cotacao_existente = Cotacao.objects.filter(
                                    ativo=ativo,
                                    data_hora=data_hora_atual
                                ).first()
                                
                                if not cotacao_existente:
                                    # Salva a nova cotação
                                    nova_cotacao = Cotacao.objects.create(
                                        ativo=ativo,
                                        preco=preco_atual,
                                        data_hora=data_hora_atual
                                    )
                                    print(f'Cotação salva para {ativo.codigo}: {preco_atual:.2f} ({data_hora_atual})')
                                    
                                    # Verifica se cruzou limites e envia notificação
                                    verificar_limites_e_notificar(ativo, preco_atual)
                                else:
                                    print(f'Ignorando cotação duplicada para {ativo.codigo} no minuto {data_hora_atual}')
                            
                            # Se chegou aqui, a operação foi bem-sucedida
                            break
                            
                        except OperationalError as e:
                            if "database is locked" in str(e) and attempt < max_retries - 1:
                                print(f"Banco de dados bloqueado. Tentativa {attempt+1}/{max_retries}. Aguardando {retry_delay}s...")
                                time.sleep(retry_delay)

                                retry_delay *= 2
                            else:
                                raise
        
        except Exception as e:
            print(f"Erro ao processar cotação para {ativo.codigo}: {str(e)}")