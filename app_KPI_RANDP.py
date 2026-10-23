import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Control de Proyectos",
    page_icon="📊",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================

st.title("Equipo Automatizaciones")
st.write("Manejo de proyectos y avances.")

st.subheader("Integrantes")
st.write("• Rodriguez Meza Pablo Adair")
st.write("• Hernandez Caltenco Jadiel Roberto")

st.divider()

# =====================================
# ARCHIVO EXCEL
# =====================================

archivo = "control_proyectos.xlsx"

# =====================================
# CARGA DE DATOS
# =====================================

if Path(archivo).exists():

    try:
        df = pd.read_excel(
            archivo,
            engine="openpyxl"
        )

    except Exception as e:

        st.error(f"Error leyendo Excel: {e}")
        st.stop()

else:

    df = pd.DataFrame(
        {
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
        }
    )

# =====================================
# EDITOR DE PROYECTOS
# =====================================

st.header("📋 Control de Proyectos")

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
            step=1
        )
    }
)

# =====================================
# GUARDAR EXCEL
# =====================================

if st.button("💾 Guardar cambios"):

    try:

        with pd.ExcelWriter(
            archivo,
            engine="openpyxl"
        ) as writer:

            df_editado.to_excel(
                writer,
                index=False,
                sheet_name="Proyectos"
            )

        st.success("✅ Cambios guardados")

    except Exception as e:

        st.error(f"❌ Error al guardar: {e}")

# =====================================
# REPOSITORIO DOCUMENTAL
# =====================================

st.divider()

st.header("📁 Repositorio de Documentos")

# Inicializar almacenamiento

if "repositorio" not in st.session_state:
    st.session_state.repositorio = {}

# Selección de proyecto

proyecto = st.selectbox(
    "Selecciona un proyecto",
    df_editado["Tarea"].unique()
)

if proyecto not in st.session_state.repositorio:
    st.session_state.repositorio[proyecto] = []

# Cargar documentos

archivos_subidos = st.file_uploader(
    "Subir documentos",
    accept_multiple_files=True,
    type=[
        "pdf",
        "xlsx",
        "xls",
        "csv",
        "docx",
        "pptx",
        "png",
        "jpg",
        "jpeg",
        "txt"
    ]
)

# Guardar documentos

if archivos_subidos:

    for archivo_subido in archivos_subidos:

        existe = any(
            doc["nombre"] == archivo_subido.name
            for doc in st.session_state.repositorio[proyecto]
        )

        if not existe:

            st.session_state.repositorio[proyecto].append(
                {
                    "nombre": archivo_subido.name,
                    "tipo": archivo_subido.type,
                    "contenido": archivo_subido.getvalue()
                }
            )

    st.success("✅ Documentos agregados")

# =====================================
# LISTA DE DOCUMENTOS
# =====================================

st.subheader(f"📂 Documentos de: {proyecto}")

documentos = st.session_state.repositorio[proyecto]

if len(documentos) == 0:

    st.info("No hay documentos cargados para este proyecto.")

else:

    for i, doc in enumerate(documentos):

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"📄 {doc['nombre']}")

        with col2:

            st.download_button(
                label="⬇️",
                data=doc["contenido"],
                file_name=doc["nombre"],
                mime=doc["tipo"],
                key=f"descargar_{proyecto}_{i}"
            )

# =====================================
# RESUMEN
# =====================================

st.divider()

st.metric(
    "Total proyectos",
    len(df_editado)
)

st.metric(
    "Promedio avance (%)",
    round(df_editado["Avance"].mean(), 1)
)
