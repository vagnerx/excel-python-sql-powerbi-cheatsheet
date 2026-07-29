# Power Query (Linguagem M) — Cheat Sheet

> 💡 **OBJETIVO DESTE DOCUMENTO (LEIA ANTES DE USAR):**
> Este arquivo **NÃO** é um tutorial passo a passo para construir o seu painel. Ele é um **documento de referência**!
> 
> O objetivo dele é apenas mostrar como as operações do nosso Cheat Sheet (ex: renomear colunas, fazer joins, criar colunas condicionais) são escritas na linguagem "M" do Power BI por trás da interface gráfica. Você **não precisa** decorar ou digitar esses códigos. Ao clicar nos botões do Power Query, o Power BI escreve esses códigos para você automaticamente.

---

O Power Query é utilizado na fase de extração, transformação e carga (ETL). Abaixo, documentamos as lógicas geradas pela ferramenta para as operações correspondentes.

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

> ⚠️ **Boas Práticas no Power BI:** O padrão recomendado é importar as tabelas originais e ligá-las via *Relacionamentos* na **Exibição de Modelo** (veja [star_schema.md](star_schema.md)). Fazer o Join (mesclar) direto no Power Query só é indicado se você realmente precisar unificar/achatar as tabelas antes de carregá-las no modelo (ETL).

Se você precisar cruzar dados no Power Query, **não é necessário escrever código M**. Faça 100% pela interface gráfica:

1. Na tela principal do Power BI, clique em **Transformar Dados** para abrir a janela do *Editor do Power Query*.
2. No painel esquerdo, selecione a tabela principal (ex: `orders`).
3. Na guia **Página Inicial** do *Editor do Power Query*, procure o botão **Mesclar Consultas** (lado direito superior) e clique nele.
4. Selecione a segunda tabela (ex: `customers`) e clique nas colunas de ligação (ex: `id_cliente`) em ambas as pré-visualizações.
5. Escolha o **Tipo de Junção** (ex: *Externa Esquerda / Left Outer*).
6. Após dar OK, clique no botão de "setas duplas" (Expandir) no cabeçalho da nova coluna gerada para escolher quais campos da segunda tabela você quer manter.

Por trás dos panos, o Power BI vai gerar este código M automaticamente no **Editor Avançado**:

```powerquery-m
// LEFT JOIN (Externa Esquerda) - O código abaixo é gerado pela interface
#"Consultas Mescladas" = Table.NestedJoin(orders, {"id_cliente"}, customers, {"id_cliente"}, "customers", JoinKind.LeftOuter),
#"customers Expandido" = Table.ExpandTableColumn(#"Consultas Mescladas", "customers", {"nome", "segmento"}, {"cliente_nome", "cliente_segmento"})

// INNER JOIN (Interna)
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
