# Tipos de Dados

## Explicação Conceitual
Garantir integridade dos dados.

## Excel
- Interface ou fórmula apropriada.
- Exemplo: PROCV/PROCX, SE(), Remover Duplicados.

## Python (Pandas)
```python
df['salary'].astype(float)
```

## SQL
```sql
CAST(salary AS NUMERIC)
```

## Power BI
`Alterar Tipo (M)`

**M:** ETL e transformação.
**DAX:** Medidas e KPIs.

## Quando usar
- Evitar erros.

## Armadilhas comuns
- Conversões inválidas.

## Diferenças entre ferramentas
Excel é visual, Python é programático, SQL opera sobre dados persistidos e Power BI integra ETL e visualização.
