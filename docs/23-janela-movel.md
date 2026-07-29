# 23. Janela Móvel (Rolling Window)

> **Tarefa:** Calcular médias, somas ou outras métricas em janelas deslizantes de N períodos.  
> **Dataset:** `datasets/orders.csv` — agregado por data

---

## Excel

Não há função nativa de janela móvel, mas pode-se usar:

```excel
=MÉDIA(F2:F8)     → média dos últimos 7 dias (fixada manualmente)
```

**Com intervalo dinâmico:**
```excel
=MÉDIA(DESLOCAMENTO(F2;-6;0;7;1))   → média móvel de 7 períodos
```

---

## Python (Pandas)

```python
import pandas as pd

orders = pd.read_csv("datasets/orders.csv")
orders["data_pedido"] = pd.to_datetime(orders["data_pedido"], errors="coerce")

# Agregar por dia
diario = (
    orders
    .groupby("data_pedido")["valor_total"]
    .sum()
    .reset_index()
    .sort_values("data_pedido")
)

# Média móvel de 7 dias
diario["media_7d"] = diario["valor_total"].rolling(window=7).mean().round(2)

# Soma móvel de 7 dias
diario["soma_7d"] = diario["valor_total"].rolling(window=7).sum().round(2)

# Máximo móvel de 30 dias
diario["max_30d"] = diario["valor_total"].rolling(window=30).max()

# Min períodos: calcular mesmo com menos de N observações
diario["media_7d_incompleta"] = diario["valor_total"].rolling(window=7, min_periods=1).mean()

# Janela por tempo (ex: últimos 7 dias a partir da data)
diario = diario.set_index("data_pedido")
diario["media_7d_tempo"] = diario["valor_total"].rolling("7D").mean().round(2)

print(diario[["valor_total","media_7d","soma_7d"]].tail(15).to_string())
```

---

## SQL

```sql
-- Média móvel de 7 linhas anteriores (SQL Window Function)
SELECT data_pedido, valor_total,
       ROUND(
           AVG(valor_total) OVER (
               ORDER BY data_pedido
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ), 2
       ) AS media_movel_7d
FROM (
    SELECT data_pedido, SUM(valor_total) AS valor_total
    FROM orders
    GROUP BY data_pedido
)
ORDER BY data_pedido;

-- Soma móvel de 7 dias
SELECT data_pedido, valor_total,
       SUM(valor_total) OVER (
           ORDER BY data_pedido
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS soma_movel_7d
FROM (
    SELECT data_pedido, SUM(valor_total) AS valor_total
    FROM orders
    GROUP BY data_pedido
)
ORDER BY data_pedido;

-- Média por grupo (por produto) janela de 3
SELECT id_produto, data_pedido, valor_total,
       ROUND(AVG(valor_total) OVER (
           PARTITION BY id_produto
           ORDER BY data_pedido
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 2) AS media_movel_3d
FROM orders
ORDER BY id_produto, data_pedido;
```

---

## Power BI

**DAX:**
```dax
Média Móvel 7 Dias =
VAR UltimaData = MAX(orders[data_pedido])
RETURN
CALCULATE(
    AVERAGE(orders[valor_total]),
    DATESINPERIOD(
        orders[data_pedido],
        UltimaData,
        -7,
        DAY
    )
)

Média Móvel 30 Dias =
CALCULATE(
    AVERAGE(orders[valor_total]),
    DATESINPERIOD(orders[data_pedido], MAX(orders[data_pedido]), -30, DAY)
)
```

---

## Quando usar?

| Cenário | Window |
|---|---|
| Suavizar ruído diário | Média móvel 7 dias |
| Tendência de longo prazo | Média móvel 30 ou 90 dias |
| Comparar pico vs. baseline | Max / Min móvel |

---

## Armadilhas comuns

- Os primeiros N-1 valores da janela serão `NaN` — use `min_periods=1` para evitar ou trate após
- `rolling("7D")` exige que o índice seja `DatetimeIndex` — converta antes com `.set_index()`
- No DAX, `DATESINPERIOD` requer uma **Tabela de Datas** para funcionar corretamente em todos os cenários

## Veja também
- [Acumulado](22-acumulado.md)
- [Filtrar por Data](17-filtrar-por-data.md)
- [Extração de Datas](16-extracao-datas.md)
