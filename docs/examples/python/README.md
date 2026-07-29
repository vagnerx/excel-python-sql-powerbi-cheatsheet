# Exemplos Python — Cheat Sheet

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vagnerx/excel-python-sql-powerbi-cheatsheet/blob/main/notebooks/cheatsheet_completo.ipynb)

Exemplos práticos e executáveis de todas as 24 operações do cheat sheet usando **Python + Pandas**.

---

## Como executar

### Opção 1 — Google Colab (sem instalar nada)

Clique no badge acima ou acesse diretamente:  
https://colab.research.google.com/github/vagnerx/excel-python-sql-powerbi-cheatsheet/blob/main/notebooks/cheatsheet_completo.ipynb

### Opção 2 — Local

```bash
# Instalar dependências
pip install pandas numpy

# Executar um script específico
python docs/examples/python/01_import_data.py
python docs/examples/python/02_filtering.py
python docs/examples/python/03_grouping.py
python docs/examples/python/04_joins.py
python docs/examples/python/05_dates.py
python docs/examples/python/06_advanced.py

# Ou o notebook completo
jupyter notebook notebooks/cheatsheet_completo.ipynb
```

---

## Scripts disponíveis

| Script | Operações cobertas |
|---|---|
| `01_import_data.py` | Importar CSV, Excel, SQLite; inspecionar DataFrame |
| `02_filtering.py` | Filtros simples, compostos, isin, texto, nulos, datas, between, query() |
| `03_grouping.py` | groupby, agg, pivot_table, value_counts, transform, HAVING equivalente |
| `04_joins.py` | INNER, LEFT, RIGHT, OUTER, anti-join, join encadeado |
| `05_dates.py` | Extração de partes, tempo de casa, filtros, agrupamento por período, rolling |
| `06_advanced.py` | Ranking, percentual, np.select, pivot/melt, janela móvel, acumulado, Top N |

---

## Datasets utilizados

| Arquivo | Linhas | Descrição |
|---|---|---|
| `datasets/employees.csv` | 52 | Funcionários com nulos e duplicatas intencionais |
| `datasets/customers.csv` | 20 | Clientes — usado nos JOINs |
| `datasets/orders.csv` | 100 | Pedidos — usado em datas, acumulado, janela móvel |

---

## Notebook completo

O notebook `notebooks/cheatsheet_completo.ipynb` contém todas as 24 operações em sequência,
organizadas nos 4 grupos do cheat sheet:

- **Grupo A** — Manipulação Básica (operações 1–8)
- **Grupo B** — Transformação (operações 9–14)
- **Grupo C** — Datas e Métricas (operações 15–20)
- **Grupo D** — Analytics Avançado (operações 21–24)

---

## Veja também

- [Exemplos SQL](../sql/README.md)
- [Exemplos Power BI](../powerbi/README.md)
- [Documentação completa](https://vagnerx.github.io/excel-python-sql-powerbi-cheatsheet/)