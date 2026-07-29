# 22. Acumulado (Running Total)

> **Tarefa:** Calcular o total acumulado ao longo de uma sequência (tempo ou ordem).  
> **Datasets:** `datasets/employees.csv`, `datasets/orders.csv`

---

## Excel

```excel
=SOMA($F$2:F2)      → soma acumulada (trava o início, solta o fim)
```

**Em Tabela Dinâmica:** Configurações de Campo → Mostrar Valores Como → Total Acumulado Em

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
orders = pd.read_csv("datasets/orders.csv")

# Acumulado de salário (por ordem de id)
df_sorted = df.sort_values("id").copy()
df_sorted["folha_acumulada"] = df_sorted["salario"].cumsum()

# Acumulado de pedidos por data
orders["data_pedido"] = pd.to_datetime(orders["data_pedido"], errors="coerce")
orders_sorted = orders.sort_values("data_pedido").copy()
orders_sorted["valor_acumulado"] = orders_sorted["valor_total"].cumsum()

# Acumulado por grupo (dentro de cada produto)
orders_sorted["acum_por_produto"] = (
    orders_sorted.groupby("id_produto")["valor_total"]
    .cumsum()
)

# Agrupado por mês com acumulado
pedidos_mes = (
    orders_sorted
    .groupby(orders_sorted["data_pedido"].dt.to_period("M"))["valor_total"]
    .sum()
    .reset_index()
)
pedidos_mes.columns = ["mes", "total_mes"]
pedidos_mes["total_acumulado"] = pedidos_mes["total_mes"].cumsum()

print(pedidos_mes.tail(10).to_string(index=False))
```

---

## SQL

```sql
-- Acumulado de salário por id
SELECT nome, salario,
       SUM(salario) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS folha_acumulada
FROM employees
WHERE salario IS NOT NULL;

-- Acumulado de pedidos por data
SELECT id_pedido, data_pedido, valor_total,
       SUM(valor_total) OVER (ORDER BY data_pedido ROWS UNBOUNDED PRECEDING) AS valor_acumulado
FROM orders
ORDER BY data_pedido;

-- Acumulado por grupo (por produto)
SELECT id_pedido, id_produto, valor_total, data_pedido,
       SUM(valor_total) OVER (
           PARTITION BY id_produto
           ORDER BY data_pedido
           ROWS UNBOUNDED PRECEDING
       ) AS acum_por_produto
FROM orders
ORDER BY id_produto, data_pedido;

-- Acumulado mensal
SELECT strftime('%Y-%m', data_pedido) AS mes,
       SUM(valor_total) AS total_mes,
       SUM(SUM(valor_total)) OVER (
           ORDER BY strftime('%Y-%m', data_pedido)
           ROWS UNBOUNDED PRECEDING
       ) AS total_acumulado
FROM orders
GROUP BY mes
ORDER BY mes;
```

---

## Power BI

**DAX:**
```dax
Total Acumulado =
CALCULATE(
    SUM(orders[valor_total]),
    FILTER(
        ALL(orders[data_pedido]),
        orders[data_pedido] <= MAX(orders[data_pedido])
    )
)

-- Com Time Intelligence (requer tabela de datas)
YTD Vendas =
TOTALYTD(
    SUM(orders[valor_total]),
    orders[data_pedido]
)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Evolução da folha no tempo | `cumsum()` / `SUM OVER UNBOUNDED` |
| Gráfico de crescimento acumulado | `YTD` no DAX |
| Acumulado por categoria | `groupby().cumsum()` / `PARTITION BY` |

---

## Armadilhas comuns

- `cumsum()` é sensível à **ordem** das linhas — sempre ordene o DataFrame antes
- `SUM OVER (ORDER BY col)` sem `ROWS UNBOUNDED PRECEDING` pode dar resultados inesperados em versões antigas de SQLite
- No DAX, `TOTALYTD` só funciona com uma **Tabela de Datas** configurada corretamente

## Veja também
- [Soma](08-soma.md)
- [Janela Móvel](23-janela-movel.md)
- [Filtrar por Data](17-filtrar-por-data.md)
