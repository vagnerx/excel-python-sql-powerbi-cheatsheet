# 6. Contar Linhas

> **Tarefa:** Saber quantos registros existem na tabela ou em um grupo.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=CONT.VALORES(A:A)-1          → conta células não vazias (menos o cabeçalho)
=CONT.SE(C:C;"TI")            → conta funcionários do depto TI
=CONT.SES(C:C;"TI";H:H;"Sim") → conta TI E ativos (múltiplas condições)
=CONTAR.VAZIO(F:F)            → conta células vazias (nulos)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Total de linhas
total = len(df)

# Total de linhas (forma alternativa)
total2 = df.shape[0]

# Contar por coluna (ignora nulos)
contagem = df["salario"].count()

# Contar por grupo
por_depto = df.groupby("departamento")["id"].count()

# Contar com condição
ativos = (df["ativo"] == "Sim").sum()

# Contar nulos
nulos_salario = df["salario"].isna().sum()

print(f"Total: {total}")
print(f"Ativos: {ativos}")
print(f"Nulos em salario: {nulos_salario}")
print(por_depto)
```

---

## SQL

```sql
-- Contar todas as linhas
SELECT COUNT(*) AS total FROM employees;

-- Contar sem nulos em salario
SELECT COUNT(salario) AS com_salario FROM employees;

-- Contar por departamento
SELECT departamento, COUNT(*) AS total
FROM employees
GROUP BY departamento
ORDER BY total DESC;

-- Contar com condição
SELECT COUNT(*) AS ativos
FROM employees
WHERE ativo = 'Sim';

-- Contar nulos
SELECT COUNT(*) - COUNT(salario) AS salarios_nulos
FROM employees;
```

---

## Power BI

**DAX:**
```dax
Total Funcionários =
COUNTROWS(employees)

Funcionários Ativos =
CALCULATE(
    COUNTROWS(employees),
    employees[ativo] = "Sim"
)

Qtd TI =
CALCULATE(
    COUNTROWS(employees),
    employees[departamento] = "TI"
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Validar integridade dos dados | `COUNT(*)` vs `COUNT(coluna)` |
| KPI de headcount | `COUNTROWS` no DAX |
| Análise de completude (nulos) | `isna().sum()` / `COUNT(*) - COUNT(col)` |

---

## Armadilhas comuns

- `COUNT(*)` ≠ `COUNT(coluna)` — o primeiro conta tudo, o segundo ignora nulos
- `len(df)` conta todas as linhas incluindo nulos; `df["col"].count()` ignora nulos
- No DAX, `COUNTROWS` e `COUNT` se comportam diferente em contextos de filtro

## Veja também
- [Agrupar Dados](05-agrupar-agregar.md)
- [Tratar Nulos](12-tratar-nulos.md)
- [Contar Valores Únicos](18-contar-unicos.md)
