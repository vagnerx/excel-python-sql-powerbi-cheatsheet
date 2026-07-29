-- 03_joins.sql
-- INNER JOIN, LEFT JOIN, múltiplas tabelas (Operação 13)

-- 1. INNER JOIN (Apenas cruzamentos válidos)
SELECT 
    o.id_pedido, 
    c.nome AS cliente, 
    o.valor_total
FROM orders o
INNER JOIN customers c ON o.id_cliente = c.id_cliente
LIMIT 5;

-- 2. LEFT JOIN e Anti-Join (Clientes sem pedidos)
SELECT 
    c.nome, 
    c.segmento,
    o.id_pedido
FROM customers c
LEFT JOIN orders o ON c.id_cliente = o.id_cliente
WHERE o.id_pedido IS NULL;

-- 3. Agregando com Join
-- Total gasto por cliente (Top 5)
SELECT 
    c.nome,
    COUNT(o.id_pedido) AS qtd_pedidos,
    SUM(o.valor_total) AS total_gasto
FROM customers c
LEFT JOIN orders o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nome
ORDER BY total_gasto DESC
LIMIT 5;
