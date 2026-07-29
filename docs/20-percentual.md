# 20. Percentual

> **Tarefa:** Calcular a participação de cada item em relação ao total.  
> **Datasets:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

```excel
=F2/SOMA($F$2:$F$52)                     → % de cada salário no total
=F2/SOMA($F$2:$F$52)*100                 → em porcentagem
=SOMASE(C:C;"TI";F:F)/SOMA(F:F)         → % da folha do depto TI
```

**Formatar como porcentagem:** Ctrl+Shift+% ou Formato → Porcentagem

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# Percentual de cada salário no total
total_sal = df["salario"].sum()
df["pct_folha"] = (df["salario"] / total_sal * 100).round(2)

# Percentual por departamento
pct_depto = (
    df.groupby("departamento")["salario"]
    .sum()
    .div(total_sal)
    .mul(100)
    .round(1)
    .rename("pct_folha_%")
)

# Percentual por linha dentro do grupo (participação no depto)
df["total_depto"] = df.groupby("departamento")["salario"].transform("sum")
df["pct_no_depto"] = (df["salario"] / df["total_depto"] * 100).round(1)

# Percentual de pedidos por produto
pct_produto = (
    orders.groupby("id_produto")["valor_total"]
    .sum()
    .div(orders["valor_total"].sum())
    .mul(100)
    .round(1)
    .sort_values(ascending=False)
)

print("% da folha por departamento:")
print(pct_depto)
print("\n% de vendas por produto:")
print(pct_produto)
```

---

## SQL

```sql
-- % de cada salário no total geral
SELECT nome, salario,
       ROUND(salario * 100.0 / SUM(salario) OVER (), 2) AS pct_folha
FROM employees
WHERE salario IS NOT NULL
ORDER BY pct_folha DESC;

-- % por departamento
SELECT departamento,
       SUM(salario) AS total,
       ROUND(SUM(salario) * 100.0 / SUM(SUM(salario)) OVER (), 1) AS pct_total
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento
ORDER BY pct_total DESC;

-- % dentro do próprio departamento
SELECT nome, departamento, salario,
       ROUND(salario * 100.0 / SUM(salario) OVER (PARTITION BY departamento), 1)
           AS pct_no_depto
FROM employees
WHERE salario IS NOT NULL;

-- % por produto em pedidos
SELECT id_produto,
       SUM(valor_total) AS total,
       ROUND(SUM(valor_total) * 100.0 / SUM(SUM(valor_total)) OVER (), 1) AS pct
FROM orders
GROUP BY id_produto
ORDER BY pct DESC;
```

---

## Power BI

**DAX:**
```dax
% da Folha =
DIVIDE(
    SUM(employees[salario]),
    CALCULATE(SUM(employees[salario]), ALL(employees)),
    0
) * 100

% no Departamento =
DIVIDE(
    SUM(employees[salario]),
    CALCULATE(SUM(employees[salario]), ALLEXCEPT(employees, employees[departamento])),
    0
) * 100
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Participação no total | `/ SUM(...) OVER ()` / `DIVIDE(..., ALL(...))` |
| Participação por grupo | `/ SUM(...) OVER (PARTITION BY col)` / `ALLEXCEPT` |
| Exibição formatada | `f"{valor:.1%}"` no Python / Formato % no Power BI |

---

## Armadilhas comuns

- No SQLite, `5 / 2 = 2` (divisão inteira) — sempre use `5 * 1.0 / 2` ou `5.0 / 2`
- `DIVIDE()` no DAX evita divisão por zero — prefira ao operador `/`
- Transformar `pct_folha` em `transform("sum")` é fundamental para calcular % por grupo sem `merge`

## Veja também
- [Soma](08-soma.md)
- [Agrupar Dados](05-agrupar-agregar.md)
- [Ranking](21-ranking.md)
