# 💰 Investidor B3 - Desafio de Desenvolvimento

Este projeto foi desenvolvido com o objetivo de auxiliar investidores a tomarem decisões de compra e venda de ativos da B3 com base em cotações atualizadas e regras de túnel de preço.

## 📌 Descrição

A aplicação permite:

- Cadastrar ativos da B3 que serão monitorados;
- Definir parâmetros de túnel de preço (limite inferior/superior ou percentual);
- Escolher a periodicidade (em minutos) para verificação de cotação por ativo;
- Armazenar as cotações ao longo do tempo;
- Notificar o investidor via e-mail quando a cotação cruzar os limites definidos, sugerindo **compra** ou **venda**.

🔗 **URL principal:** `http://localhost:8000/ativos/`  
Essa é a página inicial da aplicação, onde você pode cadastrar novos ativos e configurar seus parâmetros de monitoramento.

📌 **Observação sobre o desenvolvimento:**  
A maior parte dos commits foi realizada na branch `developer`, seguindo boas práticas de versionamento. Após a conclusão das principais funcionalidades, o conteúdo foi integrado à branch `main`.

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Django 5.2**
- **SQLite** (para fins de simplicidade/testes)
- **APScheduler** (agendamento das checagens de cotação)
- **yfinance** (para obter cotações dos ativos da B3)
- **Django REST Framework**
- **Console Email Backend** (para testes de envio de e-mail)

## 💻 Exemplos de Cadastro de Ativo

### Exemplo 1: Ativo PETR4 com túnel fixo

- **Nome**: Petrobras PN  
- **Código**: PETR4.SA  
- **Limite Inferior**: 28.00  
- **Limite Superior**: 34.00  
- **Periodicidade (minutos)**: 15  
