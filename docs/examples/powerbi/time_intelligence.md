# Time Intelligence (DAX)

Para análises temporais no Power BI (operações 22 e 23 do cheat sheet), é **obrigatório** possuir uma Tabela de Datas (Calendário) marcada corretamente no modelo e relacionada com as tabelas de fatos.

## 1. Tabela de Calendário Básica

Se você não tiver uma no banco de dados, pode gerar uma com DAX:

```dax
Calendario = 
ADDCOLUMNS(
    CALENDARAUTO(),
    "Ano", YEAR([Date]),
    "Mês Num", MONTH([Date]),
    "Mês Nome", FORMAT([Date], "MMMM"),
    "Trimestre", "Q" & FORMAT([Date], "Q"),
    "Ano Mês", FORMAT([Date], "YYYY-MM")
)
```

## 2. Acumulado / Running Total (22)

Acumulados anuais (Year-To-Date), mensais (Month-To-Date), etc.

```dax
-- YTD Padrão (Total Acumulado no Ano)
Receita YTD = 
TOTALYTD(
    SUM(orders[valor_total]),
    Calendario[Date]
)

-- YTD com CALCULATE (alternativa)
Receita YTD Calc = 
CALCULATE(
    SUM(orders[valor_total]),
    DATESYTD(Calendario[Date])
)

-- MTD (Total Acumulado no Mês)
Receita MTD = 
TOTALMTD(
    SUM(orders[valor_total]),
    Calendario[Date]
)
```

## 3. Comparações de Período

Comparar a métrica atual com o mesmo período do ano anterior.

```dax
-- Mesmo período do ano passado (YoY)
Receita Ano Anterior (LY) = 
CALCULATE(
    SUM(orders[valor_total]),
    SAMEPERIODLASTYEAR(Calendario[Date])
)

-- Variação (YoY %)
Crescimento YoY % = 
DIVIDE(
    [Receita YTD] - [Receita Ano Anterior (LY)],
    [Receita Ano Anterior (LY)],
    0
)
```

## 4. Janela Móvel / Rolling Window (23)

Cálculo de médias ou somas em janelas deslizantes dos últimos N dias.

```dax
-- Média Móvel de 30 Dias
Media Movel 30D = 
CALCULATE(
    AVERAGE(orders[valor_total]),
    DATESINPERIOD(
        Calendario[Date],
        MAX(Calendario[Date]), -- Inicia na última data do contexto
        -30,                   -- Retrocede 30
        DAY                    -- Unidade (DAY, MONTH, QUARTER, YEAR)
    )
)

-- Soma Móvel (Rolling 12 Months - R12M)
Receita Ultimos 12 Meses = 
CALCULATE(
    SUM(orders[valor_total]),
    DATESINPERIOD(
        Calendario[Date],
        MAX(Calendario[Date]),
        -12,
        MONTH
    )
)
```

## ⚠️ Armadilhas de Time Intelligence

1. **Mark as Date Table**: A tabela de calendário precisa ser marcada como "Tabela de Data" no Power BI para que o Time Intelligence funcione corretamente, garantindo que não haja buracos (missing dates).
2. **Relacionamento**: A relação deve ser `Calendario[Date] 1 --- * Fato[Data]`.
3. **Múltiplas Datas**: Se uma tabela fato tem `data_pedido` e `data_entrega`, crie duas relações. Deixe a principal ativa e use `USERELATIONSHIP()` no DAX para a inativa.
