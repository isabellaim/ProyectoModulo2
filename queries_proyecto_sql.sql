USE sql10786147;
-- Proyecto Final 
-- Nombres: Annabella Sánchez, Juan Munizaga, Isabella Martín

-- Primer Ejercicio - Primera Sección
SELECT 
  pr.ProductName AS nombre, 
  SUM(ordets.Quantity * ordets.UnitPrice) AS total_ganancia
FROM Products pr
JOIN OrderDetails ordets
  ON pr.ProductID = ordets.ProductID
GROUP BY pr.ProductID
ORDER BY total_ganancia DESC
LIMIT 10;

-- Segundo Ejercicio - Primera Sección
SELECT 
  c.CategoryName AS categoria, 
  SUM(ordets.Quantity * ordets.UnitPrice) AS tot_ganancia
FROM Categories c
JOIN Products pr
  ON c.CategoryID = pr.CategoryID
JOIN OrderDetails ordets
  ON pr.ProductID = ordets.ProductID
GROUP BY categoria
ORDER BY tot_ganancia DESC
LIMIT 5;

-- Tercer Ejercicio: ¿Qué cliente ha realizado más compras en valor total? - Primera Sección
SELECT 
  cust.CompanyName, 
  SUM(ordets.Quantity * ordets.UnitPrice) AS valor_total
FROM Customers cust
JOIN Orders ords
  ON cust.CustomerID = ords.CustomerID
JOIN OrderDetails ordets
  ON ordets.OrderID = ords.OrderID
GROUP BY cust.CustomerID
ORDER BY valor_total DESC
LIMIT 1;

-- Cuarto Ejercicio: ¿Qué país ha generado más ingresos en los últimos 12 meses? - Primera Sección
SELECT 
  cust.Country AS pais, 
  SUM(ordets.Quantity * ordets.UnitPrice) AS ingresos
FROM Customers cust
JOIN Orders ords
  ON cust.CustomerID = ords.CustomerID
JOIN OrderDetails ordets
  ON ordets.OrderID = ords.OrderID
WHERE ords.OrderDate >= (
    SELECT DATE_SUB(MAX(o.OrderDate), INTERVAL 12 MONTH)
    FROM Orders o
)
GROUP BY pais
ORDER BY ingresos DESC
LIMIT 1;

-- Quinto Ejercicio: ¿Qué empleado ha gestionado la mayor cantidad de pedidos? - Primera Sección
SELECT 
  e.FirstName AS nombre, 
  e.LastName AS apellido, 
  COUNT(ords.OrderID) AS total_ordenes
FROM Employees e
JOIN Orders ords
  ON e.EmployeeID = ords.EmployeeID
GROUP BY e.EmployeeID
ORDER BY total_ordenes DESC
LIMIT 2;

-- Primer Ejercicio: ¿Qué porcentaje de clientes no ha comprado nada? - Segunda Sección
SELECT 
  100.0 * COUNT(*) / (
    SELECT COUNT(*) 
    FROM Customers
  ) AS pct 
FROM Customers cust
WHERE NOT EXISTS (
  SELECT 1
  FROM Orders ords
  WHERE ords.CustomerID = cust.CustomerID
);

-- Segundo Ejercicio: ¿Cuáles son los 5 países con más clientes activos? - Segunda Sección
SELECT 
  c.Country, 
  COUNT(DISTINCT c.CustomerID) AS num_clientes
FROM Customers c
JOIN Orders o
  ON c.CustomerID = o.CustomerID
GROUP BY c.Country
ORDER BY num_clientes DESC
LIMIT 5;

-- Tercer Ejercicio: ¿Qué clientes han comprado más de 10 productos distintos? - Segunda Sección
SELECT  
  c.CustomerID, 
  c.CompanyName, 
  COUNT(DISTINCT ordets.ProductID) AS DistinctProducts
FROM Customers c
JOIN Orders ords
  ON c.CustomerID = ords.CustomerID
JOIN OrderDetails ordets
  ON ords.OrderID = ordets.OrderID
GROUP BY c.CustomerID, c.CompanyName
HAVING COUNT(DISTINCT ordets.ProductID) > 10
ORDER BY DistinctProducts DESC;

-- Cuarto Ejercicio: ¿Hay clientes que compran solo un tipo de producto (una categoría)? - Segunda Sección
SELECT 
  COUNT(*) AS clientes_una_categoria
FROM (
  SELECT 
    cust.CustomerID, 
    COUNT(DISTINCT pr.CategoryID) AS num_categorias
  FROM Customers cust
  JOIN Orders ords
    ON cust.CustomerID = ords.CustomerID
  JOIN OrderDetails ordets
    ON ords.OrderID = ordets.OrderID
  JOIN Products pr
    ON ordets.ProductID = pr.ProductID
  GROUP BY cust.CustomerID
  HAVING num_categorias = 1
) sub;

-- Quinta Pregunta: ¿Cuál es el ticket promedio por pedido y cómo varía entre países? - Segunda Sección
-- Ticket promedio global
SELECT 
  AVG(t.total_orden) AS prom_ticket_global
FROM (
  SELECT 
    ords.OrderID,
    SUM(ordets.UnitPrice * ordets.Quantity) AS total_orden
  FROM Orders ords
  JOIN OrderDetails ordets
    ON ords.OrderID = ordets.OrderID
  GROUP BY ords.OrderID
) t;

-- Ticket promedio por país
SELECT 
  t.Country,
  AVG(t.OrderTotal) AS prom_ticket_pais
FROM (
  SELECT 
    ords.OrderID,
    cust.Country,
    SUM(ordets.UnitPrice * ordets.Quantity) AS OrderTotal
  FROM Customers cust
  JOIN Orders ords
    ON cust.CustomerID = ords.CustomerID
  JOIN OrderDetails ordets
    ON ords.OrderID = ordets.OrderID
  GROUP BY ords.OrderID, cust.Country
) t
GROUP BY t.Country
ORDER BY prom_ticket_pais DESC;

-- Primer Ejercicio: ¿Cuál es el ranking de clientes por gasto total? - Tercera Sección
SELECT 
  cust.CustomerID,
  cust.CompanyName,
  SUM(ordets.UnitPrice * ordets.Quantity) AS total_gasto
FROM Customers cust
JOIN Orders ords
  ON cust.CustomerID = ords.CustomerID
JOIN OrderDetails ordets
  ON ords.OrderID = ordets.OrderID
GROUP BY cust.CustomerID, cust.CompanyName
ORDER BY total_gasto DESC;

-- Segundo Ejercicio: ¿Cuál es el total de productos vendidos por mes? - Tercera Sección
SELECT 
  YEAR(ords.OrderDate) AS anio,
  MONTH(ords.OrderDate) AS mes,
  SUM(ordets.Quantity) AS tot_prods
FROM Orders ords
JOIN OrderDetails ordets
  ON ords.OrderID = ordets.OrderID
GROUP BY anio, mes
ORDER BY anio, mes;

-- Tercer Ejercicio: ¿Cuál fue el mejor mes en ventas del último año? - Tercera Sección
SELECT 
  DATE_FORMAT(ords.OrderDate, '%Y-%m') AS mes,
  SUM(ordets.UnitPrice * ordets.Quantity) AS tot_ventas
FROM Orders ords
JOIN OrderDetails ordets
  ON ords.OrderID = ordets.OrderID
WHERE ords.OrderDate >= (
  SELECT DATE_SUB(MAX(ords.OrderDate), INTERVAL 1 YEAR)
  FROM Orders ords
)
GROUP BY mes
ORDER BY tot_ventas DESC
LIMIT 1;

-- Cuarto Ejercicio: ¿Cuál es la evolución del gasto acumulado por cliente? - Tercera Sección
SELECT 
  cust.CustomerID,
  cust.CompanyName AS nombre,
  ords.OrderDate AS fecha,
  SUM(ordets.UnitPrice * ordets.Quantity) 
    OVER (PARTITION BY cust.CustomerID ORDER BY ords.OrderDate) AS gasto_acum
FROM Customers cust
JOIN Orders ords
  ON cust.CustomerID = ords.CustomerID
JOIN OrderDetails ordets
  ON ords.OrderID = ordets.OrderID
ORDER BY cust.CustomerID, ords.OrderDate;

-- Quinto Ejercicio: ¿Qué productos se repiten como más vendidos cada trimestre? - Tercera Sección
SELECT 
  anio,
  trimestre,
  ProductID,
  nombre,
  tot_vendido
FROM (
  SELECT 
    YEAR(ords.OrderDate) AS anio,
    QUARTER(ords.OrderDate) AS trimestre,
    pr.ProductID,
    pr.ProductName AS nombre,
    SUM(ordets.Quantity) AS tot_vendido,
    ROW_NUMBER() OVER (
      PARTITION BY YEAR(ords.OrderDate), QUARTER(ords.OrderDate)
      ORDER BY SUM(ordets.Quantity) DESC
    ) AS rn
  FROM Orders ords
  JOIN OrderDetails ordets
    ON ords.OrderID = ordets.OrderID
  JOIN Products pr
    ON ordets.ProductID = pr.ProductID
  GROUP BY anio, trimestre, pr.ProductID, nombre
) t
WHERE rn = 1;
