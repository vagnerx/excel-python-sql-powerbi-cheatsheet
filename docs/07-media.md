# 7. Média Simples

> **Tarefa:** Calcular o valor médio de uma coluna numérica.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=MÉDIA(F:F)                         → média de todos os salários
=MÉDIASE(C:C;"TI";F:F)             → média salarial do depto TI
=MÉDIASES(F:F;C:C;"Vendas";H:H;"Sim")  → média de Vendas E ativos
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Média geral
media_geral = df["salario"].mean()

# Média por grupo
media_por_depto = df.groupby("departamento")["salario"].mean().round(2)

# Média condicional
media_ativos = df[df["ativo"] == "Sim"]["salario"].mean()

# Média por múltiplos grupos
media_depto_ativo = df.groupby(["departamento", "ativo"])["salario"].mean()

# Estatísticas completas
print(df["salario"].describe())
print(f"\nMédia geral: R$ {media_geral:,.2f}")
print(f"Média ativos: R$ {media_ativos:,.2f}")
print("\nMédia por departamento:")
print(media_por_depto)
```

---

## SQL

```sql
-- Média geral
SELECT AVG(salario) AS media_salarial
FROM employees;

-- Média por departamento
SELECT departamento, ROUND(AVG(salario), 2) AS media
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento
ORDER BY media DESC;

-- Média condicional
SELECT
    AVG(CASE WHEN departamento = 'TI' THEN salario END)      AS media_ti,
    AVG(CASE WHEN departamento = 'Vendas' THEN salario END)  AS media_vendas
FROM employees;

-- Comparar com a média geral
SELECT nome, departamento, salario,
       ROUND(AVG(salario) OVER (), 2) AS media_geral,
       salario - AVG(salario) OVER () AS diferenca_media
FROM employees
WHERE salario IS NOT NULL;
```

---

## Power BI

**DAX:**
```dax
Média Salarial =
AVERAGE(employees[salario])

Média por Depto =
AVERAGEX(
    VALUES(employees[departamento]),
    CALCULATE(AVERAGE(employees[salario]))
)

Desvio da Média =
employees[salario] - [Média Salarial]
```

---

## Quando usar?

| Cenário | Observação |
|---|---|
| Tendência central | Média é sensível a outliers |
| Comparar com mediana | Se média >> mediana, há outliers altos |
| KPI executivo | Média por equipe/período |

---

## Armadilhas comuns

- **Outliers distorcem a média** — considere usar mediana (`df["salario"].median()`)
- `AVG` no SQL ignora nulos automaticamente — `AVERAGE` no DAX também
- No Python, `df["salario"].mean()` também ignora nulos (comportamento padrão do Pandas)

## Veja também
- [Soma](08-soma.md)
- [Agrupar Dados](05-agrupar-agregar.md)
- [Min / Max](15-min-max.md)
