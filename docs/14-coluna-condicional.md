# 14. Coluna Condicional

> **Tarefa:** Criar uma nova coluna com valores baseados em condições.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=SE(F2>8000;"Sênior";SE(F2>5000;"Pleno";"Júnior"))
```

**Múltiplas condições:**
```excel
=SE(E(F2>8000;C2="TI");"TI Sênior";"Outros")
```

**SEERRO (evitar erros):**
```excel
=SEERRO(SE(F2>8000;"Sênior";"Júnior");"Sem dados")
```

**IFS (Excel 2016+):**
```excel
=IFS(F2>10000;"Especialista";F2>7000;"Sênior";F2>5000;"Pleno";VERDADEIRO;"Júnior")
```

---

## Python (Pandas)

```python
import pandas as pd
import numpy as np
df = pd.read_csv("datasets/employees.csv")

# Condição simples com np.where
df["nivel"] = np.where(df["salario"] > 8000, "Sênior", "Júnior")

# Múltiplas condições com np.select
condicoes = [
    df["salario"] > 10_000,
    df["salario"] > 7_000,
    df["salario"] > 5_000,
]
valores = ["Especialista", "Sênior", "Pleno"]
df["nivel"] = np.select(condicoes, valores, default="Júnior")

# Usando apply + lambda (mais flexível, mais lento)
def classificar(row):
    if row["salario"] > 8000 and row["departamento"] == "TI":
        return "TI Sênior"
    elif row["salario"] > 8000:
        return "Sênior Outro"
    return "Outros"

df["classificacao"] = df.apply(classificar, axis=1)

# Map — para substituições simples
df["ativo_label"] = df["ativo"].map({"Sim": "Ativo", "Não": "Inativo"})

print(df[["nome", "salario", "nivel", "ativo_label"]].head(10))
```

---

## SQL

```sql
-- CASE WHEN simples
SELECT nome, salario,
    CASE
        WHEN salario > 10000 THEN 'Especialista'
        WHEN salario > 7000  THEN 'Sênior'
        WHEN salario > 5000  THEN 'Pleno'
        ELSE 'Júnior'
    END AS nivel
FROM employees
WHERE salario IS NOT NULL;

-- CASE com múltiplas condições
SELECT nome, departamento, salario,
    CASE
        WHEN salario > 8000 AND departamento = 'TI' THEN 'TI Sênior'
        WHEN salario > 8000 THEN 'Sênior'
        ELSE 'Outros'
    END AS classificacao
FROM employees;

-- CASE em GROUP BY
SELECT
    CASE
        WHEN salario > 8000 THEN 'Alto'
        WHEN salario > 5000 THEN 'Médio'
        ELSE 'Baixo'
    END AS faixa,
    COUNT(*) AS total,
    ROUND(AVG(salario), 2) AS media
FROM employees
WHERE salario IS NOT NULL
GROUP BY faixa;
```

---

## Power BI

**Interface:** Adicionar Coluna → Coluna Condicional (wizard visual)

**DAX — Coluna calculada:**
```dax
Nível =
IF(
    employees[salario] > 10000, "Especialista",
    IF(employees[salario] > 7000, "Sênior",
    IF(employees[salario] > 5000, "Pleno", "Júnior"))
)
```

**DAX com SWITCH (mais legível):**
```dax
Nível =
SWITCH(
    TRUE(),
    employees[salario] > 10000, "Especialista",
    employees[salario] > 7000,  "Sênior",
    employees[salario] > 5000,  "Pleno",
    "Júnior"
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Classificação simples (2 valores) | `np.where` / `SE()` |
| Múltiplas categorias | `np.select` / `CASE WHEN` / `SWITCH(TRUE())` |
| Lógica complexa por linha | `apply(lambda)` |

---

## Armadilhas comuns

- `apply()` é conveniente mas lento para grandes volumes — prefira `np.select` quando possível
- No SQL, `CASE WHEN` avalia as condições **em ordem** — coloque as mais específicas primeiro
- No DAX, `IF` aninhado fica difícil de ler — prefira `SWITCH(TRUE())` para mais de 2 condições

## Veja também
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Ranking](21-ranking.md)
- [Agrupar Dados](05-agrupar-agregar.md)
