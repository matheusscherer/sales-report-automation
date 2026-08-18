"""
Integração com a API do Notion para publicação do relatório.
"""

import os
from datetime import datetime
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"


def _validar_configuracao() -> None:
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        raise EnvironmentError(
            "As variáveis NOTION_TOKEN e NOTION_DATABASE_ID precisam estar "
            "definidas no arquivo .env. Veja o README para instruções."
        )


def montar_payload(metricas: Dict, data_referencia: Optional[str] = None) -> dict:
    data_referencia = data_referencia or datetime.now().strftime("%Y-%m-%d")

    return {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Nome": {
                "title": [
                    {"text": {"content": f"Relatório de Vendas - {data_referencia}"}}
                ]
            },
            "Data": {"date": {"start": data_referencia}},
            "Faturamento Total": {"number": metricas["faturamento_total"]},
            "Quantidade Vendida": {"number": metricas["quantidade_total"]},
            "Ticket Médio": {"number": metricas["ticket_medio"]},
        },
    }


def enviar_para_notion(
    metricas: Dict,
    data_referencia: Optional[str] = None,
) -> requests.Response:
    """Envia as métricas consolidadas para o Notion."""
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
