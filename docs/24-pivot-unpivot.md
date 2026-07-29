# 24. Pivot / Unpivot

> **Tarefa:** Transformar linhas em colunas (pivot) ou colunas em linhas (unpivot).  
> **Datasets:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

**Pivot → Tabela Dinâmica:**
```
Inserir → Tabela Dinâmica
- Linhas: departamento
- Colunas: ativo
- Valores: Soma de salario
```

**Unpivot no Power Query:**
```
Selecionar colunas → Transformar → Remover Dinâmica de Outras Colunas
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# ── PIVOT ──────────────────────────────────────────────
# pivot_table: equivalente à Tabela Dinâmica
pivot = df.pivot_table(
    values="salario",
    index="departamento",
    columns="ativo",
    aggfunc="mean",
    fill_value=0
).round(2)

print("Salário médio por depto e status:")
print(pivot)

# pivot com múltiplas métricas
pivot_multi = df.pivot_table(
    values="salario",
    index="departamento",
    aggfunc=["mean", "count", "sum"]
).round(2)

# pivot simples (sem agregação — dados únicos por chave)
# Requer que combinação index+columns seja única
try:
    pivot_simples = df.pivot(index="id", columns="ativo", values="salario")
except ValueError as e:
    print(f"Erro: {e}")

# ── UNPIVOT (melt) ────────────────────────────────────
# Transformar colunas em linhas
df_wide = pivot_multi.reset_index()

# Exemplo: orders com valor_unit e valor_total → formato longo
orders_long = orders.melt(
    id_vars=["id_pedido", "id_cliente", "id_produto", "data_pedido"],
    value_vars=["valor_unit", "valor_total"],
    var_name="tipo_valor",
    value_name="valor"
)

print("\nOrders em formato longo:")
print(orders_long.head(6).to_string(index=False))
```

---

## SQL

```sql
-- PIVOT manual com CASE WHEN (SQLite não tem PIVOT nativo)
SELECT departamento,
       ROUND(AVG(CASE WHEN ativo = 'Sim' THEN salario END), 2) AS media_ativos,
       ROUND(AVG(CASE WHEN ativo = 'Não' THEN salario END), 2) AS media_inativos,
       COUNT(*) AS total
FROM employees
WHERE salario IS NOT NULL
GROUP BY departamento
ORDER BY departamento;

-- UNPIVOT manual com UNION ALL
SELECT id_pedido, id_produto, 'valor_unit'  AS tipo, valor_unit  AS valor FROM orders
UNION ALL
SELECT id_pedido, id_produto, 'valor_total' AS tipo, valor_total AS valor FROM orders
ORDER BY id_pedido, tipo;
```

> 💡 PostgreSQL e SQL Server têm operadores `PIVOT` / `UNPIVOT` nativos.

---

## Power BI

**Pivot — Power Query M:**
```powerquery-m
= Table.Pivot(
    tabela,
    List.Distinct(tabela[ativo]),
    "ativo",
    "salario",
    List.Average
)
```

**Unpivot — Power Query M:**
```powerquery-m
= Table.UnpivotOtherColumns(
    tabela,
    {"id_pedido", "id_produto"},
    "Tipo Valor",
    "Valor"
)
```

**DAX — Tabela Pivotada:**
```dax
Pivot por Depto =
SUMMARIZECOLUMNS(
    employees[departamento],
    employees[ativo],
    "Media Salario", AVERAGE(employees[salario])
)
```

---

## Quando usar?

| Operação | Cenário |
|---|---|
| Pivot | Criar visão cruzada (depto × ativo × métrica) |
| Unpivot | Normalizar dados "wide" para análise |
| Ambos | Reformatar dados vindos de planilhas legadas |

---

## Armadilhas comuns

- `pivot()` falha se houver duplicatas na combinação `index + columns` — use `pivot_table()` que agrega
- `melt()` pode criar muitas linhas — certifique-se de que `id_vars` identifica unicamente cada linha
- No Power BI, **unpivot antes de modelar** — é muito mais fácil do que tentar corrigir depois no DAX

## Veja também
- [Agrupar Dados](05-agrupar-agregar.md)
- [Merge / Join](13-merge-join.md)
- [Renomear Colunas](10-renomear-colunas.md)
