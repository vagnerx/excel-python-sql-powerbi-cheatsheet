# 19. Top N Registros

> **Tarefa:** Retornar os N maiores (ou menores) registros de uma coluna.  
> **Datasets:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

```excel
=GRANDE(F2:F52;1)    → 1º maior salário
=GRANDE(F2:F52;3)    → 3º maior salário
=PEQUENO(F2:F52;1)   → menor salário

-- Top 5 com FILTRAR (Excel 365):
=FILTRAR(A2:H52;F2:F52>=GRANDE(F2:F52;5))
```

**Interface:** Dados → Filtro → Filtro por Número → "10 Principais"

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# Top 5 maiores salários
top5_sal = df.nlargest(5, "salario")[["nome", "departamento", "salario"]]

# Bottom 5 menores salários
bottom5_sal = df.nsmallest(5, "salario")[["nome", "departamento", "salario"]]

# Top 5 com colunas adicionais
top5_full = df.nlargest(5, "salario").reset_index(drop=True)
top5_full.index += 1   # ranking começa em 1

# Top N por grupo — top 2 de cada departamento
top2_por_depto = (
    df.sort_values("salario", ascending=False)
    .groupby("departamento")
    .head(2)
    .sort_values(["departamento", "salario"], ascending=[True, False])
)

# Top 10 pedidos por valor
top10_pedidos = orders.nlargest(10, "valor_total")[["id_pedido","id_cliente","valor_total"]]

print("Top 5 salários:")
print(top5_sal.to_string(index=False))
print("\nTop 2 por departamento:")
print(top2_por_depto[["departamento","nome","salario"]].to_string(index=False))
```

---

## SQL

```sql
-- Top 5 maiores salários (SQLite)
SELECT nome, departamento, salario
FROM employees
WHERE salario IS NOT NULL
ORDER BY salario DESC
LIMIT 5;

-- Top 5 com posição
SELECT nome, departamento, salario,
       ROW_NUMBER() OVER (ORDER BY salario DESC) AS posicao
FROM employees
WHERE salario IS NOT NULL
LIMIT 5;

-- Top 2 por departamento (Window Function)
SELECT nome, departamento, salario
FROM (
    SELECT nome, departamento, salario,
           ROW_NUMBER() OVER (
               PARTITION BY departamento
               ORDER BY salario DESC
           ) AS rnk
    FROM employees
    WHERE salario IS NOT NULL
)
WHERE rnk <= 2
ORDER BY departamento, salario DESC;

-- Top 10 pedidos
SELECT id_pedido, id_cliente, valor_total
FROM orders
ORDER BY valor_total DESC
LIMIT 10;
```

---

## Power BI

**Interface:** Filtros → Top N → selecionar coluna e campo

**DAX:**
```dax
Top 5 Funcionários =
TOPN(5, employees, employees[salario], DESC)

Top N Salários Medida =
CALCULATE(
    SUM(employees[salario]),
    TOPN(
        5,
        VALUES(employees[nome]),
        CALCULATE(SUM(employees[salario]))
    )
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Ranking global | `nlargest(N)` / `ORDER BY ... LIMIT N` |
| Top N por categoria | `groupby().head(N)` / `PARTITION BY` |
| Visualização de líderes | `TOPN` no DAX |

---

## Armadilhas comuns

- `ORDER BY ... LIMIT N` **não garante determinismo** em caso de empate — use `ROW_NUMBER()` ou `RANK()`
- `nlargest()` ignora nulos automaticamente
- No DAX, `TOPN` retorna uma **tabela**, não um escalar — use dentro de `CALCULATE` ou `CALCULATETABLE`

## Veja também
- [Ordenar Dados](04-ordenar-dados.md)
- [Ranking](21-ranking.md)
- [Min / Max](15-min-max.md)
