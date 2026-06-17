# Contar Linhas

## Explicação Conceitual
Medir volume de registros.

## Dataset Utilizado
`datasets/employees.csv`

## Excel
**Interface:** Dados → Filtro/Classificar/Tabela Dinâmica

**Exemplo PT-BR:**
- Soma: `=SOMA(G:G)`
- Média: `=MÉDIA(E:E)`
- Contagem: `=CONT.VALORES(A:A)`

## Python (Pandas)
```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
resultado = len(df)
print(resultado)
```

## SQL
```sql
SELECT COUNT(*) FROM employees;
```

Compatível com PostgreSQL e SQL Server.

## Power BI
**Implementação:** `COUNTROWS(Employees) (DAX)`

### M ou DAX?
- **M (Power Query):** ETL e transformação.
- **DAX:** medidas, KPIs e análise.

## Quando usar
- Auditoria e volume.
- Dashboards
- Exploração de dados

## Armadilhas comuns
- Ignorar valores nulos.
- Misturar tipos de dados.
- Aplicar agregações incorretas.

## Diferenças entre ferramentas
- Excel: interface visual.
- Python: automação e escala.
- SQL: dados persistidos.
- Power BI: visualização e modelagem.

## Veja também
- Merge/Join
- Tratar Nulos
- Top N
