# Power Query (Linguagem M) — Cheat Sheet

O Power Query é utilizado na fase de extração, transformação e carga (ETL). Aqui estão os equivalentes das operações básicas realizadas via interface ou scripts M.

## 1. Importação de Dados (01)

No Power Query, você raramente escreve M do zero para importar, usa-se a interface. O código gerado é similar a:

```powerquery-m
// CSV
Fonte = Csv.Document(File.Contents("C:\caminho\employees.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None])

// Excel
Fonte = Excel.Workbook(File.Contents("C:\caminho\arquivo.xlsx"), null, true)
```

## 2. Tipos de Dados e Limpeza

```powerquery-m
// Alterar Tipos (11)
#"Tipo Alterado" = Table.TransformColumnTypes(Fonte,{{"id", Int64.Type}, {"salario", type number}, {"data_admissao", type date}})

// Tratar Nulos / Substituir Valores (12)
#"Valor Substituído" = Table.ReplaceValue(#"Tipo Alterado", null, "Não Informado", Replacer.ReplaceValue, {"departamento"})

// Renomear Colunas (10)
#"Colunas Renomeadas" = Table.RenameColumns(#"Valor Substituído",{{"nome", "Funcionario"}})

// Selecionar Colunas / Remover Outras (03)
#"Colunas Removidas" = Table.RemoveColumns(#"Colunas Renomeadas",{"cidade", "cargo"})
```

## 3. Merge / Join (13)

Operações de Join são feitas através do `Table.NestedJoin`, seguidas da expansão.

```powerquery-m
// LEFT JOIN (Padrão)
#"Consultas Mescladas" = Table.NestedJoin(orders, {"id_cliente"}, customers, {"id_cliente"}, "customers", JoinKind.LeftOuter),
#"customers Expandido" = Table.ExpandTableColumn(#"Consultas Mescladas", "customers", {"nome", "segmento"}, {"cliente_nome", "cliente_segmento"})

// INNER JOIN
#"Consultas Mescladas Inner" = Table.NestedJoin(orders, {"id_cliente"}, customers, {"id_cliente"}, "customers", JoinKind.Inner)

// ANTI JOIN (Left Anti) - Encontrar clientes sem pedidos
#"Left Anti" = Table.NestedJoin(customers, {"id_cliente"}, orders, {"id_cliente"}, "orders", JoinKind.LeftAnti)
```

## 4. Coluna Condicional (14)

Embora recomendada na interface ("Adicionar Coluna Condicional"), o código gerado é:

```powerquery-m
#"Coluna Condicional Adicionada" = Table.AddColumn(#"Passo Anterior", "Nivel", each 
    if [salario] > 12000 then "Especialista" 
    else if [salario] > 8000 then "Sênior" 
    else if [salario] > 5000 then "Pleno" 
    else "Júnior"
)
```

## 5. Pivot e Unpivot (24)

Operações fundamentais para modelagem. **Unpivot** é especialmente útil para transformar tabelas legadas do Excel.

```powerquery-m
// Unpivot (Transformar Colunas em Linhas)
// Selecione as colunas que NÃO quer mudar, botão direito > "Transformar Outras Colunas em Linhas"
#"Outras Colunas Não Dinâmicas" = Table.UnpivotOtherColumns(Fonte, {"id_pedido", "id_produto"}, "Tipo Valor", "Valor")

// Pivot (Transformar Linhas em Colunas)
#"Coluna Dinâmica" = Table.Pivot(Fonte, List.Distinct(Fonte[ativo]), "ativo", "salario", List.Average)
```
