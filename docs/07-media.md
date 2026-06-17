# Média

## Explicação Conceitual
Calcular tendência central.

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
resultado = df['salary'].mean()
print(resultado)
```

## SQL
```sql
SELECT AVG(salary) FROM employees;
```

Compatível com PostgreSQL e SQL Server.

## Power BI
**Implementação:** `AVERAGE(Employees[salary]) (DAX)`

### M ou DAX?
- **M (Power Query):** ETL e transformação.
- **DAX:** medidas, KPIs e análise.

## Quando usar
- Indicadores.
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
