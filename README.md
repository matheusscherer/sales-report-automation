# Sales Report Automation

Automação em Python que consolida dados de vendas de múltiplos canais de e-commerce (**Shopify** e **Mercado Livre**), calcula métricas principais e publica automaticamente um resumo diário no **Notion**.

Projeto de portfólio focado em automação de processos, integração de dados e APIs.

---

## O que faz

1. Lê CSVs de vendas de cada canal
2. Consolida em uma única base
3. Calcula faturamento, quantidade vendida, número de pedidos e ticket médio
4. Gera resumo diário em CSV
5. (Opcional) Publica o resumo no Notion via API

---

## Estrutura

```text
sales-report-automation/
├── src/
│   └── sales_report/
│       ├── __init__.py
│       ├── consolidar.py
│       ├── notion.py
│       └── main.py
├── dados/
│   ├── vendas_shopify.csv
│   └── vendas_mercado_livre.csv
├── tests/
├── docs/
├── .env.example
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Instalação

```bash
git clone https://github.com/matheusscherer/sales-report-automation.git
cd sales-report-automation

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

---

## Como usar

```bash
# Apenas consolida e gera o relatório
python -m sales_report.main
# ou
sales-report

# Com envio para o Notion
sales-report --enviar-notion
```

### Configuração do Notion (opcional)

1. Crie uma integração em [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Crie um database com as colunas: `Nome` (Title), `Data` (Date), `Faturamento Total` (Number), `Quantidade Vendida` (Number), `Ticket Médio` (Number)
3. Conecte a integração ao database
4. Copie `.env.example` para `.env` e preencha:

```env
NOTION_TOKEN=seu_token_aqui
NOTION_DATABASE_ID=seu_database_id_aqui
```

---

## Testes

```bash
pytest -v
```

---

## Stack

- Python 3.10+
- Pandas
- Requests + Notion API
- python-dotenv
- pytest + GitHub Actions

---

**Matheus Scherer** · [github.com/matheusscherer](https://github.com/matheusscherer)

MIT License
