import streamlit as st
import streamlit.components.v1 as components

st.title("📄 Proyecto Final – Resultados de Consultas SQL")

st.markdown("""
Este proyecto corresponde al trabajo final del módulo de SQL, y tiene como objetivo aplicar los conocimientos adquiridos para resolver 
preguntas de negocio utilizando la base de datos Northwind.

Northwind es una base de datos simulada que representa las operaciones de una empresa de distribución. Incluye información sobre 
productos, clientes, empleados, proveedores, órdenes y detalles de ventas.

A lo largo de este proyecto, se plantean consultas SQL agrupadas en tres secciones principales:

- 📦 Análisis de ventas: productos más vendidos, categorías rentables, países con mayor ingreso, entre otros.
- 👥 Comportamiento de clientes: porcentaje de clientes inactivos, ticket promedio, comportamiento por país, etc.
- 📊 Rendimiento y optimización: evolución de ventas, ranking de clientes, análisis temporal de productos.

Esta aplicación presenta exclusivamente los **resultados tabulares** de dichas consultas SQL ejecutadas sobre un servidor remoto (FreeSQLDatabase.com).
""")

st.subheader("👨‍👩‍👧 Integrantes del grupo")

col1, col2, col3 = st.columns(3)
with col1:
    st.image("images/Isabella.jpg", caption="Isabella Martín", width=150)
with col2:
    st.image("images/Juan.jpg", caption="Annabella Sánchez", width=300)
with col3:
    st.image("images/Annabella.jpg", caption="Juan Munizaga", width=150)

st.subheader("📚 Secciones del proyecto")

st.markdown("Selecciona una sección desde el menú lateral para ver los resultados de las consultas:")
st.markdown("""
- 📦 Análisis de ventas
- 👥 Comportamiento de clientes
- 📊 Rendimiento y optimización
""")
st.info("Utiliza el menú de la izquierda para navegar entre las secciones.")

components.html("""
<audio autoplay loop hidden>
  <source src="music/conejo_malo.mp3" type="audio/mp3">
</audio>
""", height=0)

