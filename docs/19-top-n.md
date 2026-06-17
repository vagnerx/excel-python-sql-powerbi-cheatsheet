# Top N

## Explicação Conceitual
Retornar maiores valores.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df.nlargest(5,'sales')
```

## SQL
```sql
SELECT * FROM employees ORDER BY sales DESC LIMIT 5;
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`TOPN() (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Rankings.

## Armadilhas comuns
- Empates.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
