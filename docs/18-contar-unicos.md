# 18. Contar Valores Únicos

> **Tarefa:** Contar quantos valores distintos existem em uma coluna.  
> **Dataset:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

```excel
=CONT.SE(C:C;"<>")                → conta células não vazias
=SOMARPRODUTO(1/CONT.SE(C2:C52;C2:C52))   → conta únicos (fórmula matricial clássica)
=CONT.VALORES(ÚNICO(C2:C52))      → conta únicos (Excel 365)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# Contar únicos em uma coluna
qtd_deptos = df["departamento"].nunique()
qtd_cargos = df["cargo"].nunique()

# Contar únicos ignorando nulos (padrão)
qtd_deptos_sem_nulo = df["departamento"].nunique(dropna=True)

# Contar únicos incluindo nulos
qtd_deptos_com_nulo = df["departamento"].nunique(dropna=False)

# Contar únicos por grupo
unicos_por_depto = df.groupby("departamento")["cargo"].nunique()

# Clientes únicos que fizeram pedidos
clientes_compraram = orders["id_cliente"].nunique()

print(f"Departamentos únicos: {qtd_deptos}")
print(f"Cargos únicos: {qtd_cargos}")
print(f"Clientes com pedidos: {clientes_compraram}")
print("\nCargos únicos por depto:")
print(unicos_por_depto)
```

---

## SQL

```sql
-- Contar valores únicos
SELECT COUNT(DISTINCT departamento) AS deptos_unicos
FROM employees;

-- Múltiplas colunas
SELECT
    COUNT(DISTINCT departamento) AS deptos,
    COUNT(DISTINCT cargo)        AS cargos,
    COUNT(DISTINCT cidade)       AS cidades
FROM employees;

-- Distintos por grupo
SELECT departamento, COUNT(DISTINCT cargo) AS cargos_unicos
FROM employees
GROUP BY departamento
ORDER BY cargos_unicos DESC;

-- Clientes únicos com pedidos
SELECT COUNT(DISTINCT id_cliente) AS clientes_ativos
FROM orders;

-- Clientes que NÃO fizeram pedidos
SELECT COUNT(*) AS sem_pedido
FROM customers
WHERE id_cliente NOT IN (SELECT DISTINCT id_cliente FROM orders);
```

---

## Power BI

**DAX:**
```dax
Qtd Departamentos =
DISTINCTCOUNT(employees[departamento])

Qtd Clientes Ativos =
DISTINCTCOUNT(orders[id_cliente])

Cargos por Depto =
CALCULATE(
    DISTINCTCOUNT(employees[cargo]),
    ALLEXCEPT(employees, employees[departamento])
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Validar diversidade de dados | `nunique()` / `COUNT(DISTINCT)` |
| KPI de clientes únicos | `DISTINCTCOUNT` no DAX |
| Detectar cardinalidade de coluna | `nunique()` para decidir tipo (category vs text) |

---

## Armadilhas comuns

- `COUNT(DISTINCT col)` **ignora nulos** — use `nunique(dropna=False)` no Python se quiser contá-los
- `COUNT(*)` e `COUNT(DISTINCT col)` são conceitos diferentes — nunca os confunda
- Alta cardinalidade (muitos únicos) em uma coluna de texto no Power BI impacta performance

## Veja também
- [Obter Valores Únicos](09-obter-valores-unicos.md)
- [Contar Linhas](06-contar-linhas.md)
- [Merge / Join](13-merge-join.md)
