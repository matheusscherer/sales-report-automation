"""Testes da consolidação de vendas."""

from pathlib import Path

import pandas as pd
import pytest

from sales_report.consolidar import (
    calcular_metricas_gerais,
    gerar_resumo_diario,
)


@pytest.fixture
def df_exemplo():
    return pd.DataFrame({
        "data": pd.to_datetime(["2026-07-18", "2026-07-18", "2026-07-19"]),
        "valor": [100.0, 50.0, 200.0],
        "quantidade": [2, 1, 4],
        "canal": ["Shopify", "Mercado Livre", "Shopify"],
    })


def test_calcular_metricas(df_exemplo):
    metricas = calcular_metricas_gerais(df_exemplo)
    assert metricas["faturamento_total"] == 350.0
    assert metricas["quantidade_total"] == 7
    assert metricas["numero_pedidos"] == 3
    assert metricas["ticket_medio"] == pytest.approx(116.67, abs=0.01)


def test_resumo_diario(df_exemplo):
    resumo = gerar_resumo_diario(df_exemplo)
    assert len(resumo) == 2
    assert "faturamento" in resumo.columns
    assert "ticket_medio" in resumo.columns
