"""
main.py

Ponto de entrada da automação. Executa o pipeline completo:
1. Lê e consolida os dados de vendas (Shopify + Mercado Livre)
2. Calcula as métricas gerais do período
3. Gera o CSV consolidado por dia
4. Envia o resumo para o Notion (opcional, se configurado)

Uso:
    python scripts/main.py
    python scripts/main.py --enviar-notion
"""

import argparse
from datetime import datetime

from consolidar_vendas import (
    consolidar_canais,
    calcular_metricas_gerais,
    gerar_resumo_diario,
    salvar_resumo,
    ARQUIVO_SAIDA,
)
from notion_integration import enviar_para_notion


def executar_pipeline(enviar_notion: bool = False) -> None:
    print("Lendo e consolidando os dados de vendas...")
    df = consolidar_canais()

    print("Calculando métricas gerais...")
    metricas = calcular_metricas_gerais(df)

    print("Gerando resumo diário...")
    resumo_diario = gerar_resumo_diario(df)
    salvar_resumo(resumo_diario)

    print("\n===== RELATÓRIO DE VENDAS =====")
    print(f"Faturamento total.......: R$ {metricas['faturamento_total']:.2f}")
    print(f"Quantidade vendida......: {metricas['quantidade_total']} unidades")
    print(f"Número de pedidos.......: {metricas['numero_pedidos']}")
    print(f"Ticket médio.............: R$ {metricas['ticket_medio']:.2f}")
    print(f"Arquivo consolidado.....: {ARQUIVO_SAIDA}")
    print("================================\n")

    if enviar_notion:
        print("Enviando resumo para o Notion...")
        data_referencia = datetime.now().strftime("%Y-%m-%d")
        enviar_para_notion(metricas, data_referencia)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automação de relatório de vendas para e-commerce.")
    parser.add_argument(
        "--enviar-notion",
        action="store_true",
        help="Envia o resumo consolidado para o Notion após gerar o relatório.",
    )
    args = parser.parse_args()

    executar_pipeline(enviar_notion=args.enviar_notion)
