# Ranking

## Explicação Conceitual
Ranking atribui uma posição relativa a cada registro conforme um critério de ordenação.

## Excel
- Fórmula: `=ORDEM(E2;$E$2:$E$9;0)`

## Python (Pandas)
```python
df['rank'] = df['sales'].rank(ascending=False)
```

## SQL
```sql
SELECT name,
       sales,
       RANK() OVER(ORDER BY sales DESC) AS ranking
FROM employees;
```

## Power BI
```DAX
Ranking Vendas =
RANKX(ALL(Employees), SUM(Employees[sales]))
```
**DAX**

## Quando usar
- Ranking de vendedores
- Top clientes
- Classificações

## Armadilhas comuns
- Empates geram posições repetidas.
