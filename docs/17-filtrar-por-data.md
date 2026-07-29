# 17. Filtrar por Data

> **Tarefa:** Selecionar registros dentro de um intervalo ou período específico.  
> **Datasets:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

```excel
=FILTRAR(A2:H52;G2:G52>="2023-01-01")         → admitidos de 2023 em diante (Excel 365)
=FILTRAR(A2:H52;(G2:G52>="2023-01-01")*(G2:G52<="2023-12-31"))   → só 2023
```

**Interface:** Dados → Filtro → Filtro por Data → "No ano" / "Entre datas"

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# Converter para datetime
df["data_admissao"] = pd.to_datetime(df["data_admissao"], errors="coerce")
orders["data_pedido"] = pd.to_datetime(orders["data_pedido"], errors="coerce")

# Filtro por data exata
df_2023 = df[df["data_admissao"].dt.year == 2023]

# Filtro por intervalo
inicio = pd.Timestamp("2022-01-01")
fim    = pd.Timestamp("2023-12-31")
df_intervalo = df[(df["data_admissao"] >= inicio) & (df["data_admissao"] <= fim)]

# Filtro com string (Pandas converte automaticamente)
orders_2024 = orders[orders["data_pedido"] >= "2024-01-01"]

# Filtro por mês específico
pedidos_jan = orders[orders["data_pedido"].dt.month == 1]

# Filtro com between (mais legível)
mask = orders["data_pedido"].between("2024-01-01", "2024-06-30")
orders_h1_2024 = orders[mask]

# Último N dias
hoje = pd.Timestamp.today()
ultimos_30 = orders[orders["data_pedido"] >= hoje - pd.Timedelta(days=30)]

print(f"Admissões em 2023: {len(df_2023)}")
print(f"Pedidos 1º semestre 2024: {len(orders_h1_2024)}")
```

---

## SQL

```sql
-- Filtro por ano
SELECT * FROM employees
WHERE strftime('%Y', data_admissao) = '2023';

-- Filtro por intervalo
SELECT * FROM orders
WHERE data_pedido BETWEEN '2024-01-01' AND '2024-06-30';

-- Filtro últimos 30 dias (SQLite)
SELECT * FROM orders
WHERE data_pedido >= date('now', '-30 days');

-- Pedidos por mês
SELECT strftime('%Y-%m', data_pedido) AS mes, COUNT(*) AS qtd, SUM(valor_total) AS total
FROM orders
GROUP BY mes
ORDER BY mes;

-- Admissões nos últimos 2 anos
SELECT nome, departamento, data_admissao
FROM employees
WHERE data_admissao >= date('now', '-2 years')
  AND data_admissao IS NOT NULL
ORDER BY data_admissao DESC;
```

---

## Power BI

**Interface:** Filtros → Data é depois de / está entre

**DAX:**
```dax
Pedidos 2024 =
CALCULATE(
    COUNTROWS(orders),
    YEAR(orders[data_pedido]) = 2024
)

Pedidos H1 2024 =
CALCULATE(
    SUM(orders[valor_total]),
    orders[data_pedido] >= DATE(2024, 1, 1),
    orders[data_pedido] <= DATE(2024, 6, 30)
)

Últimos 30 Dias =
CALCULATE(
    SUM(orders[valor_total]),
    DATESINPERIOD(orders[data_pedido], TODAY(), -30, DAY)
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Análise de período específico | `BETWEEN` / `.between()` / `DATESINPERIOD` |
| Dados recentes (rolling window) | `date('now', '-N days')` / `pd.Timedelta` |
| Agregação por mês/ano | `strftime` / `dt.year` / `YEAR()` DAX |

---

## Armadilhas comuns

- Strings de data funcionam **apenas se** o formato for consistente (`YYYY-MM-DD`)
- `BETWEEN` no SQL inclui os extremos (início e fim)
- No Power BI, use uma **Tabela de Datas** para filtros de tempo avançados com `DATESINPERIOD`, `SAMEPERIODLASTYEAR` etc.

## Veja também
- [Extração de Datas](16-extracao-datas.md)
- [Janela Móvel](23-janela-movel.md)
- [Acumulado](22-acumulado.md)
