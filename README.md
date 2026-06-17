# Excel → Python → SQL → Power BI Cheat Sheet

## Índice
1. Importar Dados
2. Filtrar Linhas
3. Selecionar Colunas
4. Ordenar Dados
5. Agrupar Dados
6. Obter Valores Únicos
7. Merge / Join
8. Coluna Condicional
9. Datas
10. Ranking
11. Acumulado
12. Pivot / Unpivot

## Dataset
Use o arquivo `datasets/employees.csv`.

## Exemplo: Filtrar salário > 5000

### Excel
Use filtro na coluna salário.

### Python
```python
df[df['salario'] > 5000]
```

### SQL
```sql
SELECT * FROM employees
WHERE salario > 5000;
```

### Power BI (DAX)
```DAX
SalariosAltos =
CALCULATE(COUNTROWS(Employees), Employees[salario] > 5000)
```

## Power BI: quando usar M vs DAX
- M: ETL e transformação.
- DAX: métricas e análise.
