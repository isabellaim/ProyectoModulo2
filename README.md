# Proyecto Final: Análisis Interactivo de la Base de Datos Northwind

## Descripción
Este repositorio contiene un proyecto de análisis de la base de datos **Northwind** que simula las operaciones de una empresa de distribución. A través de una aplicación web desarrollada con **Streamlit** y conectada a una base de datos **MySQL** alojada en FreeSQLDatabase.com, podrás:

- Visualizar en tiempo real KPIs clave (productos más vendidos, clientes top, evolución mensual de ingresos).  
- Filtrar por periodos, categorías, clientes y empleados.  
- Revisar consultas SQL optimizadas con CTEs, índices y análisis de **EXPLAIN**.  
- Explorar pestañas independientes para cada sección de análisis.

## Tabla de Contenidos
1. [Requisitos](#requisitos)  
2. [Instalación y puesta en marcha](#instalación-y-puesta-en-marcha)  
3. [Estructura del proyecto](#estructura-del-proyecto)  
4. [Uso de la aplicación](#uso-de-la-aplicación)  

---

## Requisitos
- Python 3.8+  
- pip  
- Cuenta gratuita en [FreeSQLDatabase.com](https://freesqldatabase.com)  
- MySQL Workbench (o cliente equivalente)  

---

## Instalación y puesta en marcha
1. **Clona este repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/northwind-streamlit.git
   cd northwind-streamlit
   ```

2. **Crea y activa un entorno virtual**
    ```bash
    python3 -m venv venv
    # En Linux/macOS:
    source venv/bin/activate
    # En Windows PowerShell:
    .\venv\Scripts\Activate.ps1
    ```

3. **Instala las dependencias**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Ejecuta la app**
    ```bash
    streamlit run 🏠_Inicio.py
    ```

## Estructura del proyecto
```
.
├── README.md
├── __pycache__
│   └── db_config.cpython-311.pyc
├── db_config.py
├── images
│   ├── Annabella.jpg
│   ├── Isabella.jpg
│   └── Juan.jpg
├── music
│   └── conejo_malo.mp3
├── pages
│   ├── 2_📦_Análisis_de_ventas.py
│   ├── 3_👥_Comportamiento_de_clientes.py
│   ├── 4_📊_Rendimiento_y_optimización.py
│   └── __pycache__
│       ├── clientes.cpython-311.pyc
│       ├── inicio.cpython-311.pyc
│       ├── rendimiento.cpython-311.pyc
│       └── ventas.cpython-311.pyc
├── queries_proyecto_sql.sql
├── requirements.txt
└── 🏠_Inicio.py
```

## Uso de la aplicación
Al iniciar la app verás en la barra lateral las pestañas:

1. **Análisis de ventas:** Top productos, ingresos por categoría, mejores clientes y países.

2. **Comportamiento de clientes:** Clientes inactivos, países con más clientes, diversidad de compras.

3. **Rendimiento y optimización:** Ranking por gasto, ventas mensuales, mejor mes del año, análisis trimestral.

Cada pestaña:

- Ejecuta una o varias consultas SQL documentadas.

- Muestra tablas y gráficos generados con Pandas y Streamlit.

- Incluye interpretación de resultados.