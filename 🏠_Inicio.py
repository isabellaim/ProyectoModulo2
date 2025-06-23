import streamlit as st
import json
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Inicio", layout="wide")

# --- Función para cargar animación desde archivo ---
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Cargar animaciones individuales para cada sección
anim_ventas = load_lottie("assets/aniVentas.json")
anim_clientes = load_lottie("assets/aniClientes.json")
anim_rendimiento = load_lottie("assets/aniRendimiento.json")

# --- Título principal ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='font-size: 42px; color: #3366FF;'>Proyecto Final – Análisis con SQL</h1>
        <p style='font-size: 18px; color: #555;'>Exploración interactiva de datos con la base Northwind</p>
    </div>
""", unsafe_allow_html=True)

# --- Animación debajo del título ---
st_lottie(load_lottie("assets/aniDB.json"), speed=1, height=300, loop=True)

# --- Descripción del proyecto ---
st.markdown("""
<div style='text-align: justify; font-size: 16px;'>
Este proyecto corresponde al trabajo final del módulo de <strong>SQL</strong>, donde aplicamos consultas para resolver preguntas de negocio utilizando la base de datos <strong>Northwind</strong>.<br><br>
La base incluye información sobre productos, clientes, empleados, proveedores, órdenes y ventas, lo que nos permite explorar y obtener <strong>conclusiones clave del negocio</strong> a partir de datos reales.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Secciones con tarjetas y animaciones ---
st.markdown("<h2 style='color: #F1962C;'>Secciones principales del análisis</h2>", unsafe_allow_html=True)

section_cols = st.columns(3)

with section_cols[0]:
    st_lottie(anim_ventas, height=160, key="ventas")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 140px;'>
            <h5>Análisis de ventas</h5>
            <p style='font-size: 14px;'>Productos, categorías y países más rentables</p>
        </div>
    """, unsafe_allow_html=True)

with section_cols[1]:
    st_lottie(anim_clientes, height=160, key="clientes")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 140px;'>
            <h5>Comportamiento de clientes</h5>
            <p style='font-size: 14px;'>Inactividad, ticket promedio, patrones</p>
        </div>
    """, unsafe_allow_html=True)

with section_cols[2]:
    st_lottie(anim_rendimiento, height=160, key="rendimiento")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 140px;'>
            <h5>Rendimiento y optimización</h5>
            <p style='font-size: 14px;'>Evolución temporal, ranking, eficiencia</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.info("ℹ️ Usa el menú lateral (sidebar) para navegar por las secciones del proyecto.")

st.markdown("---")

# --- Integrantes ---
st.markdown("<h2 style='color: #F1962C;'>Integrantes del grupo</h2>", unsafe_allow_html=True)

cols = st.columns(3)
integrantes = [
    {"nombre": "Isabella Martín", "foto": "images/isabellaOficial.jpg"},
    {"nombre": "Annabella Sánchez", "foto": "images/annabellaOficial.jpg"},
    {"nombre": "Juan Munizaga", "foto": "images/juanOficial.jpg"}
]

for col, integrante in zip(cols, integrantes):

    with col:
        st.image(integrante["foto"], width=150, caption=f"{integrante['nombre']}", use_column_width=True)