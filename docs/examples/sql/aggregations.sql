SELECT department,
       COUNT(*) qtd,
       AVG(salary) media_salario,
       SUM(sales) total_vendas
FROM employees
GROUP BY department;