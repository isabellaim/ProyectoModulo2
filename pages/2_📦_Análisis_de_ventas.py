import streamlit as st
import pandas as pd
from db_config import get_connection
import streamlit.components.v1 as components

# Configurar diseño ancho y título
st.set_page_config(layout="wide")
st.title("📦 Análisis de Ventas")
conn = get_connection()

# ------------------------------------------------------------
# Función genérica que inyecta un botón “Ver SQL” y, al clic,
# agrega un backdrop y un modal sobre toda la página padre
def ver_sql(query: str, key: str):
    # Escapamos cualquier backtick para no romper la template literal JS
    safe_query = query.strip().replace("`", "\\`")
    html = f"""
    <div>
      <button id="show-{key}" style="
        background:none;
        border:none;
        cursor:pointer;
        color:#3366ff;
        font-size:16px;
      ">📝 Ver SQL</button>
    </div>
    <script>
    (function() {{
      const query = `{safe_query}`;
      document.getElementById("show-{key}").onclick = function() {{
        const p = window.parent.document;
        // Si ya existe, no hacemos nada
        if (p.getElementById("sql-backdrop-{key}")) return;

        // Creamos el fondo semitransparente
        const backdrop = p.createElement("div");
        backdrop.id = "sql-backdrop-{key}";
        backdrop.style.cssText =
          "position:fixed;top:0;left:0;width:100%;height:100%;" +
          "background:rgba(0,0,0,0.5);z-index:9998;";
        p.body.appendChild(backdrop);

        // Creamos el modal
        const modal = p.createElement("div");
        modal.id = "sql-modal-{key}";
        modal.style.cssText =
          "position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);" +
          "background:#fff;padding:20px;border-radius:8px;" +
          "box-shadow:0 4px 20px rgba(0,0,0,0.3);" +
          "z-index:9999;max-width:80vw;max-height:80vh;overflow:auto;";
        
        // Pre con la consulta
        const pre = p.createElement("pre");
        pre.textContent = query;
        pre.style.cssText =
          "background:#f5f5f5;padding:10px;border-radius:6px;" +
          "font-family:monospace;white-space:pre-wrap;margin:0;";
        modal.appendChild(pre);

        // Botón Cerrar
        const btn = p.createElement("button");
        btn.textContent = "Cerrar";
        btn.style.cssText =
          "margin-top:10px;padding:6px 12px;border:none;" +
          "background:#3366ff;color:#fff;border-radius:4px;cursor:pointer;";
        btn.onclick = () => {{ backdrop.remove(); modal.remove(); }};
        modal.appendChild(btn);

        p.body.appendChild(modal);
      }};
    }})();
    </script>
    """
    # Iframe muy pequeño que solo muestra el botón
    components.html(html, height=40, width=120, scrolling=False)


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
# Columnas: título + botón
col1, col2 = st.columns([9,1])
with col1:
    st.write("")  # ya está el markdown arriba
with col2:
    ver_sql(query1, key="ejer1")

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
col1, col2 = st.columns([9,1])
with col1:
    st.write("") 
with col2:
    ver_sql(query2, key="ejer2")

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
col1, col2 = st.columns([9,1])
with col1:
    st.write("") 
with col2:
    ver_sql(query3, key="ejer3")

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
col1, col2 = st.columns([9,1])
with col1:
    st.write("") 
with col2:
    ver_sql(query4, key="ejer4")

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
col1, col2 = st.columns([9,1])
with col1:
    st.write("") 
with col2:
    ver_sql(query5, key="ejer5")

df5 = pd.read_sql(query5, conn)
empleado = df5.iloc[0]
st.markdown(f"""
    <div style="background-color: #f3e5f5; padding: 20px; border-radius: 10px;">
        <h4>👔 {empleado['nombre']} {empleado['apellido']}</h4>
        <p style="font-size: 18px;">Total de órdenes gestionadas: <strong>{empleado['total_ordenes']}</strong></p>
    </div>
""", unsafe_allow_html=True)

# Cerrar conexión
conn.close()
