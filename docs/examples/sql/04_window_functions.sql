-- 04_window_functions.sql
-- RANK, SUM OVER, AVG OVER, ROW_NUMBER (Operações 20, 21, 22)

-- 1. Ranking Geral e por Departamento (Operação 21)
SELECT 
    nome, 
    departamento, 
    salario,
    RANK() OVER(ORDER BY salario DESC) AS rank_geral,
    RANK() OVER(PARTITION BY departamento ORDER BY salario DESC) AS rank_depto
FROM employees
WHERE salario IS NOT NULL;

-- 2. Percentual do Total do Departamento (Operação 20)
SELECT 
    nome, 
    departamento, 
    salario,
    SUM(salario) OVER(PARTITION BY departamento) AS total_depto,
    ROUND((salario * 100.0) / SUM(salario) OVER(PARTITION BY departamento), 1) AS pct_do_depto
FROM employees
WHERE salario IS NOT NULL;

-- 3. Acumulado e Média Móvel (Operações 22, 23)
-- Exemplo fictício ordenando os pedidos por data para fazer soma acumulada
SELECT 
    data_pedido,
    valor_total,
    SUM(valor_total) OVER(ORDER BY data_pedido ROWS UNBOUNDED PRECEDING) AS soma_acumulada,
    AVG(valor_total) OVER(ORDER BY data_pedido ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel_3_dias
FROM orders
LIMIT 10;
