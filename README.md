# 📊 Automação de Relatório de Vendas para E-commerce

Automação em Python que consolida dados de vendas de múltiplos canais de
e-commerce (Shopify e Mercado Livre), calcula as métricas principais do
negócio e publica automaticamente um resumo diário em uma página do
Notion — eliminando o trabalho manual de exportar planilhas e montar
relatórios todos os dias.

Projeto criado para fins de portfólio e prospecção de clientes de
automação de processos (RPA / integração de dados).

---

## 🧩 O problema

Lojistas que vendem em mais de um canal (site próprio via Shopify,
marketplaces como Mercado Livre, etc.) normalmente precisam:

- Baixar relatórios separados de cada plataforma;
- Consolidar tudo manualmente em uma planilha;
- Calcular faturamento, ticket médio e volume de vendas "na mão";
- Repetir esse processo todos os dias ou todas as semanas.

Isso consome tempo, é sujeito a erro humano e atrasa a tomada de decisão.

## ✅ A solução

Este projeto automatiza esse fluxo de ponta a ponta:

1. **Lê** os arquivos de vendas exportados de cada canal (CSV);
2. **Consolida** tudo em uma única base de dados;
3. **Calcula** faturamento total, quantidade de produtos vendidos e
   ticket médio, além de um resumo dia a dia;
4. **Publica** automaticamente o resumo em uma página/database do
   Notion, deixando o relatório sempre atualizado e acessível para o
   time, sem intervenção manual.

O mesmo pipeline pode ser adaptado para rodar todos os dias via
agendador (cron, Task Scheduler, GitHub Actions, etc.), mantendo o
Notion sempre atualizado sem nenhuma ação manual.

---

## 🛠️ Tecnologias usadas

| Tecnologia       | Uso                                                |
|------------------|-----------------------------------------------------|
| Python 3.10+     | Linguagem principal da automação                    |
| Pandas           | Leitura, consolidação e cálculo das métricas        |
| Requests         | Requisições HTTP para a API do Notion               |
| python-dotenv    | Gerenciamento seguro de variáveis de ambiente       |
| Notion API       | Publicação automática do relatório                  |

---

## 📁 Estrutura do projeto

```
sales-report-automation/
├── dados/
│   ├── vendas_shopify.csv          # dados fictícios (30 dias)
│   ├── vendas_mercado_livre.csv    # dados fictícios (30 dias)
│   └── vendas_consolidadas.csv     # gerado automaticamente pelo script
├── scripts/
│   ├── consolidar_vendas.py        # leitura, consolidação e cálculo de métricas
│   ├── notion_integration.py       # integração com a API do Notion
│   └── main.py                     # ponto de entrada da automação
├── docs/
│   └── exemplo_saida.md            # exemplo de saída no console, CSV e Notion
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sales-report-automation.git
cd sales-report-automation
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o pipeline (sem enviar ao Notion)

```bash
cd scripts
python main.py
```

Isso vai ler os CSVs em `dados/`, calcular as métricas e gerar o
arquivo `dados/vendas_consolidadas.csv` com o resumo diário.

### 5. Rode o pipeline enviando o resumo para o Notion

```bash
python main.py --enviar-notion
```

(veja a seção abaixo para configurar a integração antes de usar essa opção)

---

## 🔗 Como configurar a integração com o Notion

### Passo 1 — Criar a integração

1. Acesse [notion.so/my-integrations](https://www.notion.so/my-integrations);
2. Clique em **"New integration"**;
3. Dê um nome (ex: `Automação de Vendas`) e selecione o workspace;
4. Copie o **"Internal Integration Token"** gerado — esse é o seu `NOTION_TOKEN`.

### Passo 2 — Criar o database no Notion

1. Crie uma página no Notion e adicione um **database** (tabela) com as
   colunas abaixo (os nomes devem ser exatamente estes):

   | Nome da coluna       | Tipo   |
   |-----------------------|--------|
   | Nome                  | Title  |
   | Data                  | Date   |
   | Faturamento Total      | Number |
   | Quantidade Vendida     | Number |
   | Ticket Médio           | Number |

2. Clique em **"Share"** no canto superior direito da página do database
   e conecte a integração criada no Passo 1 (ela precisa ter acesso
   explícito ao database para poder escrever nele).

3. Copie o **ID do database**: é o trecho de 32 caracteres presente na
   URL da página, por exemplo:

   ```
   https://www.notion.so/workspace/1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d?v=...
                                    └──────────── database_id ────────────┘
   ```

### Passo 3 — Configurar as variáveis de ambiente

1. Copie o arquivo de exemplo:

   ```bash
   cp .env.example .env
   ```

2. Preencha o arquivo `.env` com seus dados reais:

   ```
   NOTION_TOKEN=seu_token_aqui
   NOTION_DATABASE_ID=seu_database_id_aqui
   ```

3. **Nunca** suba o arquivo `.env` (com valores reais) para o GitHub —
   ele já está listado no `.gitignore`.

### Passo 4 — Rodar com a integração ativa

```bash
python scripts/main.py --enviar-notion
```

Se tudo estiver configurado corretamente, uma nova página (registro)
será criada no seu database do Notion com o resumo do dia.

---

## 📈 Exemplo de saída

**No console:**

```
===== RELATÓRIO DE VENDAS =====
Faturamento total.......: R$ 87899.55
Quantidade vendida......: 785 unidades
Número de pedidos.......: 318
Ticket médio.............: R$ 276.41
Arquivo consolidado.....: dados/vendas_consolidadas.csv
================================
```

**No CSV gerado (`dados/vendas_consolidadas.csv`):**

| data       | faturamento | quantidade_vendida | numero_pedidos | ticket_medio |
|------------|-------------|---------------------|-----------------|----------------|
| 2026-07-18 | 2975.21     | 25                  | 14              | 212.52         |
| 2026-07-19 | 2193.46     | 22                  | 11              | 199.41         |
| 2026-07-20 | 3774.06     | 34                  | 13              | 290.31         |

Veja mais detalhes, incluindo o exemplo de registro criado no Notion,
em [`docs/exemplo_saida.md`](docs/exemplo_saida.md).

---

## 🔮 Possíveis melhorias futuras

- [ ] Suporte a mais canais de venda (Amazon, Shopee, loja física via PDV);
- [ ] Agendamento automático via GitHub Actions ou cron, sem intervenção manual;
- [ ] Envio de alertas por e-mail/WhatsApp quando o faturamento diário
      ficar abaixo de uma meta configurável;
- [ ] Dashboard interativo (Streamlit) para visualizar as métricas
      históricas além do Notion;
- [ ] Testes automatizados (pytest) para as funções de consolidação e cálculo;
- [ ] Suporte a múltiplas lojas/clientes no mesmo pipeline (multi-tenant);
- [ ] Deploy como serviço containerizado (Docker) rodando em produção.

---

## 📄 Licença

Este é um projeto de portfólio, livre para uso e adaptação como
referência de aprendizado.

---

**Desenvolvido por Matheus Scherer** — Analista de Dados e Automação Júnior
[GitHub](https://github.com/matheusscherer)
