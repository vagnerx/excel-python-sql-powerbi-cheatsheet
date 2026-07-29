# 8. Soma

> **Tarefa:** Somar valores de uma coluna numérica.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=SOMA(F:F)                           → soma todos os salários
=SOMASE(C:C;"Vendas";F:F)           → soma salários de Vendas
=SOMASES(F:F;C:C;"TI";H:H;"Sim")   → soma TI E ativos
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Soma total
total_folha = df["salario"].sum()

# Soma por departamento
soma_depto = df.groupby("departamento")["salario"].sum().sort_values(ascending=False)

# Soma com condição
soma_ativos = df[df["ativo"] == "Sim"]["salario"].sum()

# Soma acumulada (running total)
df_sorted = df.sort_values("data_admissao")
df_sorted["folha_acumulada"] = df_sorted["salario"].cumsum()

# Percentual de cada depto no total
soma_depto_pct = (soma_depto / total_folha * 100).round(1)

print(f"Folha total: R$ {total_folha:,.2f}")
print(f"Folha ativos: R$ {soma_ativos:,.2f}")
print("\nPor departamento:")
print(soma_depto)
```

---

## SQL

```sql
-- Soma total
SELECT SUM(salario) AS folha_total
FROM employees;

-- Soma por departamento
SELECT departamento, SUM(salario) AS total
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento
ORDER BY total DESC;

-- Soma com percentual
SELECT
    departamento,
    SUM(salario) AS total,
    ROUND(SUM(salario) * 100.0 / SUM(SUM(salario)) OVER (), 1) AS pct_folha
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento;

-- Soma acumulada (window function)
SELECT nome, salario,
       SUM(salario) OVER (ORDER BY salario DESC) AS soma_acumulada
FROM employees
WHERE salario IS NOT NULL;
```

---

## Power BI

**DAX:**
```dax
Folha Total =
SUM(employees[salario])

Folha Ativos =
CALCULATE(
    SUM(employees[salario]),
    employees[ativo] = "Sim"
)

% Participação Depto =
DIVIDE(
    SUM(employees[salario]),
    CALCULATE(SUM(employees[salario]), ALL(employees[departamento])),
    0
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Folha de pagamento total | `SUM` simples |
| Participação percentual | `SUM / SUM(ALL)` |
| Evolução no tempo | Soma acumulada / `cumsum()` |

---

## Armadilhas comuns

- `SUM` ignora nulos no SQL e DAX — mas no Python `df["salario"].sum()` também ignora NaN
- Ao calcular percentual no SQL, use `* 1.0` ou `* 100.0` para forçar divisão decimal (SQLite usa integer division)
- No DAX, use `DIVIDE(numerador, denominador, 0)` ao invés de `/` para evitar erro de divisão por zero

## Veja também
- [Média Simples](07-media.md)
- [Agrupar Dados](05-agrupar-agregar.md)
- [Acumulado](22-acumulado.md)
- [Percentual](20-percentual.md)
