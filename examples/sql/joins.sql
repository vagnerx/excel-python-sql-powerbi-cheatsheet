SELECT e.*, d.manager
FROM employees e
JOIN departments d
  ON e.department = d.department;