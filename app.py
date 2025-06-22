import streamlit as st
from pages import inicio, ventas, clientes, rendimiento

st.set_page_config(page_title="Northwind Dashboard", layout="wide")

# Menú lateral
st.sidebar.title("📊 Menú Principal")
opcion = st.sidebar.radio("Ir a sección:", ["Inicio", "Análisis de Ventas", "Comportamiento de Clientes", "Rendimiento y Optimización"])

# Renderizado dinámico de páginas
if opcion == "Inicio":
    inicio.mostrar()
elif opcion == "Análisis de Ventas":
    ventas.mostrar()
elif opcion == "Comportamiento de Clientes":
    clientes.mostrar()
elif opcion == "Rendimiento y Optimización":
    rendimiento.mostrar()