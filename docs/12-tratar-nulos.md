# Tratar Nulos

## Explicação Conceitual
Lidar com dados ausentes.

## Excel
- Interface ou fórmula apropriada.
- Exemplo: PROCV/PROCX, SE(), Remover Duplicados.

## Python (Pandas)
```python
df.fillna(0)
```

## SQL
```sql
COALESCE(salary,0)
```

## Power BI
`COALESCE() (DAX)`

**M:** ETL e transformação.
**DAX:** Medidas e KPIs.

## Quando usar
- Qualidade.

## Armadilhas comuns
- Substituir sem regra.

## Diferenças entre ferramentas
Excel é visual, Python é programático, SQL opera sobre dados persistidos e Power BI integra ETL e visualização.
