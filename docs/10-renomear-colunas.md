# 10. Renomear Colunas

> **Tarefa:** Padronizar ou clarificar os nomes das colunas.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Interface:** Duplo-clique no cabeçalho da coluna para renomear  
**Power Query:** Duplo-clique no nome da etapa ou renomeie na barra de fórmulas

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Renomear colunas específicas
df_renamed = df.rename(columns={
    "nome":          "funcionario",
    "departamento":  "depto",
    "salario":       "salario_bruto",
    "data_admissao": "dt_admissao",
})

# Renomear todas as colunas (substituindo lista completa)
df.columns = ["id", "funcionario", "depto", "cargo", "cidade",
              "salario_bruto", "dt_admissao", "ativo"]

# Padronizar para minúsculas e remover espaços
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Adicionar prefixo/sufixo
df_prefix = df.add_prefix("emp_")

print(df_renamed.columns.tolist())
```

---

## SQL

```sql
-- Renomear no SELECT (alias de coluna)
SELECT
    nome          AS funcionario,
    departamento  AS depto,
    salario       AS salario_bruto
FROM employees;

-- Usar alias na query (CTEs)
WITH base AS (
    SELECT nome AS funcionario, salario AS salario_bruto
    FROM employees
)
SELECT * FROM base WHERE salario_bruto > 5000;

-- Renomear tabela (alias)
SELECT e.nome, e.salario
FROM employees AS e
WHERE e.departamento = 'TI';
```

> ⚠️ SQL não tem `RENAME COLUMN` em todos os SGBDs. No SQLite, é necessário recriar a tabela.

---

## Power BI

**Interface:** Transformar → Renomear (duplo-clique na coluna)

**Power Query M:**
```powerquery-m
= Table.RenameColumns(
    employees,
    {{"nome", "funcionario"}, {"salario", "salario_bruto"}}
)
```

**DAX — Coluna calculada com novo nome:**
```dax
salario_bruto = employees[salario]
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Padronizar nomenclatura | `rename()` no Python / `RenameColumns` no M |
| Exibição amigável em relatório | Alias no SQL / renomear no Power BI |
| Integrar dados de fontes diferentes | Renomear antes do JOIN |

---

## Armadilhas comuns

- `df.rename(columns=...)` **não modifica** o DataFrame original por padrão — use `inplace=True` ou reatribua
- Alias no SQL (`AS`) é apenas visual — a coluna original não muda no banco
- Renomear colunas no Power BI pode quebrar medidas DAX que referenciam o nome antigo

## Veja também
- [Selecionar Colunas](03-selecionar-colunas.md)
- [Tipos de Dados](11-tipos-de-dados.md)
- [Merge / Join](13-merge-join.md)
