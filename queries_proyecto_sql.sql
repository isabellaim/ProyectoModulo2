use northwind;
-- Proyecto Final 
-- Nombres: Annabella Sánchez, Juan Munizaga, Isabella Martín
-- Primer Ejercicio - Primera Seccion
SELECT pr.productname as nombre, sum(ordets.Quantity * ordets.UnitPrice) as total_ganancia
FROM products pr join orderdetails ordets
on pr.ProductID = ordets.ProductID
group by pr.ProductID
order by total_ganancia desc LIMIT 10;

-- Segundo Ejercicio -- Primera Seccion
SELECT c.CategoryName as categoria, sum(ordets.Quantity * ordets.UnitPrice) as tot_ganancia
from categories c join products pr on c.CategoryID = pr.CategoryID 
join orderdetails ordets on pr.ProductID = ordets.ProductID
group by categoria
order by tot_ganancia desc limit 5;

-- Tercer Ejercicio: ¿Qué cliente ha realizado más compras en valor total? - Primera Seccion
SELECT cust.CompanyName, sum(ordets.Quantity * ordets.UnitPrice) as valor_total
from customers cust join orders ords on cust.CustomerID = ords.CustomerID 
join orderdetails ordets on ordets.OrderID = ords.OrderID
group by cust.CustomerID
order by valor_total desc limit 1;

-- Cuarto Ejercicio: ¿Qué país ha generado más ingresos en los últimos 12 meses? - Primera Seccion
SELECT cust.Country as pais, sum(ordets.Quantity * ordets.UnitPrice) as ingresos
from customers cust join orders ords on cust.CustomerID = ords.CustomerID 
join orderdetails ordets on ordets.OrderID = ords.OrderID
where ords.OrderDate >= (SELECT date_sub(MAX(o.OrderDate), INTERVAL 12 month)
						FROM orders o)
group by pais
order by ingresos desc limit 1;

-- Quinto ejercicio:  ¿Qué empleado ha gestionado la mayor cantidad de pedidos? - Primera Seccion
SELECT e.FirstName as nombre, e.LastName as apellido, count(ords.OrderID) as total_ordenes
from employees e join orders ords on e.EmployeeID = ords.EmployeeID
group by e.EmployeeID
order by total_ordenes DESC LIMIT 2;

-- Primer Ejercicio: ¿Qué porcentaje de clientes no ha comprado nada? - Segunda Sección
SELECT 100 * COUNT(*)/(SELECT COUNT(*) FROM Customers) as pct 
FROM Customers cust
WHERE NOT EXISTS(
SELECT 1
FROM Orders ords
WHERE ords.CustomerID = cust.CustomerID);

-- Segundo Ejercicio: ¿Cuáles son los 5 países con más clientes activos (que han realizado pedidos)? - Segunda Secion
SELECT c.Country, COUNT(DISTINCT c.CustomerID) AS num_clientes
FROM Customers c JOIN Orders o 
ON c.CustomerID = o.CustomerID
GROUP BY c.Country
ORDER BY num_clientes DESC
LIMIT 5;

-- Tercer Ejercicio: ¿Qué clientes han comprado más de 10 productos distintos? - segunda seccion
SELECT  c.CustomerID, c.CompanyName, COUNT(DISTINCT ordets.ProductID) AS DistinctProducts
FROM Customers c JOIN Orders ords ON c.CustomerID = ords.CustomerID
JOIN OrderDetails ordets ON ords.OrderID = ordets.OrderID
GROUP BY c.CustomerID, c.CompanyName
HAVING COUNT(DISTINCT ordets.ProductID) > 10
ORDER BY DistinctProducts DESC ;

-- Cuarto Ejercicio: ¿Hay clientes que compran solo un tipo de producto (una categoría)? - Segunda Sección
SELECT COUNT(*) AS clientes_una_categoria
FROM (
  SELECT cust.CustomerID, COUNT(DISTINCT pr.CategoryID) AS num_categorias
  FROM customers cust
  JOIN orders ords ON cust.CustomerID=ords.CustomerID
  JOIN orderDetails ordets ON ords.OrderID=ordets.OrderID
  JOIN products pr ON ordets.ProductID=pr.ProductID
  GROUP BY cust.CustomerID
  HAVING num_categorias=1
) sub;

-- Quinta Pregunta: ¿Cuál es el ticket promedio por pedido y cómo varía entre países? - Segunda Sección 
SELECT AVG(t.total_orden) AS prom_ticket_global
FROM (SELECT ords.OrderID,SUM(ordets.UnitPrice*ordets.Quantity) AS total_orden
      FROM orders ords
      JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
      GROUP BY ords.OrderID) t;

SELECT t.Country,AVG(t.OrderTotal) AS prom_ticket_pais
FROM (SELECT ords.OrderID,cust.Country,SUM(ordets.UnitPrice*ordets.Quantity) AS OrderTotal
      FROM Customers cust
      JOIN Orders ords ON cust.CustomerID=ords.CustomerID
      JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
      GROUP BY ords.OrderID,cust.Country) t
GROUP BY t.Country
ORDER BY prom_ticket_pais DESC;

-- Primer Ejercicio - ¿Cuál es el ranking de clientes por gasto total? - Tercera Seccion
SELECT cust.CustomerID,cust.CompanyName,SUM(ordets.UnitPrice*ordets.Quantity) AS total_gasto
FROM customers cust JOIN orders ords ON cust.CustomerID=ords.CustomerID
JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
GROUP BY cust.CustomerID,cust.CompanyName
ORDER BY total_gasto DESC;

-- Segundo Ejercicio: ¿Cuál es el total de productos vendidos por mes? - Tercera Seccion
SELECT YEAR(ords.OrderDate) AS anio,MONTH(ords.OrderDate) AS mes,SUM(ordets.Quantity) AS tot_prods
FROM orders ords JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
GROUP BY anio,mes
ORDER BY anio,mes;

-- Tercer Ejercicio: ¿Cuál fue el mejor mes en ventas del último año? - Tercera Seccion
SELECT DATE_FORMAT(ords.OrderDate,'%Y-%m') AS mes,SUM(ordets.UnitPrice*ordets.Quantity) AS tot_ventas
FROM orders ords JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
WHERE ords.OrderDate>=(SELECT date_sub(MAX(ords.OrderDate), INTERVAL 1 year)
						FROM orders ords)
GROUP BY mes
ORDER BY tot_ventas DESC LIMIT 1;

-- Cuarto Ejercicio: ¿Cuál es la evolución del gasto acumulado por cliente? - Tercera Seccion
WITH order_totals AS (
  SELECT cust.CustomerID, cust.CompanyName AS nombre, ords.OrderID, ords.OrderDate AS fecha,
  SUM(ordets.UnitPrice * ordets.Quantity) AS order_total
  FROM customers cust JOIN orders ords ON cust.CustomerID = ords.CustomerID
  JOIN orderdetails ordets  ON ords.OrderID = ordets.OrderID
  GROUP BY cust.CustomerID, cust.CompanyName, ords.OrderID, ords.OrderDate
)
SELECT CustomerID, nombre, fecha, order_total, SUM(order_total) 
    OVER (PARTITION BY CustomerID ORDER BY fecha
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS gasto_acum
FROM order_totals
ORDER BY CustomerID, fecha;

-- Quinto Ejercicio - ¿Qué productos se repiten como más vendidos cada trimestre? - Tercera Seccion
SELECT anio,trimestre,ProductID,nombre,tot_vendido FROM(
SELECT YEAR(ords.OrderDate) AS anio,QUARTER(ords.OrderDate) AS trimestre,
        pr.ProductID,pr.ProductName as nombre,
        SUM(ordets.Quantity) AS tot_vendido,
        ROW_NUMBER() OVER(
		PARTITION BY YEAR(ords.OrderDate),QUARTER(ords.OrderDate) 
        ORDER BY SUM(ordets.Quantity) DESC) AS rn
 FROM orders ords
 JOIN orderdetails ordets ON ords.OrderID=ordets.OrderID
 JOIN products pr ON ordets.ProductID=pr.ProductID
 GROUP BY anio,trimestre,pr.ProductID,nombre
) t WHERE rn=1;