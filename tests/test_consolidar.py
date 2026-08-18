"""Testes da consolidação de vendas."""

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


# ---------------------------------------------------------------------------
# parametrize = um teste, vários cenários (o 20% que mais vale em pytest)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "valores, quantidades, fat_esperado, qtd_esperada, ticket_esperado",
    [
        # caso feliz
        ([100.0, 50.0], [2, 1], 150.0, 3, 75.0),
        # um único pedido
        ([200.0], [4], 200.0, 4, 200.0),
        # valores fracionários
        ([10.5, 20.25], [1, 1], 30.75, 2, 15.38),
    ],
)
def test_metricas_parametrizadas(valores, quantidades, fat_esperado, qtd_esperada, ticket_esperado):
    """Mesma lógica, entradas diferentes — sem copiar/colar três testes."""
    df = pd.DataFrame({
        "data": pd.to_datetime(["2026-07-18"] * len(valores)),
        "valor": valores,
        "quantidade": quantidades,
        "canal": ["Shopify"] * len(valores),
    })
    m = calcular_metricas_gerais(df)
    assert m["faturamento_total"] == fat_esperado
    assert m["quantidade_total"] == qtd_esperada
    assert m["ticket_medio"] == pytest.approx(ticket_esperado, abs=0.01)


def test_dataframe_vazio():
    """Borda: base vazia não pode quebrar (ZeroDivision)."""
    df = pd.DataFrame(columns=["data", "valor", "quantidade", "canal"])
    m = calcular_metricas_gerais(df)
    assert m["faturamento_total"] == 0
    assert m["numero_pedidos"] == 0
    assert m["ticket_medio"] == 0
