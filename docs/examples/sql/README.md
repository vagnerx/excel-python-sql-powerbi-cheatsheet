# Exemplos SQL — Cheat Sheet

Este diretório contém os códigos em SQL equivalentes para as 24 operações listadas no cheat sheet.

## Como rodar os exemplos?

Todos os scripts `.sql` desta pasta foram desenhados para rodar no nosso banco de dados **SQLite** gerado automaticamente.

### 1. Criar o Banco de Dados

Antes de mais nada, crie o banco de dados e popule-o com os arquivos `.csv` (isso criará o arquivo `datasets/cheatsheet.db`):

```bash
python docs/examples/sql/create_db.py
```

### 2. Rodar pelo Console (Utilitário Python)

Criamos um pequeno wrapper para rodar os scripts SQL direto do terminal usando Python e ver a saída formatada em Pandas:

```bash
python docs/examples/sql/run_sql.py docs/examples/sql/01_basic.sql
python docs/examples/sql/run_sql.py docs/examples/sql/02_aggregations.sql
```

### 3. Rodar via Jupyter Notebook

A forma mais visual e didática. Abra o notebook interativo:

👉 **[Abrir `notebooks/sql_com_python.ipynb`](../../notebooks/sql_com_python.ipynb)**

---

## Arquivos `.sql` disponíveis

| Arquivo | Descrição | Comandos SQL em destaque |
|---|---|---|
| `01_basic.sql` | Operações de seleção, filtros (E/OU) e ordenação | `SELECT`, `WHERE`, `IN`, `ORDER BY`, `LIMIT` |
| `02_aggregations.sql`| Operações de agrupamento e métricas de resumo | `GROUP BY`, `COUNT`, `SUM`, `AVG`, `HAVING` |
| `03_joins.sql` | Cruzamento entre as tabelas employees, customers e orders | `INNER JOIN`, `LEFT JOIN` (Anti-Join) |
| `04_window_functions.sql` | Análise avançada: rankings, fatias (% do total) e running totals | `OVER()`, `PARTITION BY`, `RANK()`, `ROWS UNBOUNDED` |
| `05_ddl.sql` | Colunas condicionais, pivot básico e manuseio de dados (DML) | `CASE WHEN`, `UPDATE`, `DELETE` |
| `06_dates.sql` | Manipulação de campos de data e agrupamentos temporais | `STRFTIME()` (SQLite), `CAST`, Subtração de Datas |

---

## E o DuckDB?

Se você não quer criar um banco SQLite e quer usar SQL direto nos seus arquivos `.csv`, nós demonstramos no nosso **Notebook Jupyter** como o **DuckDB** faz isso maravilhosamente bem:

```sql
-- Exemplo rodando em DuckDB
SELECT * FROM read_csv_auto('datasets/employees.csv')
```

---

## Veja também

- [Exemplos Python](../python/README.md)
- [Exemplos Excel](../excel/README.md)
- [Exemplos Power BI](../powerbi/README.md)
