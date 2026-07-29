# Exemplos Excel — Cheat Sheet

Arquivos Excel prontos para estudo e replicação das 24 operações do cheat sheet.

---

## Arquivo principal

### `cheatsheet_excel.xlsx`

Gerado pelo script `generate_excel.py` com dados reais e fórmulas funcionais.

Para regenerar (caso queira atualizar com novos datasets):

```bash
pip install openpyxl
python docs/examples/excel/generate_excel.py
```

---

## Abas do arquivo

| Aba | Conteúdo | Fórmulas em destaque |
|---|---|---|
| **Dados** | Dataset `employees.csv` completo + painel de resumo | `CONT.VALORES`, `MEDIA`, `MAXIMO`, `MINIMO`, `SOMA` |
| **Filtros** | Exemplos de filtro e agregação condicional | `CONT.SE`, `CONT.SES`, `SOMASE`, `SOMASES`, `MEDIASE`, `MEDIASES` |
| **Agrupamento** | Tabela equivalente ao GROUP BY por departamento | `SOMASE`, `MAXSES`, `MINSES`, `MEDIASE` |
| **Datas** | Extração de partes, cálculo de tempo de casa, filtros | `ANO`, `MES`, `DIA`, `HOJE`, `FRAÇÃO.ANO`, `FIMMÊS`, `NUM.SEMANA` |
| **Condicional** | Coluna de nível/faixa com lógica condicional | `SE`, `IFS`, `SEERRO`, lógicas aninhadas |
| **Lookup** | Busca de funcionário por ID | `PROCV`, `PROCX`, `INDICE+CORRESP`, `SEERRO` |
| **Metricas** | Ranking, Top N, percentual, desvio padrão | `ORDEM.EQ`, `GRANDE`, `PEQUENO`, `MED`, `DESVPAD`, `SOMARPRODUTO` |

---

## Código de cores nas fórmulas

| Cor | Significado |
|---|---|
| 🟡 Amarelo claro | Fórmulas principais (PROCV, SE, SOMASE...) |
| 🟢 Verde claro | Fórmulas alternativas (PROCX, MEDIASES...) |
| 🔵 Azul claro | INDICE + CORRESP |
| 🔴 Vermelho claro | SEERRO — tratamento de erro |

---

## O que não é possível gerar por código

> **Tabela Dinâmica (Pivot Table)** e **Gráficos**: o `openpyxl` não suporta criação de Tabelas Dinâmicas.
> Para criá-las manualmente:
> 1. Abra o arquivo `cheatsheet_excel.xlsx`
> 2. Selecione os dados na aba **Dados**
> 3. `Inserir → Tabela Dinâmica`
> 4. Configure: Linhas = `departamento`, Valores = `salario` (Média)

---

## Compatibilidade de fórmulas

| Fórmula | Versão mínima |
|---|---|
| `PROCV`, `SOMASE`, `CONT.SE` | Excel 2010+ |
| `MAXSES`, `MINSES`, `IFS` | Excel 2016+ |
| `PROCX`, `FILTRAR`, `ÚNICO` | Excel 365 / Excel 2021 |

---

## Datasets utilizados

| Arquivo | Descrição |
|---|---|
| `datasets/employees.csv` | 52 funcionários — usado em todas as abas |
| `datasets/customers.csv` | 20 clientes — para exemplos de PROCV cruzado |
| `datasets/orders.csv` | 100 pedidos — para exemplos de SOMASES por período |

---

## Veja também

- [Documentação Excel no site](https://vagnerx.github.io/excel-python-sql-powerbi-cheatsheet/01-importar-dados/)
- [Exemplos Python](../python/README.md)
- [Exemplos SQL](../sql/README.md)
