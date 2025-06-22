import streamlit as st

st.set_page_config(page_title="Inicio", layout="wide")

st.title("📊 Proyecto Final – Análisis con SQL")

st.markdown("""
Este proyecto corresponde al trabajo final del módulo de **SQL**, donde aplicamos consultas para resolver preguntas de negocio utilizando la base de datos **Northwind**.

La base incluye información sobre productos, clientes, empleados, proveedores, órdenes y ventas, lo que nos permite explorar y obtener **conclusiones clave del negocio** a partir de datos simulados.

La aplicación presenta resultados agrupados en tres secciones:

- 📦 Análisis de ventas  
- 👥 Comportamiento de clientes  
- 📈 Rendimiento y optimización  
""")

st.divider()
st.markdown("## 🧑‍🤝‍🧑 Integrantes del grupo")

cols = st.columns(3)
integrantes = [
    {"nombre": "Isabella Martín", "foto": "images/isabella.jpg"},
    {"nombre": "Annabella Sánchez", "foto": "images/annabella.jpg"},
    {"nombre": "Juan Munizaga", "foto": "images/juan.jpg"}
]

for col, integrante in zip(cols, integrantes):
    with col:
        st.image(integrante["foto"], width=180, caption=integrante["nombre"])

st.divider()
st.info("ℹ️ Utiliza el menú lateral para explorar los resultados de las distintas secciones.")
