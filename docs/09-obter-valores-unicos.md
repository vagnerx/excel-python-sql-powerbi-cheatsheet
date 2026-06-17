# Obter Valores Únicos

## Explicação Conceitual
Identificar registros únicos sem duplicidades.

## Excel
- Interface ou fórmula apropriada.
- Exemplo: PROCV/PROCX, SE(), Remover Duplicados.

## Python (Pandas)
```python
df.drop_duplicates()
```

## SQL
```sql
SELECT DISTINCT department FROM employees;
```

## Power BI
`Remover Duplicados (M)`

**M:** ETL e transformação.
**DAX:** Medidas e KPIs.

## Quando usar
- Deduplicação e qualidade.

## Armadilhas comuns
- DISTINCT não remove fisicamente no SQL.

## Diferenças entre ferramentas
Excel é visual, Python é programático, SQL opera sobre dados persistidos e Power BI integra ETL e visualização.
