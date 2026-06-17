# Min / Max

## Explicação Conceitual
Identificar valores extremos.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df['salary'].min(); df['salary'].max()
```

## SQL
```sql
SELECT MIN(salary), MAX(salary) FROM employees;
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`MIN()/MAX() (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Análise exploratória.

## Armadilhas comuns
- Ignorar outliers.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
