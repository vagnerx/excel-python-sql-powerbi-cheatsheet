SELECT name,
       sales,
       RANK() OVER(ORDER BY sales DESC) ranking,
       SUM(sales) OVER(ORDER BY hire_date) acumulado
FROM employees;