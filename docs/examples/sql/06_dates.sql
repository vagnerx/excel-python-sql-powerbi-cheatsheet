-- 06_dates.sql
-- YEAR(), MONTH(), DAY(), filtros por data (Operações 16, 17)

-- Nota: No SQLite, as funções de data são usadas através de STRFTIME. 
-- Se for PostgreSQL ou SQL Server, usa-se YEAR(), MONTH() ou EXTRACT().

-- 1. Extração de Data (SQLite format)
SELECT 
    nome,
    data_admissao,
    strftime('%Y', data_admissao) AS ano,
    strftime('%m', data_admissao) AS mes,
    strftime('%Y-%m', data_admissao) AS ano_mes
FROM employees
WHERE data_admissao IS NOT NULL
LIMIT 5;

-- 2. Filtro por Data
SELECT 
    nome,
    data_admissao 
FROM employees 
WHERE data_admissao >= '2023-01-01' 
  AND data_admissao < '2024-01-01';

-- 3. Idade na Empresa (Dias)
SELECT 
    nome,
    data_admissao,
    CAST(julianday('now') - julianday(data_admissao) AS INTEGER) AS dias_de_empresa
FROM employees
WHERE data_admissao IS NOT NULL
ORDER BY dias_de_empresa DESC
LIMIT 5;
