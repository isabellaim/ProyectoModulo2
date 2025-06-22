import streamlit as st
import pandas as pd
from db_config import get_connection

# Configurar diseño ancho
st.set_page_config(layout="wide")
st.title("📦 Análisis de Ventas")

conn = get_connection()

# ---------- Ejercicio 1 ----------
st.markdown("### 🏆 Top 10 productos por ingresos")
query1 = """
SELECT pr.productname AS nombre, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS total_ganancia
FROM Products pr 
JOIN OrderDetails ordets ON pr.ProductID = ordets.ProductID
GROUP BY pr.ProductID
ORDER BY total_ganancia DESC 
LIMIT 10;
"""
df1 = pd.read_sql(query1, conn)
df1["total_ganancia"] = df1["total_ganancia"].round(2)

for i in range(0, len(df1), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(df1):
            row = df1.iloc[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div style="
                        background-color: #f0f4ff; 
                        padding: 25px; 
                        border-radius: 12px; 
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        margin: 10px 0;
                        height: 150px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <h5 style="margin: 0 0 10px 0;">📦 <strong>{row['nombre']}</strong></h5>
                        <p style="font-size: 20px; color: #3366ff; margin: 0;"><strong>${row['total_ganancia']:,.2f}</strong></p>
                    </div>
                """, unsafe_allow_html=True)

# ---------- Ejercicio 2 ----------
st.markdown("---")
st.markdown("### 📂 Ingresos por categoría (Top 5)")
query2 = """
SELECT c.CategoryName AS categoria, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS tot_ganancia
FROM Categories c 
JOIN Products pr ON c.CategoryID = pr.CategoryID 
JOIN OrderDetails ordets ON pr.ProductID = ordets.ProductID
GROUP BY categoria
ORDER BY tot_ganancia DESC 
LIMIT 5;
"""
df2 = pd.read_sql(query2, conn)
df2["tot_ganancia"] = df2["tot_ganancia"].round(2)
for i in range(0, len(df2), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(df2):
            row = df2.iloc[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div style="
                        background-color: #fef6e4; 
                        padding: 25px; 
                        border-radius: 12px; 
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        margin: 10px 0;
                        height: 130px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <h5 style="margin: 0 0 10px 0;">🗂️ <strong>{row['categoria']}</strong></h5>
                        <p style="font-size: 20px; color: #e67e22; margin: 0;"><strong>${row['tot_ganancia']:,.2f}</strong></p>
                    </div>
                """, unsafe_allow_html=True)

# ---------- Ejercicio 3 ----------
st.markdown("---")
st.markdown("### 👤 Cliente con mayor valor de compras")
query3 = """
SELECT cust.CompanyName, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS valor_total
FROM Customers cust 
JOIN Orders ords ON cust.CustomerID = ords.CustomerID 
JOIN OrderDetails ordets ON ordets.OrderID = ords.OrderID
GROUP BY cust.CustomerID
ORDER BY valor_total DESC 
LIMIT 1;
"""
df3 = pd.read_sql(query3, conn)
cliente = df3.iloc[0]
st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px;">
        <h4>🏅 {cliente['CompanyName']}</h4>
        <p style="font-size: 18px;">Total en compras: <strong>${cliente['valor_total']:,.2f}</strong></p>
    </div>
""", unsafe_allow_html=True)

# ---------- Ejercicio 4 ----------
st.markdown("---")
st.markdown("### 🌍 País con mayores ingresos (últimos 12 meses)")
query4 = """
SELECT cust.Country AS pais, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS ingresos
FROM Customers cust 
JOIN Orders ords ON cust.CustomerID = ords.CustomerID 
JOIN OrderDetails ordets ON ordets.OrderID = ords.OrderID
WHERE ords.OrderDate >= (
    SELECT DATE_SUB(MAX(o.OrderDate), INTERVAL 12 MONTH)
    FROM Orders o)
GROUP BY pais
ORDER BY ingresos DESC 
LIMIT 1;
"""
df4 = pd.read_sql(query4, conn)
pais = df4.iloc[0]
st.markdown(f"""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px;">
        <h4>🌐 País: {pais['pais']}</h4>
        <p style="font-size: 18px;">Ingresos en 12 meses: <strong>${pais['ingresos']:,.2f}</strong></p>
    </div>
""", unsafe_allow_html=True)

# ---------- Ejercicio 5 ----------
st.markdown("---")
st.markdown("### 🧑‍💼 Empleados con más pedidos gestionados")
query5 = """
SELECT e.FirstName AS nombre, 
       e.LastName AS apellido, 
       COUNT(ords.OrderID) AS total_ordenes
FROM Employees e 
JOIN Orders ords ON e.EmployeeID = ords.EmployeeID
GROUP BY e.EmployeeID
ORDER BY total_ordenes DESC 
LIMIT 1;
"""

df5 = pd.read_sql(query5, conn)
empleado = df5.iloc[0]
st.markdown(f"""
    <div style="background-color: #f3e5f5; padding: 20px; border-radius: 10px;">
        <h4>👔 {empleado['nombre']} {empleado['apellido']}</h4>
        <p style="font-size: 18px;">Total de órdenes gestionadas: <strong>{empleado['total_ordenes']}</strong></p>
    </div>
""", unsafe_allow_html=True)
conn.close()
