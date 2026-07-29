-- 02_aggregations.sql
-- COUNT, SUM, AVG, GROUP BY, HAVING (Operações 05, 06, 07, 08, 18)

-- 1. Métricas Globais
SELECT 
    COUNT(*) AS qtd_funcionarios,
    COUNT(salario) AS qtd_com_salario,
    ROUND(AVG(salario), 2) AS salario_medio,
    SUM(salario) AS folha_total,
    MAX(salario) AS maior_salario,
    MIN(salario) AS menor_salario,
    COUNT(DISTINCT departamento) AS deptos_unicos
FROM employees;

-- 2. Agrupamento (GROUP BY)
SELECT 
    departamento,
    COUNT(*) AS qtd,
    ROUND(AVG(salario), 2) AS media,
    SUM(salario) AS total
FROM employees
GROUP BY departamento
ORDER BY total DESC;

-- 3. Agrupamento com Filtro (HAVING)
-- Departamentos com média salarial maior que 7000
SELECT 
    departamento,
    ROUND(AVG(salario), 2) AS media
FROM employees
GROUP BY departamento
HAVING AVG(salario) > 7000;
