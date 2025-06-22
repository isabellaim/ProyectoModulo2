import streamlit as st
import pandas as pd
import altair as alt
from db_config import get_connection

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.markdown("""
<style>
    .metric-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #3366FF;
    }
    .metric-value {
        font-size: 22px;
        font-weight: bold;
        color: #F1962C;
    }
    .dataframe tbody tr th, .dataframe tbody td {
        background-color: #FFF5E6;
        color: #333;
    }
    .dataframe thead th {
        background-color: #003366;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='font-size: 42px; color: #3366FF;'>Análisis de Ventas</h1>
    </div>
""", unsafe_allow_html=True)

conn = get_connection()
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>Top 10 productos por ingresos</h2>", unsafe_allow_html=True)
query4 = """
SELECT pr.productname AS nombre, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS total_ganancia
FROM Products pr 
JOIN OrderDetails ordets ON pr.ProductID = ordets.ProductID
GROUP BY pr.ProductID
ORDER BY total_ganancia DESC 
LIMIT 10;
"""
df4 = pd.read_sql(query4, conn)

fig1 = alt.Chart(df4).mark_bar().encode(
    x=alt.X('total_ganancia:Q', title='Ingresos'),
    y=alt.Y('nombre:N', sort='-x', title='Producto'),
    color=alt.Color('total_ganancia:Q', scale=alt.Scale(scheme='blues'), legend=None),
    tooltip=['nombre', 'total_ganancia']
).properties(width=800, height=300)

st.altair_chart(fig1, use_container_width=True)
with st.expander("📋 Ver tabla completa"):
    st.dataframe(df4.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}))

st.markdown("---")

st.markdown("<h2 style='color: #F1962C;'>Ingresos por categoría (Top 5)</h2>", unsafe_allow_html=True)
query5 = """
SELECT c.CategoryName AS categoria, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS tot_ganancia
FROM Categories c 
JOIN Products pr ON c.CategoryID = pr.CategoryID 
JOIN OrderDetails ordets ON pr.ProductID = ordets.ProductID
GROUP BY categoria
ORDER BY tot_ganancia DESC 
LIMIT 5;
"""
df5 = pd.read_sql(query5, conn)

fig2 = alt.Chart(df5).mark_bar().encode(
    x=alt.X('tot_ganancia:Q', title='Ingresos'),
    y=alt.Y('categoria:N', sort='-x', title='Categoría'),
    color=alt.Color('tot_ganancia:Q', scale=alt.Scale(scheme='blues'), legend=None),
    tooltip=['categoria', 'tot_ganancia']
).properties(width=800, height=300)

st.altair_chart(fig2, use_container_width=True)
with st.expander("📋 Ver tabla completa"):
    st.dataframe(df5.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}))

st.markdown("---")

# Fila de KPIs al final
col1, col2, col3 = st.columns(3)

# Cliente con mayor valor de compras
query1 = """
SELECT cust.CompanyName, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS valor_total
FROM Customers cust 
JOIN Orders ords ON cust.CustomerID = ords.CustomerID 
JOIN OrderDetails ordets ON ordets.OrderID = ords.OrderID
GROUP BY cust.CustomerID
ORDER BY valor_total DESC 
LIMIT 1;
"""
df1 = pd.read_sql(query1, conn).iloc[0]
with col1:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Cliente Top Comprador</div>
        <div class='metric-value'>{df1['CompanyName']}</div>
        <p>Total: <strong>${df1['valor_total']:,.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

# País con mayores ingresos últimos 12 meses
query2 = """
SELECT cust.Country AS pais, 
       SUM(ordets.Quantity * ordets.UnitPrice) AS ingresos
FROM Customers cust 
JOIN Orders ords ON cust.CustomerID = ords.CustomerID 
JOIN OrderDetails ordets ON ordets.OrderID = ords.OrderID
WHERE ords.OrderDate >= (SELECT DATE_SUB(MAX(o.OrderDate), INTERVAL 12 MONTH) FROM Orders o)
GROUP BY pais
ORDER BY ingresos DESC 
LIMIT 1;
"""
df2 = pd.read_sql(query2, conn).iloc[0]
with col2:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>País con más ingresos (últ. 12 meses)</div>
        <div class='metric-value'>{df2['pais']}</div>
        <p>Total: <strong>${df2['ingresos']:,.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Empleado con más pedidos
query3 = """
SELECT e.FirstName AS nombre, e.LastName AS apellido, 
       COUNT(ords.OrderID) AS total_ordenes
FROM Employees e 
JOIN Orders ords ON e.EmployeeID = ords.EmployeeID
GROUP BY e.EmployeeID
ORDER BY total_ordenes DESC 
LIMIT 1;
"""
df3 = pd.read_sql(query3, conn).iloc[0]
with col3:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Empleado con más pedidos</div>
        <div class='metric-value'>{df3['nombre']} {df3['apellido']}</div>
        <p>Órdenes: <strong>{df3['total_ordenes']}</strong></p>
    </div>
    """, unsafe_allow_html=True)

conn.close()