import streamlit as st
import pandas as pd
import numpy as np 
from pathlib import Path

# =====================================
# TÍTULO
# =====================================

st.title("Equipo Automatizaciones")
st.write("Manejo de proyectos y avances.")

# =====================================
# INTEGRANTES
# =====================================

st.subheader("Integrantes")

st.write("• Rodriguez Meza Pablo Adair")
st.write("• Hernandez Caltenco Jadiel Roberto")

st.divider()

# =====================================
# ARCHIVO EXCEL
# =====================================

archivo = "control_proyectos.xlsx"

# =====================================
# CARGAR DATOS
# =====================================

if Path(archivo).exists():
    df = pd.read_excel(archivo)
else:
    df = pd.DataFrame({
        "Tarea": [
            "Herramienta Caracterizadora PC 095 PI",
            "Dashboard Performance",
            "Asignación MELI"
        ],

        "Area/Equipo": [
            "Monse, Erick, Olga",
            "Antonio de Jesús",
            "Ana Fragoso"
        ],

        "Responsable": [
            "Pablo",
            "Roberto",
            "Pablo"
        ],

        "Fecha Entrega": [
            "2026-10-07",
            "2026-10-05",
            "2026-10-02"
        ],

        "Avance": [
            90,
            95,
            70
        ],

        "Status": [
            "En Revisión",
            "Pendiente",
            "Entregado"
        ],

        "Comentarios": [
            "Pendiente cerrar con equipo",
            "Mejoras",
            "Ver avance de código"
        ]
    })

# =====================================
# CONTROL DE PROYECTOS
# =====================================

st.title("Control de Proyectos")

df_editado = st.data_editor(
    df,
    hide_index=True,
    use_container_width=True,
    num_rows="dynamic",

    column_config={

        "Responsable": st.column_config.SelectboxColumn(
            "Responsable",
            options=[
                "Pablo",
                "Roberto",
                "Todos",
                "Otros"
            ]
        ),

        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=[
                "Pendiente",
                "En Curso",
                "En Revisión",
                "Entregado"
            ]
        ),

      "Avance": st.column_config.NumberColumn(
    "Avance (%)",
    min_value=0,
    max_value=100,
    step=1,
    format="%d"
)
    }
)

# =====================================
# GUARDAR CAMBIOS
# =====================================

if st.button("💾 Guardar cambios"):
    df_editado.to_excel(archivo, index=False)
    st.success("Cambios guardados correctamente")

st.divider()


