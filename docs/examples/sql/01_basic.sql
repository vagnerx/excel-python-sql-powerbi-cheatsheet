-- 01_basic.sql
-- SELECT, WHERE, ORDER BY, LIMIT (Operações 01, 02, 03, 04)

-- 1. Importação Básica (SELECT)
SELECT 
    id, nome, departamento, salario 
FROM employees 
LIMIT 5;

-- 2. Filtro Simples (WHERE)
SELECT 
    nome, departamento, salario 
FROM employees 
WHERE salario > 8000;

-- 3. Filtro Composto e IN
SELECT 
    nome, departamento 
FROM employees 
WHERE departamento IN ('TI', 'Financeiro') 
  AND ativo = 'Sim';

-- 4. Ordenação (ORDER BY) e Top N (LIMIT)
SELECT 
    nome, salario 
FROM employees 
ORDER BY salario DESC 
LIMIT 3;

-- 5. Lidando com Nulos (IS NULL)
SELECT 
    nome, departamento 
FROM employees 
WHERE salario IS NULL;
