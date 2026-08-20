# Relatório de vendas — dois CSVs viram um resumo

Lê dois CSVs de canais, concatena, calcula faturamento / quantidade / pedidos / ticket médio, grava um CSV consolidado. Opcional: uma linha no Notion (`--enviar-notion`).

Os arquivos de exemplo se chamam `vendas_shopify.csv` e `vendas_mercado_livre.csv`. **São CSVs no mesmo schema** (`data`, `valor`, `quantidade`). Não há API da Shopify nem do Mercado Livre neste repositório.

**Autor:** [Matheus Scherer](https://github.com/matheusscherer) · Porto Alegre

---

## O que faz

| | |
|---|---|
| **Entra** | Dois CSVs com colunas `data`, `valor`, `quantidade` |
| **Sai** | `dados/vendas_consolidadas.csv` + números no terminal |
| **Opcional** | POST na API do Notion, só com flag e `.env` |

Nada publica sozinho. Sem `--enviar-notion`, só gera arquivo.

---

## Stack

Python 3.10+ · Pandas · Requests · python-dotenv · pytest · GitHub Actions · MIT

---

## Como executar

```bash
git clone https://github.com/matheusscherer/sales-report-automation.git
cd sales-report-automation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

python -m sales_report.main
python -m sales_report.main --enviar-notion   # só com .env
pytest -v
```

Troca os CSVs. Mantém as colunas. O relatório sai.

---

## Evidência / demo

- Dados de exemplo em `dados/`
- Testes: métricas, resumo diário, base vazia (ticket = 0), `parametrize`
- CI verde em Python 3.10 / 3.11 / 3.12
- Notion: integração real via API, **opt-in**. Sem token, o script não envia.

Não há print de cliente. Não há hora economizada medida.

---

## Limitações

- Os dois canais precisam do **mesmo schema**. Não mapeia export real da Shopify vs. Mercado Livre.
- Notion cria uma página por execução — não é idempotente.
- Sem agendamento. Roda quando você roda.

---

## O que isto NÃO é

- Não é integração com API da Shopify ou do Mercado Livre.
- Não é ERP, fiscal, dashboard em tempo real, nem receita 24/7.
- Não é case de cliente. É exemplo com CSV.

---

Python 3.10+ · Pandas · Requests (Notion) · pytest · MIT
