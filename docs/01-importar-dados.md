# 1. Importar Dados

> **Tarefa:** Carregar dados de arquivos externos para análise.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Caminho:** Dados → Obter Dados → De Arquivo → Do CSV/Excel  
Ou simplesmente arraste o arquivo para o Excel e use **Power Query**.

```
Dados → Obter e Transformar Dados → De Texto/CSV
```

**Fórmulas úteis após importar:**
```excel
=SOMA(F:F)           → soma de todos os salários
=MÉDIA(F:F)          → média salarial
=CONT.VALORES(A:A)   → quantidade de registros
```

---

## Python (Pandas)

```python
import pandas as pd

# Importar CSV
df = pd.read_csv("datasets/employees.csv")

# Importar Excel
df_excel = pd.read_excel("datasets/employees.xlsx")

# Primeiras linhas
print(df.head())

# Informações gerais
print(df.info())
print(df.shape)   # (linhas, colunas)
```

---

## SQL

```sql
-- Selecionar tudo da tabela
SELECT * FROM employees;

-- Ver estrutura (SQLite)
PRAGMA table_info(employees);

-- Primeiros 5 registros
SELECT * FROM employees LIMIT 5;
```

---

## Power BI (M — Power Query)

```
Página Inicial → Obter Dados → Texto/CSV
```

**Código M equivalente:**
```powerquery-m
let
    Fonte = Csv.Document(
        File.Contents("C:\datasets\employees.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromoveuCabeçalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true])
in
    PromoveuCabeçalhos
```

---

## Quando usar?

| Ferramenta | Use quando... |
|---|---|
| Excel | Análise pontual, arquivos pequenos |
| Python | Automação, grandes volumes, pipelines |
| SQL | Dados já persistidos em banco |
| Power BI | Dashboards e relatórios visuais |

---

## Armadilhas comuns

- **Encoding:** arquivos com acentos precisam de `encoding="utf-8"` no Python
- **Tipos automáticos:** o Pandas pode inferir tipos errados — valide com `df.dtypes`
- **Cabeçalho:** verifique se a primeira linha é realmente o cabeçalho

## Veja também
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Tratar Nulos](12-tratar-nulos.md)
- [Tipos de Dados](11-tipos-de-dados.md)
