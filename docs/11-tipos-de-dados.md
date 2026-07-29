# 11. Mudar Tipo de Dados

> **Tarefa:** Garantir que cada coluna tenha o tipo correto para cálculos e análises.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

```excel
Formatar Célula → Número / Data / Texto / Moeda
```

- **Data:** Ctrl+1 → Número → Data → escolher formato `DD/MM/AAAA`
- **Número:** Formatar como moeda ou número com casas decimais
- **Texto para número:** `=VALOR(A2)` converte texto "5000" em número 5000
- **Número para texto:** `=TEXTO(F2;"R$ #.##0,00")` formata como moeda

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Ver tipos atuais
print(df.dtypes)

# Converter coluna para inteiro
df["id"] = df["id"].astype(int)

# Converter para float
df["salario"] = pd.to_numeric(df["salario"], errors="coerce")  # nulos viram NaN

# Converter para datetime
df["data_admissao"] = pd.to_datetime(df["data_admissao"], format="%Y-%m-%d", errors="coerce")

# Converter para string
df["ativo"] = df["ativo"].astype(str)

# Converter para category (economiza memória)
df["departamento"] = df["departamento"].astype("category")

# Converter para boolean
df["ativo_bool"] = df["ativo"].map({"Sim": True, "Não": False})

print(df.dtypes)
print(f"\nMemória usada: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
```

---

## SQL

```sql
-- Converter tipo no SELECT (CAST)
SELECT
    nome,
    CAST(salario AS INTEGER)   AS salario_int,
    CAST(salario AS TEXT)      AS salario_texto,
    DATE(data_admissao)        AS data_fmt
FROM employees;

-- Formatar data
SELECT nome, strftime('%d/%m/%Y', data_admissao) AS data_br
FROM employees
WHERE data_admissao IS NOT NULL;

-- Tratar texto como número
SELECT nome, CAST(salario AS REAL) * 1.10 AS salario_reajustado
FROM employees
WHERE salario IS NOT NULL;
```

---

## Power BI

**Interface:** Transformar → Tipo de Dados → Número Decimal / Texto / Data

**Power Query M:**
```powerquery-m
= Table.TransformColumnTypes(
    employees,
    {
        {"salario",       type number},
        {"data_admissao", type date},
        {"id",            type text}
    }
)
```

**DAX — Conversão:**
```dax
Salário Inteiro = INT(employees[salario])
Data Formatada  = FORMAT(employees[data_admissao], "DD/MM/YYYY")
```

---

## Quando usar?

| Problema | Solução |
|---|---|
| Número importado como texto | `pd.to_numeric(errors="coerce")` / `CAST AS REAL` |
| Data importada como texto | `pd.to_datetime()` / `DATE()` no SQL |
| Categoria repetitiva | `.astype("category")` para economizar memória |

---

## Armadilhas comuns

- `.astype(int)` falha se houver nulos — use `pd.to_numeric(errors="coerce")` antes
- No SQLite, datas são armazenadas como TEXT — use funções `DATE()` e `strftime()`
- No Power BI, alterar o tipo de dados pode quebrar etapas anteriores do Power Query

## Veja também
- [Tratar Nulos](12-tratar-nulos.md)
- [Extração de Datas](16-extracao-datas.md)
- [Importar Dados](01-importar-dados.md)
