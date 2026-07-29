# 21. Ranking

> **Tarefa:** Ordenar posições dentro de um grupo ou no total geral.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=ORDEM.EQ(F2;$F$2:$F$52;0)          → ranking do maior para o menor (0=DESC)
=ORDEM.EQ(F2;$F$2:$F$52;1)          → ranking do menor para o maior (1=ASC)
```

**Com empate denso (dense rank):**
```excel
=SOMARPRODUTO((F$2:F$52>F2)/CONT.SE(F$2:F$52;F$2:F$52))+1
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Ranking simples (maior salário = posição 1)
df["ranking"] = df["salario"].rank(method="min", ascending=False).astype("Int64")

# Métodos de ranking:
# "min"    → em empate, o menor rank é atribuído a todos (RANK no SQL)
# "max"    → em empate, o maior rank é atribuído
# "dense"  → sem pulos (1, 2, 2, 3...)  ← dense rank
# "first"  → ordem de aparição no dataset
# "average"→ média dos ranks em empate

# Dense rank (sem pulos)
df["ranking_denso"] = df["salario"].rank(method="dense", ascending=False).astype("Int64")

# Ranking por grupo (rank dentro de cada departamento)
df["rank_no_depto"] = (
    df.groupby("departamento")["salario"]
    .rank(method="dense", ascending=False)
    .astype("Int64")
)

# Exibir top 3 de cada departamento
top3 = df[df["rank_no_depto"] <= 3].sort_values(
    ["departamento", "rank_no_depto"]
)[["nome", "departamento", "salario", "rank_no_depto"]]

print(top3.to_string(index=False))
```

---

## SQL

```sql
-- RANK (com pulos em empates: 1, 2, 2, 4)
SELECT nome, departamento, salario,
       RANK() OVER (ORDER BY salario DESC) AS rank_geral
FROM employees
WHERE salario IS NOT NULL;

-- DENSE_RANK (sem pulos: 1, 2, 2, 3)
SELECT nome, departamento, salario,
       DENSE_RANK() OVER (ORDER BY salario DESC) AS rank_denso
FROM employees
WHERE salario IS NOT NULL;

-- ROW_NUMBER (sem empates, ordem de chegada)
SELECT nome, departamento, salario,
       ROW_NUMBER() OVER (ORDER BY salario DESC) AS posicao
FROM employees
WHERE salario IS NOT NULL;

-- Ranking por departamento
SELECT nome, departamento, salario,
       DENSE_RANK() OVER (
           PARTITION BY departamento
           ORDER BY salario DESC
       ) AS rank_no_depto
FROM employees
WHERE salario IS NOT NULL
ORDER BY departamento, rank_no_depto;

-- Top 3 por departamento
SELECT nome, departamento, salario, rank_no_depto
FROM (
    SELECT nome, departamento, salario,
           DENSE_RANK() OVER (PARTITION BY departamento ORDER BY salario DESC) AS rank_no_depto
    FROM employees
    WHERE salario IS NOT NULL
)
WHERE rank_no_depto <= 3;
```

---

## Power BI

**DAX:**
```dax
Ranking Geral =
RANKX(
    ALL(employees),
    employees[salario],
    ,
    DESC,
    Dense
)

Ranking no Departamento =
RANKX(
    ALLSELECTED(employees[nome]),
    employees[salario],
    ,
    DESC,
    Dense
)
```

---

## Diferença entre RANK, DENSE_RANK e ROW_NUMBER

| Salário | RANK | DENSE_RANK | ROW_NUMBER |
|---|---|---|---|
| 15.000 | 1 | 1 | 1 |
| 12.000 | 2 | 2 | 2 |
| 12.000 | 2 | 2 | 3 |
| 10.000 | 4 | 3 | 4 |
| 9.000  | 5 | 4 | 5 |

---

## Armadilhas comuns

- `rank(method="min")` no Pandas equivale ao `RANK()` do SQL — ambos deixam pulos
- `RANKX` no DAX é sensível ao contexto de filtro — use `ALL()` para ranking global
- `ROW_NUMBER()` é determinístico apenas se o `ORDER BY` for único

## Veja também
- [Top N Registros](19-top-n.md)
- [Percentual](20-percentual.md)
- [Ordenar Dados](04-ordenar-dados.md)
