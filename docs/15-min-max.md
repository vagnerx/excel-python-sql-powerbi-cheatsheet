# 15. Min / Max

> **Tarefa:** Encontrar o menor ou maior valor de uma coluna.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
=MÍNIMO(F:F)                        → menor salário
=MÁXIMO(F:F)                        → maior salário
=MÍNIMOSES(F:F;C:C;"TI")           → menor salário do depto TI
=MÁXIMOSES(F:F;C:C;"TI")           → maior salário do depto TI
```

**Identificar o funcionário com maior salário:**
```excel
=ÍNDICE(B:B;CORRESP(MÁXIMO(F:F);F:F;0))   → nome do maior salário
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Min e Max gerais
sal_min = df["salario"].min()
sal_max = df["salario"].max()
print(f"Menor: R$ {sal_min:,.2f} | Maior: R$ {sal_max:,.2f}")

# Min/Max por grupo
resumo = df.groupby("departamento")["salario"].agg(["min", "max"])

# Linha com o maior salário
linha_max = df.loc[df["salario"].idxmax()]
print(f"\nMaior salário: {linha_max['nome']} — R$ {linha_max['salario']:,.2f}")

# Linha com o menor salário
linha_min = df.loc[df["salario"].idxmin()]

# Top N maiores
top3 = df.nlargest(3, "salario")[["nome", "departamento", "salario"]]
print("\nTop 3 salários:")
print(top3)

# Bottom N menores
bottom3 = df.nsmallest(3, "salario")[["nome", "departamento", "salario"]]
```

---

## SQL

```sql
-- Min e Max simples
SELECT MIN(salario) AS menor, MAX(salario) AS maior
FROM employees
WHERE salario IS NOT NULL;

-- Min/Max por departamento
SELECT departamento,
       MIN(salario) AS menor,
       MAX(salario) AS maior,
       MAX(salario) - MIN(salario) AS amplitude
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento;

-- Nome do funcionário com maior salário
SELECT nome, departamento, salario
FROM employees
WHERE salario = (SELECT MAX(salario) FROM employees);

-- Top 1 por departamento (Window Function)
SELECT nome, departamento, salario
FROM (
    SELECT nome, departamento, salario,
           RANK() OVER (PARTITION BY departamento ORDER BY salario DESC) AS rnk
    FROM employees
    WHERE salario IS NOT NULL
)
WHERE rnk = 1;
```

---

## Power BI

**DAX:**
```dax
Menor Salário = MIN(employees[salario])
Maior Salário = MAX(employees[salario])

Amplitude Salarial =
MAX(employees[salario]) - MIN(employees[salario])

Funcionário Top Salário =
CALCULATE(
    FIRSTNONBLANK(employees[nome], 1),
    TOPN(1, employees, employees[salario], DESC)
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Validar intervalo de dados | `min()` + `max()` / `MIN` + `MAX` |
| Encontrar o registro extremo | `idxmax()` + `loc` / subquery |
| Min/Max por categoria | `groupby().agg(["min","max"])` / `MIN OVER PARTITION BY` |

---

## Armadilhas comuns

- `min()` e `max()` em strings ordenam **alfabeticamente** — verifique o tipo da coluna
- No SQL, `MIN/MAX` ignoram nulos — mas o resultado pode ser inesperado se todos forem nulos
- `idxmax()` retorna o **índice** da linha, não o valor — use `.loc[df["col"].idxmax()]` para acessar a linha

## Veja também
- [Top N Registros](19-top-n.md)
- [Ranking](21-ranking.md)
- [Agrupar Dados](05-agrupar-agregar.md)
