# DAX Essentials

## Medidas básicas
```DAX
Total Sales = SUM(Employees[sales])

Average Salary = AVERAGE(Employees[salary])

Employee Count = COUNTROWS(Employees)
```

## Contexto de filtro
```DAX
Sales TI =
CALCULATE(
    [Total Sales],
    Employees[department] = "TI"
)
```

## Ranking
```DAX
Ranking Sales =
RANKX(
    ALL(Employees),
    [Total Sales]
)
```
