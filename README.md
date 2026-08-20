# Sales Report Automation

Two sales CSVs become one clean summary.

Reads two channel CSVs, concatenates them, calculates revenue / quantity / orders / average ticket, and writes a consolidated CSV. Optional: one Notion row (`--enviar-notion`).

Example files are named `vendas_shopify.csv` and `vendas_mercado_livre.csv`. **They are CSVs with the same schema** (`data`, `valor`, `quantidade`). There is no Shopify or Mercado Livre API in this repository.

**Author:** [Matheus Scherer](https://github.com/matheusscherer) · Porto Alegre, Brazil

---

## What it does

| | |
|---|---|
| **Input** | Two CSVs with columns `data`, `valor`, `quantidade` |
| **Output** | `dados/vendas_consolidadas.csv` + numbers in the terminal |
| **Optional** | POST to Notion API, only with flag and `.env` |

Nothing publishes by itself. Without `--enviar-notion`, it only generates a file.

---

## Stack

Python 3.10+ · Pandas · Requests · python-dotenv · pytest · GitHub Actions · MIT

---

## How to run

```bash
git clone https://github.com/matheusscherer/sales-report-automation.git
cd sales-report-automation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

python -m sales_report.main
python -m sales_report.main --enviar-notion   # only with .env
pytest -v
```

Replace the CSVs. Keep the columns. The report comes out.

---

## Evidence / demo

- Example data in `dados/`
- Tests: metrics, daily summary, empty base (ticket = 0), `parametrize`
- Green CI on Python 3.10 / 3.11 / 3.12
- Notion: real API integration, **opt-in**. Without token, the script does not send.

No client screenshots. No measured hours saved.

---

## Limitations

- Both channels need the **same schema**. It does not map real Shopify vs Mercado Livre exports.
- Notion creates one page per run — not idempotent.
- No scheduling. Runs when you run it.

---

## What this is NOT

- Not an integration with Shopify or Mercado Livre APIs.
- Not ERP, tax, real-time dashboard, or 24/7 revenue tracking.
- Not a client case. It is an example with CSV.

---

[LinkedIn](https://linkedin.com/in/scherermatheus) · [Site](https://mtsch-site.vercel.app) · [GitHub](https://github.com/matheusscherer)
