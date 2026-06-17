# Acumulado

## Explicação Conceitual
Calcula totais progressivos ao longo do tempo.

## Excel
Soma acumulada usando referências absolutas:
`=SOMA($G$2:G2)`

## Python
```python
df['acumulado'] = df['sales'].cumsum()
```

## SQL
```sql
SELECT *,
       SUM(sales) OVER(
           ORDER BY hire_date
       ) acumulado
FROM employees;
```

## Power BI
```DAX
Vendas Acumuladas =
TOTALYTD(
    SUM(Employees[sales]),
    Employees[hire_date]
)
```
**DAX**

## Armadilhas comuns
- Calendário incorreto no Power BI.
