import yfinance as yf
from .models import Ativo, Cotacao
from django.utils import timezone
from django.db import transaction, OperationalError
import time
from .notificador import verificar_limites_e_notificar

def buscar_cotacoes_e_salvar():

    ativos = Ativo.objects.all()
    
    for ativo in ativos:
        try:
            ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora').first()
            agora = timezone.now()
            data_hora_atual = agora.replace(second=0, microsecond=0)
            print(f"[DEBUG] Agora: {agora}, Última cotação: {ultima_cotacao.data_hora if ultima_cotacao else 'Nenhuma'}, Periodicidade: {ativo.periodicidade_minutos}min")
            
            if (
                not ultima_cotacao or 
                (data_hora_atual - ultima_cotacao.data_hora.replace(second=0, microsecond=0)).total_seconds() >= ativo.periodicidade_minutos * 60
            ):
                ticker = yf.Ticker(f"{ativo.codigo}.SA")
                cotacoes = ticker.history(period='1d', interval='1m')

                if not cotacoes.empty:
                    preco_atual = cotacoes['Close'].iloc[-1]

                    max_retries = 3
                    retry_delay = 1

                    for attempt in range(max_retries):
                        try:
                            with transaction.atomic():
                                cotacao_existente = Cotacao.objects.filter(
                                    ativo=ativo,
                                    data_hora=data_hora_atual
                                ).first()

                                if not cotacao_existente:
                                    nova_cotacao = Cotacao.objects.create(
                                        ativo=ativo,
                                        preco=preco_atual,
                                        data_hora=data_hora_atual
                                    )
                                    verificar_limites_e_notificar(ativo, preco_atual)
                                else:
                                    print(f'[INFO] Cotação já existe para {ativo.codigo} no minuto {data_hora_atual}')
                            break

                        except OperationalError as e:
                            if "database is locked" in str(e) and attempt < max_retries - 1:
                                print(f"[WARN] Banco de dados bloqueado. Tentativa {attempt+1}/{max_retries}. Aguardando {retry_delay}s...")
                                time.sleep(retry_delay)
                                retry_delay *= 2
                            else:
                                raise
                else:
                    print(f"[WARN] Nenhuma cotação encontrada para {ativo.codigo}")
            else:
                print(f"[INFO] Cotação registrada recentemente para {ativo.codigo}, aguardando próxima janela...")
        
        except Exception as e:
            print(f"[ERROR] Erro ao processar cotação para {ativo.codigo}: {str(e)}")
