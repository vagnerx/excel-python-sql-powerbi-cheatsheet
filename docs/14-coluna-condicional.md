# Coluna Condicional

## Explicação Conceitual
Criar regras de negócio.

## Excel
- Interface ou fórmula apropriada.
- Exemplo: PROCV/PROCX, SE(), Remover Duplicados.

## Python (Pandas)
```python
np.where(df['salary']>6000,'Senior','Junior')
```

## SQL
```sql
CASE WHEN salary>6000 THEN 'Senior' END
```

## Power BI
`IF() (DAX)`

**M:** ETL e transformação.
**DAX:** Medidas e KPIs.

## Quando usar
- Classificações.

## Armadilhas comuns
- Condições sobrepostas.

## Diferenças entre ferramentas
Excel é visual, Python é programático, SQL opera sobre dados persistidos e Power BI integra ETL e visualização.
