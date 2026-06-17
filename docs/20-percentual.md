# Percentual

## Explicação Conceitual
Calcular participação.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df['pct']=df['sales']/df['sales'].sum()
```

## SQL
```sql
SUM(sales)/SUM(total)
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`DIVIDE() (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Participação relativa.

## Armadilhas comuns
- Divisão por zero.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
