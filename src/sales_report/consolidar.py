"""
Leitura, consolidação e cálculo de métricas de vendas multi-canal.
"""

from pathlib import Path
from typing import Dict

import pandas as pd

PASTA_DADOS = Path(__file__).resolve().parents[2] / "dados"
ARQUIVO_SHOPIFY = PASTA_DADOS / "vendas_shopify.csv"
ARQUIVO_MERCADO_LIVRE = PASTA_DADOS / "vendas_mercado_livre.csv"
ARQUIVO_SAIDA = PASTA_DADOS / "vendas_consolidadas.csv"


def ler_vendas(caminho_csv: Path, canal: str) -> pd.DataFrame:
    """Lê um CSV de vendas de um canal específico e adiciona a coluna 'canal'."""
    df = pd.read_csv(caminho_csv, parse_dates=["data"])
    df["canal"] = canal
    return df


def consolidar_canais(
    caminho_shopify: Path = ARQUIVO_SHOPIFY,
    caminho_mercado_livre: Path = ARQUIVO_MERCADO_LIVRE,
) -> pd.DataFrame:
    """Une os dados de todos os canais em um único dataframe."""
    df_shopify = ler_vendas(caminho_shopify, "Shopify")
    df_mercado_livre = ler_vendas(caminho_mercado_livre, "Mercado Livre")

    df_consolidado = pd.concat([df_shopify, df_mercado_livre], ignore_index=True)
    df_consolidado.sort_values("data", inplace=True)
    return df_consolidado


def calcular_metricas_gerais(df: pd.DataFrame) -> Dict:
    """Calcula as métricas gerais do período."""
    faturamento_total = round(df["valor"].sum(), 2)
    quantidade_total = int(df["quantidade"].sum())
    numero_pedidos = len(df)
    ticket_medio = round(faturamento_total / numero_pedidos, 2) if numero_pedidos else 0

    return {
        "faturamento_total": faturamento_total,
        "quantidade_total": quantidade_total,
        "numero_pedidos": numero_pedidos,
        "ticket_medio": ticket_medio,
    }


def gerar_resumo_diario(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa os dados por dia."""
    resumo = (
        df.groupby(df["data"].dt.date)
        .agg(
            faturamento=("valor", "sum"),
            quantidade_vendida=("quantidade", "sum"),
            numero_pedidos=("valor", "count"),
        )
        .reset_index()
        .rename(columns={"data": "data"})
    )

    resumo["ticket_medio"] = (resumo["faturamento"] / resumo["numero_pedidos"]).round(2)
    resumo["faturamento"] = resumo["faturamento"].round(2)
    return resumo


def salvar_resumo(resumo: pd.DataFrame, caminho_saida: Path = ARQUIVO_SAIDA) -> None:
    """Salva o resumo diário consolidado em CSV."""
    resumo.to_csv(caminho_saida, index=False, encoding="utf-8")
