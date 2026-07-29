# Medidas DAX — Cheat Sheet

Este documento consolida as expressões DAX para as operações avançadas listadas no cheat sheet. Ele é focado em **Medidas (Measures)**, que são calculadas no contexto do visual.

## 1. Operações Básicas de Agregação

```dax
-- Soma (08)
Folha Total = SUM(employees[salario])

-- Contagem de Linhas (06)
Qtd Funcionarios = COUNTROWS(employees)
Qtd Com Salario  = COUNT(employees[salario])

-- Contar Valores Únicos (18)
Departamentos Unicos = DISTINCTCOUNT(employees[departamento])

-- Média (07)
Salario Medio = AVERAGE(employees[salario])

-- Min / Max (15)
Menor Salario = MIN(employees[salario])
Maior Salario = MAX(employees[salario])
```

---

## 2. Filtros e Cálculos Condicionais (CALCULATE)

O `CALCULATE` é a função mais importante do DAX, permitindo alterar o contexto de filtro.

```dax
-- Filtro Simples (02)
Salarios TI = 
CALCULATE(
    SUM(employees[salario]),
    employees[departamento] = "TI"
)

-- Filtro Composto (E/AND)
Salarios TI Senior = 
CALCULATE(
    SUM(employees[salario]),
    employees[departamento] = "TI",
    employees[salario] > 8000
)

-- Filtro com OU (OR / IN)
Salarios TI ou RH = 
CALCULATE(
    SUM(employees[salario]),
    employees[departamento] IN {"TI", "RH"}
)

-- Ignorar Filtros (ALL) - útil para Percentual (20)
Folha Global (Sem Filtros) = 
CALCULATE(
    SUM(employees[salario]),
    ALL(employees)
)

-- Percentual do Total Geral (20)
% do Total = 
DIVIDE(
    SUM(employees[salario]),
    CALCULATE(SUM(employees[salario]), ALL(employees)),
    0
)

-- Percentual do Departamento (ALLEXCEPT)
% Dentro do Departamento = 
DIVIDE(
    SUM(employees[salario]),
    CALCULATE(SUM(employees[salario]), ALLEXCEPT(employees, employees[departamento])),
    0
)
```

---

## 3. Lógica e Condicionais

```dax
-- Coluna Condicional (14) - Pode ser usada como Medida ou Coluna Calculada
Nivel Senioridade = 
SWITCH(
    TRUE(),
    employees[salario] > 12000, "Especialista",
    employees[salario] > 8000,  "Sênior",
    employees[salario] > 5000,  "Pleno",
    "Júnior"
)
```

---

## 4. Analytics Avançado

```dax
-- Ranking Geral (21)
Ranking Geral = 
RANKX(
    ALL(employees),
    CALCULATE(SUM(employees[salario])),
    ,
    DESC,
    Dense
)

-- Ranking por Departamento (respeitando o filtro atual)
Ranking Local = 
RANKX(
    ALLSELECTED(employees[nome]),
    CALCULATE(SUM(employees[salario])),
    ,
    DESC,
    Dense
)

-- Top N Dinâmico (19) - Soma do Top 5
Top 5 Salarios = 
CALCULATE(
    SUM(employees[salario]),
    TOPN(
        5, 
        ALL(employees[nome]), 
        CALCULATE(SUM(employees[salario]))
    )
)
```

---

> 💡 **Nota sobre Colunas Calculadas vs. Medidas:** 
> Sempre prefira **Medidas** para valores agregados (como somas, médias e % do total) pois elas respondem dinamicamente aos filtros visuais (slicers). Use **Colunas Calculadas** apenas quando precisar do resultado em um eixo de gráfico, slicer, ou quando a lógica precisar ser avaliada linha a linha estaticamente.
