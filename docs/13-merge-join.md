# 13. Merge / Join

> **Tarefa:** Combinar dados de duas ou mais tabelas usando uma chave comum.  
> **Datasets:** `datasets/employees.csv`, `datasets/customers.csv`, `datasets/orders.csv`

---

## Excel

**PROCV (clássico):**
```excel
=PROCV(A2;customers!$A:$E;3;0)   → busca cidade do cliente pelo id
```

**PROCX (moderno — Excel 365):**
```excel
=PROCX(B2;orders!$B:$B;customers!$C:$C;"Não encontrado")
```

**Índice + Corresp (flexível):**
```excel
=ÍNDICE(customers!$C:$C;CORRESP(B2;customers!$A:$A;0))
```

**Power Query:** Página Inicial → Mesclar Consultas → selecionar tipo de Join

---

## Python (Pandas)

```python
import pandas as pd

emp = pd.read_csv("datasets/employees.csv")
cust = pd.read_csv("datasets/customers.csv")
orders = pd.read_csv("datasets/orders.csv")

# INNER JOIN — apenas correspondências
inner = pd.merge(orders, cust, on="id_cliente", how="inner")

# LEFT JOIN — todos os pedidos, mesmo sem cliente
left = pd.merge(orders, cust, on="id_cliente", how="left")

# RIGHT JOIN
right = pd.merge(orders, cust, on="id_cliente", how="right")

# OUTER JOIN — todos os registros de ambas
outer = pd.merge(orders, cust, on="id_cliente", how="outer")

# Join com colunas de nome diferente
merged = pd.merge(
    orders,
    cust,
    left_on="id_cliente",
    right_on="id_cliente",
    suffixes=("_pedido", "_cliente")
)

# Múltiplos joins em cadeia
full = (
    orders
    .merge(cust, on="id_cliente", how="left")
)

print(f"Pedidos total: {len(orders)}")
print(f"Após INNER JOIN com clientes: {len(inner)}")
print(inner[["id_pedido","nome","cidade","valor_total"]].head())
```

---

## SQL

```sql
-- INNER JOIN (apenas correspondências)
SELECT o.id_pedido, c.nome, c.cidade, o.valor_total
FROM orders o
INNER JOIN customers c ON o.id_cliente = c.id_cliente;

-- LEFT JOIN (todos os pedidos)
SELECT o.id_pedido, c.nome, o.valor_total
FROM orders o
LEFT JOIN customers c ON o.id_cliente = c.id_cliente;

-- Múltiplas tabelas
SELECT o.id_pedido, c.nome AS cliente, o.valor_total, o.data_pedido
FROM orders o
LEFT JOIN customers c ON o.id_cliente = c.id_cliente
ORDER BY o.valor_total DESC;

-- Contar pedidos por cliente
SELECT c.nome, COUNT(o.id_pedido) AS qtd_pedidos, SUM(o.valor_total) AS total
FROM customers c
LEFT JOIN orders o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nome
ORDER BY total DESC NULLS LAST;
```

---

## Power BI

**Interface:** Transformar → Mesclar Consultas → escolher Join Kind

**Power Query M:**
```powerquery-m
= Table.NestedJoin(
    orders, "id_cliente",
    customers, "id_cliente",
    "DadosCliente",
    JoinKind.LeftOuter
)
```

**DAX — RELATED (via relacionamento de modelo):**
```dax
-- Criar relacionamento no modelo e usar:
Cidade Cliente = RELATED(customers[cidade])

Total por Cliente =
SUMMARIZE(
    orders,
    customers[nome],
    "Total", SUM(orders[valor_total])
)
```

---

## Tipos de Join

| Tipo | Resultado | Uso |
|---|---|---|
| INNER | Apenas linhas com match em ambas | Dados completos |
| LEFT | Todos da esquerda + match da direita | Análise de ausência |
| RIGHT | Match da esquerda + todos da direita | Menos comum |
| OUTER/FULL | Todos de ambas | Comparação completa |

---

## Armadilhas comuns

- **Cardinalidade errada:** JOIN pode multiplicar linhas se a chave não for única na tabela de referência
- **Colunas com mesmo nome:** use `suffixes=` no Pandas para diferenciar
- No Power BI, **prefira relacionamentos no modelo** a JOINs no Power Query M — é mais eficiente
- `LEFT JOIN` com `WHERE tabela_direita.col IS NOT NULL` vira um INNER JOIN implicitamente

## Veja também
- [Selecionar Colunas](03-selecionar-colunas.md)
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Agrupar Dados](05-agrupar-agregar.md)
