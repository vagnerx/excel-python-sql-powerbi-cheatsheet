# Filtrar por Data

## Explicação Conceitual
Restringir períodos.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df[df['hire_date']>'2023-01-01']
```

## SQL
```sql
SELECT * FROM employees WHERE hire_date > '2023-01-01';
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`CALCULATE(..., Date) (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Análise por período.

## Armadilhas comuns
- Formato incorreto.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
