from django.core.mail import send_mail
from django.conf import settings
from .models import Ativo, Cotacao
from decimal import Decimal

# # Função para enviar o email de notificação para o investidor
def enviar_email_notificacao(ativo, preco_atual, tipo_notificacao):

    assunto = f"Alerta de {tipo_notificacao.upper()} - {ativo.codigo}"
    
    # Verifica o tipo de notificação (compra ou venda) e cria a mensagem do email correspondente
    if tipo_notificacao == 'compra':
        mensagem = f"""
        Olá Investidor,
        
        Uma oportunidade de COMPRA foi identificada!
        
        O ativo {ativo.codigo} ({ativo.nome}) atingiu o preço de R$ {preco_atual:.2f},
        cruzando seu limite inferior de túnel de preço.
        
        Limite inferior: R$ {ativo.limite_inferior if ativo.tipo_tunel == 'estatico' else 'Dinâmico'}
        
        Atenciosamente,
        Sistema de Monitoramento B3
        """
    else:  # venda
        mensagem = f"""
        Olá Investidor,
        
        Uma oportunidade de VENDA foi identificada!
        
        O ativo {ativo.codigo} ({ativo.nome}) atingiu o preço de R$ {preco_atual:.2f},
        cruzando seu limite superior de túnel de preço.
        
        Limite superior: R$ {ativo.limite_superior if ativo.tipo_tunel == 'estatico' else 'Dinâmico'}
        
        Atenciosamente,
        Sistema de Monitoramento B3
        """
    
    # Definir o email do investidor (aqui é um exemplo, poderia vir de um banco de dados ou configuração)
    email_destino = 'investidor@exemplo.com'
    
    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        [email_destino],
        fail_silently=False,
    )
    
    print(f"Email de {tipo_notificacao} enviado para {ativo.codigo} - Preço: R$ {preco_atual:.2f}")

def verificar_limites_e_notificar(ativo, preco_atual):

    preco_decimal = Decimal(str(preco_atual))
    ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora').first()
    
    if not ultima_cotacao or ultima_cotacao.preco == preco_decimal:
        return False
    

    preco_anterior = ultima_cotacao.preco
    
    # Definir limites com base no tipo de túnel
    if ativo.tipo_tunel == 'estatico':
        limite_inferior = ativo.limite_inferior
        limite_superior = ativo.limite_superior
    else:  # túnel dinâmico
        # Calcula limites dinâmicos baseados na última cotação
        percentual = ativo.percentual_tunel / Decimal('100')
        limite_inferior = preco_anterior * (Decimal('1') - percentual)
        limite_superior = preco_anterior * (Decimal('1') + percentual)
    
    # Verificar cruzamento do limite inferior (sinal de compra)
    if preco_decimal <= limite_inferior:
        enviar_email_notificacao(ativo, preco_decimal, 'compra')
        return True
        
    # Verificar cruzamento do limite superior (sinal de venda)
    if preco_decimal >= limite_superior:
        enviar_email_notificacao(ativo, preco_decimal, 'venda')
        return True
        
    return False