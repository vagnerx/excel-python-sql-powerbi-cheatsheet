# Power Query (M)

## Importar CSV
```M
Csv.Document(
    File.Contents("employees.csv")
)
```

## Alterar Tipo
```M
Table.TransformColumnTypes(
    Fonte,
    {{"salary", Int64.Type}}
)
```

## Remover Duplicados
```M
Table.Distinct(Fonte)
```

## Unpivot
```M
Table.UnpivotOtherColumns(...)
```
