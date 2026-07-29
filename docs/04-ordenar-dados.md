# 4. Ordenar Dados

> **Tarefa:** Organizar registros em ordem crescente ou decrescente.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Interface:** Dados → Classificar → Adicionar Nível

```excel
=CLASSIFICAR(F2:F52; 1; -1)   → ordena salários do maior para o menor (Excel 365)
```

**Classificação multi-coluna:** Dados → Classificar → Adicionar Nível → departamento ASC, salario DESC

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Ordenar por uma coluna (crescente)
df_ord = df.sort_values("salario")

# Ordenar decrescente
df_ord_desc = df.sort_values("salario", ascending=False)

# Ordenar por múltiplas colunas
df_multi = df.sort_values(
    ["departamento", "salario"],
    ascending=[True, False]   # depto ASC, salário DESC
)

# Ordenar por index
df.sort_index(ascending=True)

# Top 5 maiores salários
top5 = df.nlargest(5, "salario")
print(top5[["nome", "departamento", "salario"]])
```

---

## SQL

```sql
-- Ordem crescente (padrão)
SELECT nome, salario
FROM employees
ORDER BY salario;

-- Ordem decrescente
SELECT nome, salario
FROM employees
ORDER BY salario DESC;

-- Múltiplas colunas
SELECT nome, departamento, salario
FROM employees
ORDER BY departamento ASC, salario DESC;

-- Com filtro + ordenação
SELECT nome, departamento, salario
FROM employees
WHERE ativo = 'Sim'
ORDER BY salario DESC
LIMIT 10;

-- Nulos por último (SQLite)
SELECT nome, salario
FROM employees
ORDER BY salario IS NULL, salario DESC;
```

---

## Power BI

**Interface:** Selecione a coluna → clique em "Classificar por Coluna"

**DAX — Top N por departamento:**
```dax
Ranking Salário =
RANKX(
    ALLSELECTED(employees),
    employees[salario],
    ,
    DESC,
    Dense
)
```

**Power Query M:**
```powerquery-m
= Table.Sort(employees, {{"salario", Order.Descending}})
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Exibição em relatório | ORDER BY no SQL / Classificar no Excel |
| Top N registros | `nlargest()` no Python / `ORDER BY ... LIMIT N` |
| Ranking por grupo | `RANKX` no DAX |

---

## Armadilhas comuns

- `sort_values` **não modifica** o DataFrame original — use `inplace=True` ou reatribua
- No SQL, `ORDER BY` sem `LIMIT` em tabelas grandes impacta performance
- Nulos são tratados diferente por cada ferramenta: SQL os coloca no início ou fim dependendo do SGBD

## Veja também
- [Top N Registros](19-top-n.md)
- [Ranking](21-ranking.md)
- [Filtrar Linhas](02-filtrar-linhas.md)
