import streamlit as st
import mysql.connector

def get_connection():
    creds = st.secrets["mysql"]
    return mysql.connector.connect(
        host=creds["host"],
        user=creds["user"],
        password=creds["password"],
        database=creds["database"],
        port=creds["port"]
    )
