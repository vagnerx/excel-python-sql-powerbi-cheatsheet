# 16. Extração de Datas

> **Tarefa:** Extrair partes de uma data (ano, mês, dia, trimestre, dia da semana).  
> **Dataset:** `datasets/employees.csv` — coluna `data_admissao`

---

## Excel

```excel
=ANO(G2)          → extrai o ano
=MÊS(G2)          → extrai o mês (1-12)
=DIA(G2)          → extrai o dia
=TEXTO(G2;"MMMM") → nome do mês por extenso
=DIA.DA.SEMANA(G2;2) → dia da semana (2=seg=1, dom=7)
=INT((MÊS(G2)-1)/3)+1  → trimestre (1 a 4)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Converter para datetime primeiro
df["data_admissao"] = pd.to_datetime(df["data_admissao"], errors="coerce")

# Extrair partes da data
df["ano"]           = df["data_admissao"].dt.year
df["mes"]           = df["data_admissao"].dt.month
df["dia"]           = df["data_admissao"].dt.day
df["trimestre"]     = df["data_admissao"].dt.quarter
df["dia_semana"]    = df["data_admissao"].dt.day_name()      # "Monday", "Tuesday"...
df["nome_mes"]      = df["data_admissao"].dt.month_name()    # "January"...
df["semana_ano"]    = df["data_admissao"].dt.isocalendar().week

# Análise por ano de admissão
por_ano = df.groupby("ano")["id"].count().rename("contratacoes")
print(por_ano)

# Funcionários admitidos em 2023
admitidos_2023 = df[df["ano"] == 2023]
print(f"\nContratados em 2023: {len(admitidos_2023)}")

# Tempo de casa (em dias)
df["tempo_casa_dias"] = (pd.Timestamp.today() - df["data_admissao"]).dt.days
df["tempo_casa_anos"] = (df["tempo_casa_dias"] / 365.25).round(1)

print(df[["nome","data_admissao","ano","trimestre","tempo_casa_anos"]].head())
```

---

## SQL

```sql
-- Extrair partes (SQLite usa strftime)
SELECT nome,
       data_admissao,
       strftime('%Y', data_admissao)  AS ano,
       strftime('%m', data_admissao)  AS mes,
       strftime('%d', data_admissao)  AS dia,
       strftime('%W', data_admissao)  AS semana_ano
FROM employees
WHERE data_admissao IS NOT NULL;

-- Contratações por ano
SELECT strftime('%Y', data_admissao) AS ano, COUNT(*) AS total
FROM employees
WHERE data_admissao IS NOT NULL
GROUP BY ano
ORDER BY ano;

-- Trimestre (SQLite não tem QUARTER nativo)
SELECT nome,
    CASE
        WHEN CAST(strftime('%m', data_admissao) AS INT) <= 3 THEN 'Q1'
        WHEN CAST(strftime('%m', data_admissao) AS INT) <= 6 THEN 'Q2'
        WHEN CAST(strftime('%m', data_admissao) AS INT) <= 9 THEN 'Q3'
        ELSE 'Q4'
    END AS trimestre
FROM employees
WHERE data_admissao IS NOT NULL;
```

---

## Power BI

**Interface:** Transformar → Data → Ano / Mês / Dia / Trimestre

**DAX:**
```dax
Ano Admissão   = YEAR(employees[data_admissao])
Mês Admissão   = MONTH(employees[data_admissao])
Trimestre      = QUARTER(employees[data_admissao])
Nome do Mês    = FORMAT(employees[data_admissao], "MMMM")
Tempo de Casa  = DATEDIFF(employees[data_admissao], TODAY(), YEAR)
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Análise por período | `dt.year`, `strftime('%Y')`, `YEAR()` |
| Sazonalidade por mês | `dt.month_name()`, `FORMAT("MMMM")` |
| Tempo de casa / SLA | `Timestamp.today() - data` / `DATEDIFF` |

---

## Armadilhas comuns

- A coluna deve ser do tipo `datetime` no Pandas — use `pd.to_datetime()` antes de acessar `.dt`
- No SQLite, não existe `YEAR()` — use `strftime('%Y', data)`
- No Power BI, colunas de data devem ser do tipo `Date` para funcionar com a tabela de datas (Date Table)

## Veja também
- [Filtrar por Data](17-filtrar-por-data.md)
- [Tipos de Dados](11-tipos-de-dados.md)
- [Janela Móvel](23-janela-movel.md)
