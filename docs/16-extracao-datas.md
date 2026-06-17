# Extração de Datas

## Explicação Conceitual
Extrair componentes temporais.

## Excel
- Fórmulas como MÍNIMO(), MÁXIMO(), ANO(), MÊS().
- Filtros e segmentações de data.

## Python
```python
df['hire_date'].dt.year
```

## SQL
```sql
SELECT YEAR(hire_date) FROM employees;
```

Compatível com PostgreSQL (ajustes de função podem ser necessários).

## Power BI
`YEAR() / MONTH() (DAX)`

- **M**: transformação.
- **DAX**: análise.

## Quando usar
- Análise temporal.

## Armadilhas comuns
- Problemas de timezone.

## Veja também
- Ranking
- Acumulado
- Janela Móvel
