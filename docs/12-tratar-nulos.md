# 12. Tratar Valores Vazios (Nulos)

> **Tarefa:** Identificar, preencher ou remover valores nulos/ausentes.  
> **Dataset:** `datasets/employees.csv` (contém nulos intencionais em `departamento`, `cargo`, `salario`, `data_admissao`)

---

## Excel

```excel
=SEERRO(VALOR(F2);0)              → substitui erro por 0
=SE(ÉCÉL.VAZIA(F2);0;F2)         → substitui célula vazia por 0
=SE(F2="";"Sem dado";F2)          → substitui string vazia por texto
=SEERRO(PROCV(A2;tabela;2;0);"") → PROCV sem erros
```

**Power Query:** Transformar → Substituir Valores → Substituir nulos

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Detectar nulos
print(df.isna().sum())
print(f"\nTotal de nulos: {df.isna().sum().sum()}")

# Percentual de nulos por coluna
pct_nulos = (df.isna().sum() / len(df) * 100).round(1)
print(pct_nulos[pct_nulos > 0])

# Preencher nulos com valor fixo
df["salario"] = df["salario"].fillna(0)

# Preencher com média (inputação)
media_salario = df["salario"].mean()
df["salario"] = df["salario"].fillna(media_salario)

# Preencher com valor anterior (forward fill)
df["departamento"] = df["departamento"].ffill()

# Preencher com valor posterior (backward fill)
df["departamento"] = df["departamento"].bfill()

# Preencher string vazia com texto
df["cargo"] = df["cargo"].fillna("Não informado")

# Remover linhas com nulos
df_limpo = df.dropna()

# Remover apenas se nulo em coluna específica
df_sem_nulo_sal = df.dropna(subset=["salario"])

print(df.isna().sum())
```

---

## SQL

```sql
-- Detectar nulos
SELECT
    COUNT(*) - COUNT(salario)       AS nulos_salario,
    COUNT(*) - COUNT(departamento)  AS nulos_depto
FROM employees;

-- Substituir nulo por valor padrão
SELECT nome, COALESCE(salario, 0) AS salario
FROM employees;

-- Substituir nulo por texto
SELECT nome, COALESCE(departamento, 'Não informado') AS depto
FROM employees;

-- Ignorar nulos na agregação
SELECT AVG(salario) AS media      -- AVG já ignora nulos automaticamente
FROM employees;

-- Filtrar apenas registros completos
SELECT * FROM employees
WHERE salario IS NOT NULL
  AND departamento IS NOT NULL;
```

---

## Power BI

**Interface:** Transformar → Substituir Valores → selecione `null` e substitua

**Power Query M:**
```powerquery-m
= Table.ReplaceValue(
    employees,
    null,
    0,
    Replacer.ReplaceValue,
    {"salario"}
)
```

**DAX:**
```dax
Salário Seguro =
IF(ISBLANK(employees[salario]), 0, employees[salario])

-- Ou:
Salário Seguro =
COALESCE(employees[salario], 0)
```

---

## Quando usar?

| Situação | Estratégia |
|---|---|
| Nulo em métrica numérica | `fillna(média)` ou `COALESCE(col, 0)` |
| Nulo em categoria | `fillna("Não informado")` |
| Muitos nulos (> 50%) | Considere remover a coluna |
| Nulo em linha crítica | `dropna(subset=["col"])` |

---

## Armadilhas comuns

- `fillna(0)` pode distorcer médias e somas — prefira inputação pela média ou mediana
- `dropna()` sem `subset` remove a linha se **qualquer** coluna tiver nulo
- No SQL, `WHERE col != ''` não captura `NULL` — use sempre `IS NULL` / `IS NOT NULL`
- No Power BI, `BLANK()` e `0` se comportam diferente em visuais — verifique qual é esperado

## Veja também
- [Tipos de Dados](11-tipos-de-dados.md)
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Importar Dados](01-importar-dados.md)
