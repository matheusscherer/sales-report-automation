"""
notion_integration.py

Envia o relatório consolidado de vendas para uma página do Notion,
usando a API oficial (https://developers.notion.com/).

O token da integração e o ID da página/database são lidos de variáveis
de ambiente (via arquivo .env), nunca ficam expostos no código.
"""

import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis do arquivo .env

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"  # versão da API do Notion


def _validar_configuracao() -> None:
    """Garante que as variáveis de ambiente necessárias estão definidas."""
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        raise EnvironmentError(
            "As variáveis NOTION_TOKEN e NOTION_DATABASE_ID precisam estar "
            "definidas no arquivo .env. Veja o README para instruções."
        )


def montar_payload(metricas: dict, data_referencia: str = None) -> dict:
    """
    Monta o corpo da requisição para criar uma nova página (registro) no
    database do Notion, com as métricas do relatório do dia.
    """
    data_referencia = data_referencia or datetime.now().strftime("%Y-%m-%d")

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Nome": {
                "title": [
                    {"text": {"content": f"Relatório de Vendas - {data_referencia}"}}
                ]
            },
            "Data": {
                "date": {"start": data_referencia}
            },
            "Faturamento Total": {
                "number": metricas["faturamento_total"]
            },
            "Quantidade Vendida": {
                "number": metricas["quantidade_total"]
            },
            "Ticket Médio": {
                "number": metricas["ticket_medio"]
            },
        },
    }
    return payload


def enviar_para_notion(metricas: dict, data_referencia: str = None) -> requests.Response:
    """
    Envia as métricas consolidadas para o Notion, criando uma nova página
    (registro) no database configurado.

    Parâmetros:
        metricas: dicionário com as chaves 'faturamento_total',
                  'quantidade_total' e 'ticket_medio'
                  (mesmo formato retornado por calcular_metricas_gerais).
        data_referencia: data do relatório no formato 'YYYY-MM-DD'.
                          Se não informado, usa a data atual.

    Retorna:
        O objeto Response da requisição, para inspeção/tratamento de erros.
    """
    _validar_configuracao()

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }

    payload = montar_payload(metricas, data_referencia)

    resposta = requests.post(NOTION_API_URL, headers=headers, json=payload, timeout=15)

    if resposta.status_code == 200:
        print("Dados enviados ao Notion com sucesso!")
    else:
        print(f"Erro ao enviar dados ao Notion ({resposta.status_code}): {resposta.text}")

    return resposta


if __name__ == "__main__":
    # Exemplo manual de uso (requer .env configurado)
    metricas_exemplo = {
        "faturamento_total": 12500.75,
        "quantidade_total": 340,
        "ticket_medio": 87.30,
    }
    enviar_para_notion(metricas_exemplo)
