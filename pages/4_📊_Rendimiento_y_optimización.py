import streamlit as st
import pandas as pd
import altair as alt
from db_config import get_connection
import utils as U

st.set_page_config(page_title="Rendimiento y Optimización", layout="wide")

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
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        flex: 1 1 calc(50% - 2rem);
        min-width: 280px;
        max-width: 420px;
    }
    .card h4 {
        font-size: 18px;
        color: #3366FF;
        margin-bottom: 0.5rem;
    }
    .card p {
        font-size: 24px;
        color: #F1962C;
        margin: 0;
        font-weight: bold;
    }
    .card small {
        font-size: 16px;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='font-size: 42px; color: #3366FF;'>Rendimiento y Optimización</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

conn = get_connection()
version_df = pd.read_sql("SELECT VERSION() AS version;", conn)
print("Versión de MySQL:", version_df["version"][0])

# --- Ejercicio 1 ---
st.markdown("<h2 style='color: #F1962C;'>Ranking de clientes por gasto total</h2>", unsafe_allow_html=True)
query1 = """
SELECT cust.CustomerID, cust.CompanyName, SUM(ordets.UnitPrice * ordets.Quantity) AS total_gasto
FROM Customers cust 
JOIN Orders ords ON cust.CustomerID = ords.CustomerID
JOIN OrderDetails ordets ON ords.OrderID = ordets.OrderID
GROUP BY cust.CustomerID, cust.CompanyName
ORDER BY total_gasto DESC;
"""
df1 = pd.read_sql(query1, conn)
top5 = df1.head(5)

col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    U.ver_sql(query1, key="ejer1")

# Estilos más compactos
st.markdown("""
<style>
.card-uno {
    background-color: #ffffff;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
    text-align: center;
    margin: 1rem auto;
    max-width: 500px;
    width: 92%;
}
.card-uno h4 {
    font-size: 17px;
    color: #3366FF;
    margin-bottom: 0.3rem;
}
.card-uno p {
    font-size: 22px;
    font-weight: bold;
    color: #F1962C;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

for index, row in top5.iterrows():
    st.markdown(f"""
        <div class="card-uno">
            <h4>🔹 #{index+1} {row['CompanyName']}</h4>
            <p>${row['total_gasto']:,.2f}</p>
        </div>
    """, unsafe_allow_html=True)

with st.expander("📋 Ver tabla completa"):
    st.dataframe(df1.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

# --- Ejercicio 2 ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>Total de productos vendidos por mes</h2>", unsafe_allow_html=True)
query2 = """
SELECT YEAR(ords.OrderDate) AS anio, MONTH(ords.OrderDate) AS mes, SUM(ordets.Quantity) AS tot_prods
FROM Orders ords 
JOIN OrderDetails ordets ON ords.OrderID = ordets.OrderID
GROUP BY anio, mes
ORDER BY anio, mes;
"""
df2 = pd.read_sql(query2, conn)

col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    U.ver_sql(query2, key="ejer2")

df2['mes_nombre'] = pd.to_datetime(df2['mes'], format='%m').dt.strftime('%B')
df2['anio_mes'] = df2['anio'].astype(str) + ' - ' + df2['mes_nombre']
fig2 = alt.Chart(df2).mark_line(point=True).encode(
    x=alt.X('anio_mes:N', sort=None, title='Mes'),
    y='tot_prods:Q',
    tooltip=['anio_mes', 'tot_prods']
).properties(title="Total de productos vendidos por mes", width=800, height=300)
st.altair_chart(fig2, use_container_width=True)
with st.expander("📋 Ver tabla completa"):
    st.dataframe(df2.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

# --- Ejercicio 3 ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>Mejor mes en ventas del último año</h2>", unsafe_allow_html=True)
query3 = """
SELECT DATE_FORMAT(ords.OrderDate,'%Y-%m') AS mes, SUM(ordets.UnitPrice * ordets.Quantity) AS tot_ventas
FROM Orders ords 
JOIN OrderDetails ordets ON ords.OrderID = ordets.OrderID
WHERE ords.OrderDate >= (
    SELECT DATE_SUB(MAX(ords.OrderDate), INTERVAL 1 year) FROM Orders ords)
GROUP BY mes
ORDER BY tot_ventas DESC 
LIMIT 1;
"""
df3 = pd.read_sql(query3, conn)

col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    U.ver_sql(query3, key="ejer3")

mejor_mes = df3.iloc[0]
st.markdown("""
<div class='metric-box'>
    <div class='metric-title'>Mejor mes en ventas</div>
    <div class='metric-value'>{}</div>
    <p>Total: <strong>${:,.2f}</strong></p>
</div>
""".format(mejor_mes['mes'], mejor_mes['tot_ventas']), unsafe_allow_html=True)

# --- Ejercicio 4 ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>Evolución del gasto acumulado por cliente</h2>", unsafe_allow_html=True)
df4 = pd.read_csv("csvs/pregunta4_terceraseccion.csv")
query4 = """WITH order_totals AS (
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
ORDER BY CustomerID, fecha;"""

col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    U.ver_sql(query4, key="ejer4")

cliente_col = df4.columns[df4.columns.str.lower().str.contains("nombre")]
if not cliente_col.empty:
    cliente_key = cliente_col[0]
else:
    st.error("No se encontró la columna 'nombre' en el archivo CSV.")
    cliente_key = df4.columns[0]  # fallback

clientes = df4[cliente_key].unique()
cliente_sel = st.selectbox("Selecciona un cliente", clientes)
df_cliente = df4[df4[cliente_key] == cliente_sel]
df_cliente['fecha'] = pd.to_datetime(df_cliente['fecha'])
fig4 = alt.Chart(df_cliente).mark_line(point=True).encode(
    x='fecha:T',
    y='gasto_acum:Q',
    tooltip=['fecha', 'gasto_acum']
).properties(title=f"Evolución de gasto: {cliente_sel}", width=800, height=300)
st.altair_chart(fig4, use_container_width=True)
with st.expander("📋 Ver tabla del cliente"):
    st.dataframe(df_cliente.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)
with st.expander("📋 Ver tabla de todos los clientes"):
    st.dataframe(df4.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

# --- Ejercicio 5 ---
st.markdown("---")
st.markdown("<h2 style='color: #F1962C;'>Productos más vendidos por trimestre</h2>", unsafe_allow_html=True)
df5 = pd.read_csv("csvs/pregunta5_terceraseccion.csv")

query5= """SELECT anio,trimestre,ProductID,nombre,tot_vendido FROM(
SELECT YEAR(ords.OrderDate) AS anio,QUARTER(ords.OrderDate) AS trimestre,
        pr.ProductID,pr.ProductName as nombre,
        SUM(ordets.Quantity) AS tot_vendido,
        ROW_NUMBER() OVER(
		PARTITION BY YEAR(ords.OrderDate),QUARTER(ords.OrderDate) 
        ORDER BY SUM(ordets.Quantity) DESC) AS rn
 FROM Orders ords
 JOIN OrderDetails ordets ON ords.OrderID=ordets.OrderID
 JOIN Products pr ON ordets.ProductID=pr.ProductID
 GROUP BY anio,trimestre,pr.ProductID,nombre
) t WHERE rn=1;"""
col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    U.ver_sql(query5, key="ejer5")

df5.rename(columns=lambda x: x.lower(), inplace=True)
df5['anio_trimestre'] = df5['anio'].astype(str) + ' - Q' + df5['trimestre'].astype(str)
fig5 = alt.Chart(df5).mark_bar().encode(
    x='anio_trimestre:N',
    y='tot_vendido:Q',
    color=alt.Color('trimestre:N', scale=alt.Scale(scheme='blues')),
    tooltip=['anio', 'trimestre', 'nombre', 'tot_vendido']
).properties(title="Productos más vendidos por trimestre", width=800, height=300)
st.altair_chart(fig5, use_container_width=True)
with st.expander("📋 Ver tabla completa"):
    st.dataframe(df5.style.set_properties(**{'background-color': '#FFF5E6', 'color': 'black'}).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#003366'), ('color', 'white')]},
        {'selector': 'thead tr', 'props': [('font-weight', 'bold')]}
    ]), use_container_width=True)

conn.close()
