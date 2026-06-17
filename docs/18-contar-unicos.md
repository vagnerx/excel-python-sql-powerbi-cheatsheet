# Contar Únicos

## Explicação Conceitual
Medir cardinalidade.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df['department'].nunique()
```

## SQL
```sql
SELECT COUNT(DISTINCT department) FROM employees;
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`DISTINCTCOUNT() (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Clientes únicos.

## Armadilhas comuns
- Nulos afetam contagem.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
