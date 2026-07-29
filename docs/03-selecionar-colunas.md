# 3. Selecionar Colunas

> **Tarefa:** Trabalhar apenas com as colunas necessárias.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Interface:** Clique no cabeçalho da coluna → Ctrl+Clique para múltiplas  
**Power Query:** Escolher Colunas → marcar as desejadas

```excel
=ESCOLHERCOLS(A1:H52; 1; 2; 6)   → retorna colunas id, nome, salario (Excel 365)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Selecionar uma coluna (retorna Series)
nomes = df["nome"]

# Selecionar múltiplas colunas (retorna DataFrame)
df_resumo = df[["nome", "departamento", "salario"]]

# Selecionar com loc (por rótulo)
df_loc = df.loc[:, ["nome", "salario", "ativo"]]

# Selecionar com iloc (por posição)
df_iloc = df.iloc[:, [1, 5, 7]]   # colunas: nome, salario, ativo

# Excluir colunas
df_sem_id = df.drop(columns=["id"])

# Selecionar por tipo
df_nums = df.select_dtypes(include=["number"])

print(df_resumo.head())
```

---

## SQL

```sql
-- Selecionar colunas específicas
SELECT nome, departamento, salario
FROM employees;

-- Renomear coluna no SELECT
SELECT nome, salario AS salario_mensal
FROM employees;

-- Selecionar com expressão
SELECT nome,
       salario,
       salario * 12 AS salario_anual
FROM employees;

-- Selecionar tudo (evitar em produção)
SELECT * FROM employees;
```

---

## Power BI

**Interface:** Transformar → Escolher Colunas

**DAX — Tabela virtual com colunas selecionadas:**
```dax
Resumo Funcionários =
SELECTCOLUMNS(
    employees,
    "Nome", employees[nome],
    "Depto", employees[departamento],
    "Salário", employees[salario]
)
```

**Power Query M:**
```powerquery-m
= Table.SelectColumns(employees, {"nome", "departamento", "salario"})
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Reduzir volume de dados | `SELECT col1, col2` / `df[["col1","col2"]]` |
| Criar relatório limpo | Excluir colunas técnicas (id, flags) |
| Calcular coluna derivada | `salario * 12 AS salario_anual` |

---

## Armadilhas comuns

- `df["nome"]` retorna **Series**; `df[["nome"]]` retorna **DataFrame** — atenção ao tipo
- `SELECT *` em produção retorna dados desnecessários e torna o código frágil
- No Power BI, preferir `SELECTCOLUMNS` a `ALL` para evitar contextos de filtro indesejados

## Veja também
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Renomear Colunas](10-renomear-colunas.md)
- [Tipos de Dados](11-tipos-de-dados.md)
