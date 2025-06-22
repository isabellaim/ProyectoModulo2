import streamlit as st
import pandas as pd
from db_config import get_connection

st.title("📦 Análisis de ventas")

st.subheader("🔝 Top 10 productos por ingresos")

query = """
SELECT 
    p.ProductName,
    SUM(od.UnitPrice * od.Quantity) AS TotalIngresos
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalIngresos DESC
LIMIT 10;
"""

try:
    conn = get_connection()
    df = pd.read_sql(query, conn)
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
