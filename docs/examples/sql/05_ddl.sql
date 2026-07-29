-- 05_ddl.sql
-- CREATE TABLE, INSERT, ALTER TABLE, CASE WHEN (Operação 14, 24)

-- 1. Coluna Condicional (CASE WHEN) - Semelhante a SE / IFS
SELECT 
    nome,
    salario,
    CASE 
        WHEN salario > 12000 THEN 'Especialista'
        WHEN salario > 8000 THEN 'Sênior'
        WHEN salario > 5000 THEN 'Pleno'
        ELSE 'Júnior'
    END AS nivel_senioridade
FROM employees
WHERE salario IS NOT NULL
LIMIT 5;

-- 2. Pivot no SQL (Usando CASE WHEN com SUM)
SELECT 
    departamento,
    SUM(CASE WHEN ativo = 'Sim' THEN 1 ELSE 0 END) AS ativos,
    SUM(CASE WHEN ativo = 'Não' THEN 1 ELSE 0 END) AS inativos
FROM employees
GROUP BY departamento;

-- 3. Atualizando Registros (UPDATE)
UPDATE employees
SET ativo = 'Não'
WHERE salario IS NULL;

-- 4. Excluindo Registros (DELETE)
DELETE FROM employees
WHERE id > 100;
