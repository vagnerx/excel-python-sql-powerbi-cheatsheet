# 2. Filtrar Linhas

> **Tarefa:** Selecionar apenas registros que atendem a uma condição.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Interface:** Dados → Filtro → Filtro Automático na coluna desejada

**Filtro avançado com fórmula (coluna auxiliar):**
```excel
=SE(F2>5000;"Acima da média";"Abaixo da média")
```

**Filtro com FILTRAR (Excel 365):**
```excel
=FILTRAR(A2:H52; F2:F52 > 5000)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Filtro simples — salário acima de 5000
df_sênior = df[df["salario"] > 5000]

# Filtro com múltiplas condições (E)
df_ti_senior = df[(df["departamento"] == "TI") & (df["salario"] > 8000)]

# Filtro com múltiplas condições (OU)
df_ti_ou_rh = df[(df["departamento"] == "TI") | (df["departamento"] == "RH")]

# Filtro com lista (isin)
deps = ["TI", "Financeiro", "Marketing"]
df_selecionados = df[df["departamento"].isin(deps)]

# Filtro com string — nome que contém "a"
df_nomes = df[df["nome"].str.contains("a", case=False, na=False)]

print(f"Funcionários com salário > 5000: {len(df_sênior)}")
```

---

## SQL

```sql
-- Filtro simples
SELECT * FROM employees
WHERE salario > 5000;

-- Filtro com múltiplas condições
SELECT * FROM employees
WHERE departamento = 'TI'
  AND salario > 8000;

-- Filtro com lista
SELECT * FROM employees
WHERE departamento IN ('TI', 'Financeiro', 'Marketing');

-- Filtro com texto parcial
SELECT * FROM employees
WHERE nome LIKE '%ana%';

-- Filtro com nulos
SELECT * FROM employees
WHERE salario IS NULL;

SELECT * FROM employees
WHERE salario IS NOT NULL;
```

---

## Power BI

**Interface:** Transformar Dados → Filtrar Linhas (botão na coluna)

**DAX — Medida condicional:**
```dax
Total Sênior =
CALCULATE(
    COUNTROWS(employees),
    employees[salario] > 5000
)
```

**Power Query M:**
```powerquery-m
= Table.SelectRows(employees, each [salario] > 5000)
```

---

## Quando usar?

| Cenário | Ferramenta |
|---|---|
| Análise exploratória rápida | Excel ou Python |
| Consulta em banco de dados | SQL |
| Filtro em dashboard | Power BI (DAX) |
| ETL / Preparação de dados | Python ou Power Query M |

---

## Armadilhas comuns

- **Nulos:** `df[df["salario"] > 5000]` ignora nulos automaticamente no Pandas; no SQL use `IS NOT NULL`
- **Tipos:** comparar string com número gera erro — valide com `df.dtypes`
- **Case sensitive:** `str.contains` é case-sensitive por padrão; use `case=False`

## Veja também
- [Selecionar Colunas](03-selecionar-colunas.md)
- [Tratar Nulos](12-tratar-nulos.md)
- [Coluna Condicional](14-coluna-condicional.md)
