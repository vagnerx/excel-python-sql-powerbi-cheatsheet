# Janela Móvel

## Explicação Conceitual
Calcula métricas sobre um conjunto móvel de registros.

## Excel
Usar MÉDIA com intervalo dinâmico.

## Python
```python
df['media_3'] = df['sales'].rolling(3).mean()
```

## SQL
```sql
AVG(sales) OVER(
  ORDER BY hire_date
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

## Power BI
```DAX
WINDOW(...)
```
**DAX**

## Quando usar
- Médias móveis
- Tendências

## Armadilhas comuns
- Escolher janela inadequada.
