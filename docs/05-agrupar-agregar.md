# 5. Agrupar / Agregar Dados

> **Tarefa:** Resumir dados por categoria ou grupo.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Interface:** Inserir → Tabela Dinâmica  
- Arraste `departamento` para Linhas  
- Arraste `salario` para Valores → escolha Soma, Média ou Contagem

**Fórmulas de agregação:**
```excel
=SOMASE(C:C;"TI";F:F)             → soma salários do depto TI
=CONT.SE(C:C;"Vendas")            → conta funcionários de Vendas
=MÉDIASE(C:C;"Financeiro";F:F)    → média salarial do Financeiro
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Agrupar e somar
soma_por_depto = df.groupby("departamento")["salario"].sum()

# Agrupar e calcular múltiplas métricas
resumo = df.groupby("departamento").agg(
    total_funcionarios=("id", "count"),
    salario_medio=("salario", "mean"),
    salario_total=("salario", "sum"),
    maior_salario=("salario", "max"),
    menor_salario=("salario", "min"),
)

# Múltiplos grupos
por_depto_ativo = df.groupby(["departamento", "ativo"])["salario"].mean()

# Pivot Table (equivalente à tabela dinâmica)
pivot = df.pivot_table(
    values="salario",
    index="departamento",
    columns="ativo",
    aggfunc="mean"
)

print(resumo.round(2))
```

---

## SQL

```sql
-- Soma por departamento
SELECT departamento, SUM(salario) AS total_salarios
FROM employees
GROUP BY departamento;

-- Múltiplas métricas
SELECT
    departamento,
    COUNT(*)          AS total_func,
    AVG(salario)      AS media_salarial,
    SUM(salario)      AS total_salarios,
    MAX(salario)      AS maior_salario,
    MIN(salario)      AS menor_salario
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento
ORDER BY total_salarios DESC;

-- Filtrar grupos com HAVING
SELECT departamento, AVG(salario) AS media
FROM employees
GROUP BY departamento
HAVING AVG(salario) > 7000;
```

---

## Power BI

**Interface:** Transformar → Agrupar Por → selecionar coluna e operação

**DAX — Medidas:**
```dax
Total Salários =
SUM(employees[salario])

Média Salarial =
AVERAGE(employees[salario])

Total por Depto =
CALCULATE(
    SUM(employees[salario]),
    ALLEXCEPT(employees, employees[departamento])
)
```

**Power Query M:**
```powerquery-m
= Table.Group(
    employees,
    {"departamento"},
    {{"total", each List.Sum([salario]), type number},
     {"media", each List.Average([salario]), type number}}
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Relatório executivo por depto | GROUP BY / Tabela Dinâmica |
| Dashboard com filtros | DAX CALCULATE |
| ETL de sumarização | Python groupby / Power Query Group By |

---

## Armadilhas comuns

- `COUNT(*)` conta todas as linhas incluindo nulos; `COUNT(coluna)` ignora nulos
- `HAVING` filtra **depois** do GROUP BY; `WHERE` filtra **antes** — nunca confunda
- No Pandas, `groupby` ignora nulos por padrão — use `dropna=False` para incluí-los

## Veja também
- [Contar Linhas](06-contar-linhas.md)
- [Média Simples](07-media.md)
- [Soma](08-soma.md)
- [Pivot / Unpivot](24-pivot-unpivot.md)
