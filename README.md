# Automação de relatório — exemplo vendas

Dois CSVs de canais diferentes → um resumo (faturamento, pedidos, ticket) → arquivo + opcional no Notion.

O exemplo usa Shopify e Mercado Livre. O motor é o mesmo pra qualquer operação que fecha o dia juntando planilha na mão (loja, clínica, escritório).

**Autor:** [Matheus Scherer](https://github.com/matheusscherer) — automação de processos com Python.

---

## Processo

| | |
|---|---|
| **Entra** | `dados/vendas_shopify.csv` e `dados/vendas_mercado_livre.csv` (colunas `data`, `valor`, `quantidade`) |
| **Sai** | `dados/vendas_consolidadas.csv` + números no terminal (faturamento, qtd, pedidos, ticket médio) |
| **Opcional** | a mesma linha no Notion (`--enviar-notion`) |

Nada publica sozinho. Sem a flag, só gera o arquivo.

---

## Como roda

```bash
git clone https://github.com/matheusscherer/sales-report-automation.git
cd sales-report-automation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

python -m sales_report.main
python -m sales_report.main --enviar-notion   # só se tiver .env
pytest -v
```

Troca os CSVs. Mantém as colunas. O relatório sai.

---

## Notion (opcional)

Copia `.env.example` → `.env`:

```env
NOTION_TOKEN=
NOTION_DATABASE_ID=
```

Database com: `Nome` (title), `Data` (date), `Faturamento Total` / `Quantidade Vendida` / `Ticket Médio` (number). Integração conectada no database.

---

Python 3.10+ · Pandas · Requests (Notion) · pytest + GitHub Actions · MIT
