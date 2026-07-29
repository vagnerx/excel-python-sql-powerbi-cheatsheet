# 9. Obter Valores Únicos

> **Tarefa:** Identificar e listar valores distintos, removendo duplicatas.  
> **Dataset:** `datasets/employees.csv`

---

## Excel

**Remover duplicatas:** Dados → Remover Duplicatas → selecionar coluna

**Valores únicos com fórmula (Excel 365):**
```excel
=ÚNICO(C2:C52)                     → lista únicos da coluna departamento
=ÚNICO(C2:C52; FALSO; VERDADEIRO)  → valores que aparecem exatamente 1 vez
```

**Contar distintos:**
```excel
=SOMARPRODUTO(1/CONT.SE(C2:C52;C2:C52))   → conta valores únicos (clássico)
```

---

## Python (Pandas)

```python
import pandas as pd
df = pd.read_csv("datasets/employees.csv")

# Lista de valores únicos
deptos_unicos = df["departamento"].unique()

# Contagem de valores únicos
qtd_deptos = df["departamento"].nunique()

# Frequência de cada valor
frequencia = df["departamento"].value_counts()

# Remover duplicatas (todas as colunas)
df_sem_dup = df.drop_duplicates()

# Remover duplicatas por coluna específica (manter primeiro)
df_sem_dup_nome = df.drop_duplicates(subset=["nome"], keep="first")

# Detectar duplicatas
duplicatas = df[df.duplicated()]
print(f"Linhas duplicadas: {len(duplicatas)}")

print(f"Departamentos únicos ({qtd_deptos}):", deptos_unicos)
print("\nFrequência por departamento:")
print(frequencia)
```

---

## SQL

```sql
-- Valores únicos
SELECT DISTINCT departamento FROM employees
ORDER BY departamento;

-- Contagem de valores únicos
SELECT COUNT(DISTINCT departamento) AS qtd_deptos
FROM employees;

-- Frequência por valor
SELECT departamento, COUNT(*) AS total
FROM employees
GROUP BY departamento
ORDER BY total DESC;

-- Detectar duplicatas (mesmo nome)
SELECT nome, COUNT(*) AS ocorrencias
FROM employees
GROUP BY nome
HAVING COUNT(*) > 1;
```

---

## Power BI

**Interface:** Transformar → Remover Duplicatas (na coluna)

**DAX:**
```dax
Qtd Departamentos =
DISTINCTCOUNT(employees[departamento])

Tabela de Departamentos =
DISTINCT(employees[departamento])
```

**Power Query M:**
```powerquery-m
= Table.Distinct(employees, {"nome"})
```

---

## Quando usar?

| Cenário | Técnica |
|---|---|
| Listar categorias disponíveis | `DISTINCT` / `unique()` |
| Verificar qualidade dos dados | `duplicated()` / `HAVING COUNT > 1` |
| Popular filtros/slicers | `DISTINCTCOUNT` no DAX |

---

## Armadilhas comuns

- `DISTINCT` no SQL não remove as linhas do banco — apenas filtra a exibição
- `drop_duplicates()` sem `subset` compara **todas** as colunas — use `subset=[]` para especificar
- Dois registros podem ter o mesmo nome mas IDs diferentes — defina bem o critério de duplicata

## Veja também
- [Filtrar Linhas](02-filtrar-linhas.md)
- [Contar Valores Únicos](18-contar-unicos.md)
- [Tratar Nulos](12-tratar-nulos.md)
