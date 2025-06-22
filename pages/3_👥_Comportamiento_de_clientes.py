import streamlit as st
import pandas as pd
import altair as alt
from db_config import get_connection

st.set_page_config(page_title="Comportamiento de Clientes", layout="wide")

st.markdown("""
<style>
    .metric-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
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
        <h1 style='font-size: 42px; color: #3366FF;'>Comportamiento de Clientes</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

conn = get_connection()

# --- Métricas destacadas ---
col1, col2 = st.columns(2)

# Porcentaje de clientes sin compras
query1 = """
SELECT 100 * COUNT(*)/(SELECT COUNT(*) FROM Customers) as pct 
FROM Customers cust
WHERE NOT EXISTS(
  SELECT 1
  FROM Orders ords
  WHERE ords.CustomerID = cust.CustomerID);
"""
df1 = pd.read_sql(query1, conn)
pct = round(df1['pct'][0], 2)
with col1:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-title'>% de clientes sin compras</div>
            <div class='metric-value'>{pct}%</div>
        </div>
    """, unsafe_allow_html=True)

# Clientes con 1 sola categoría
query4 = """
SELECT COUNT(*) AS clientes_una_categoria
FROM (
  SELECT cust.CustomerID, COUNT(DISTINCT pr.CategoryID) AS num_categorias
  FROM Customers cust
  JOIN Orders ords ON cust.CustomerID=ords.CustomerID
  JOIN OrderDetails ordets ON ords.OrderID=ordets.OrderID
  JOIN Products pr ON ordets.ProductID=pr.ProductID
  GROUP BY cust.CustomerID
  HAVING num_categorias=1
) sub;
"""
df4 = pd.read_sql(query4, conn)
with col2:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-title'>Clientes con 1 sola categoría</div>
            <div class='metric-value'>{df4['clientes_una_categoria'][0]}</div>
        </div>
    """, unsafe_allow_html=True)

# --- Top países con clientes activos ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>🌍 Top 5 países con más clientes activos</h2>", unsafe_allow_html=True)
query2 = """
SELECT c.Country, COUNT(DISTINCT c.CustomerID) AS num_clientes
FROM Customers c 
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.Country
ORDER BY num_clientes DESC
LIMIT 5;
"""
df2 = pd.read_sql(query2, conn)
fig2 = alt.Chart(df2).mark_bar().encode(
    x=alt.X('num_clientes:Q', title='Clientes'),
    y=alt.Y('Country:N', sort='-x', title='País'),
    color=alt.Color('num_clientes:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['Country', 'num_clientes']
).properties(
    width=700,
    height=300,
    title="Top 5 países con más clientes activos"
)
st.altair_chart(fig2, use_container_width=True)

with st.expander("📋 Ver tabla completa"):
    st.dataframe(df2.style.set_properties(**{
        'background-color': '#FFF5E6',
        'color': 'black'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

# --- Clientes que han comprado más de 10 productos ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>🛒 Clientes que han comprado más de 10 productos distintos</h2>", unsafe_allow_html=True)
query3 = """
SELECT c.CustomerID, c.CompanyName, COUNT(DISTINCT ordets.ProductID) AS DistinctProducts
FROM Customers c 
JOIN Orders ords ON c.CustomerID = ords.CustomerID
JOIN OrderDetails ordets ON ords.OrderID = ordets.OrderID
GROUP BY c.CustomerID, c.CompanyName
HAVING COUNT(DISTINCT ordets.ProductID) > 10
ORDER BY DistinctProducts DESC;
"""
df3 = pd.read_sql(query3, conn)
st.dataframe(df3[['CustomerID', 'CompanyName', 'DistinctProducts']].style.set_properties(**{
    'background-color': '#FFF5E6',
    'color': 'black'
}).set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
    {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
]), use_container_width=True)

# --- Ticket promedio por país ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>💳 Ticket promedio (global y por país)</h2>", unsafe_allow_html=True)

# Ticket promedio global
query5_global = """
SELECT AVG(t.total_orden) AS prom_ticket_global
FROM (
  SELECT ords.OrderID,SUM(ordets.UnitPrice*ordets.Quantity) AS total_orden
  FROM Orders ords
  JOIN OrderDetails ordets ON ords.OrderID=ordets.OrderID
  GROUP BY ords.OrderID
) t;
"""
df5g = pd.read_sql(query5_global, conn)
ticket_prom = f"${df5g['prom_ticket_global'][0]:,.2f}"
st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>Ticket promedio global</div>
        <div class='metric-value'>{ticket_prom}</div>
    </div>
""", unsafe_allow_html=True)

# Ticket promedio por país
ticket_query = """
SELECT t.Country,AVG(t.OrderTotal) AS prom_ticket_pais
FROM (
  SELECT ords.OrderID,cust.Country,SUM(ordets.UnitPrice*ordets.Quantity) AS OrderTotal
  FROM Customers cust
  JOIN Orders ords ON cust.CustomerID=ords.CustomerID
  JOIN OrderDetails ordets ON ords.OrderID=ordets.OrderID
  GROUP BY ords.OrderID,cust.Country
) t
GROUP BY t.Country
ORDER BY prom_ticket_pais DESC;
"""
df5p = pd.read_sql(ticket_query, conn)
df5p_top5 = df5p.head(5)
fig5 = alt.Chart(df5p_top5).mark_bar().encode(
    x=alt.X('prom_ticket_pais:Q', title='Promedio ($)'),
    y=alt.Y('Country:N', sort='-x', title='País'),
    color=alt.Color('prom_ticket_pais:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['Country', 'prom_ticket_pais']
).properties(
    width=700,
    height=300,
    title="Top 5 países por ticket promedio"
)
st.altair_chart(fig5, use_container_width=True)

with st.expander("📋 Ver ticket promedio por país"):
    st.dataframe(df5p.style.set_properties(**{
        'background-color': '#FFF5E6',
        'color': 'black'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

conn.close()
