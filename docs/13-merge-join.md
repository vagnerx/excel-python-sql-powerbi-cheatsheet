# Merge/Join

## Explicação Conceitual
Combinar dados de múltiplas tabelas.

## Excel
- Interface ou fórmula apropriada.
- Exemplo: PROCV/PROCX, SE(), Remover Duplicados.

## Python (Pandas)
```python
pd.merge(df1,df2,on='id')
```

## SQL
```sql
SELECT * FROM a JOIN b ON a.id=b.id;
```

## Power BI
`Mesclar Consultas (M)`

**M:** ETL e transformação.
**DAX:** Medidas e KPIs.

## Quando usar
- Integração.

## Armadilhas comuns
- Cardinalidade incorreta.

## Diferenças entre ferramentas
Excel é visual, Python é programático, SQL opera sobre dados persistidos e Power BI integra ETL e visualização.
