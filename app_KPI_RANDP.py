import streamlit as st
import pandas as pd
from pathlib import Path
import os
import io
import zipfile

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
st.write("Manejo de proyectos y avances")

st.subheader("Integrantes")
st.write("• Rodriguez Meza Pablo Adair")
st.write("• Hernandez Caltenco Jadiel Roberto")

st.divider()

# =====================================
# ARCHIVO EXCEL
# =====================================

archivo_excel = "control_proyectos.xlsx"

# =====================================
# REPOSITORIO DOCUMENTAL
# =====================================

CARPETA_DOCS = "repositorio_documentos"
os.makedirs(CARPETA_DOCS, exist_ok=True)

# =====================================
# CARGAR DATOS
# =====================================

if Path(archivo_excel).exists():

    try:

        df = pd.read_excel(
            archivo_excel,
            engine="openpyxl"
        )

    except Exception as e:

        st.error(
            f"Error leyendo Excel: {e}"
        )

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
# MÉTRICAS
# =====================================

st.header("📋 Control de Proyectos")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Proyectos",
        len(df)
    )

with col2:

    promedio = 0

    if len(df) > 0:
        promedio = round(
            df["Avance"].mean(),
            1
        )

    st.metric(
        "Promedio Avance",
        f"{promedio}%"
    )

with col3:

    entregados = len(
        df[df["Status"] == "Entregado"]
    )

    st.metric(
        "Entregados",
        entregados
    )

# =====================================
# EDITOR
# =====================================

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
            archivo_excel,
            engine="openpyxl"
        ) as writer:

            df_editado.to_excel(
                writer,
                sheet_name="Proyectos",
                index=False
            )

        st.success(
            "✅ Cambios guardados correctamente"
        )

    except Exception as e:

        st.error(
            f"❌ Error al guardar: {e}"
        )

# =====================================
# REPOSITORIO DOCUMENTAL
# =====================================

st.divider()

st.header("📁 Repositorio de Documentos")

if len(df_editado) > 0:

    proyectos_validos = df_editado[
        "Tarea"
    ].dropna().unique()

    if len(proyectos_validos) > 0:

        proyecto = st.selectbox(
            "Selecciona un proyecto",
            proyectos_validos
        )

        nombre_carpeta = "".join(
            c for c in proyecto
            if c.isalnum() or c in (
                " ",
                "-",
                "_"
            )
        ).strip()

        ruta_proyecto = os.path.join(
            CARPETA_DOCS,
            nombre_carpeta
        )

        os.makedirs(
            ruta_proyecto,
            exist_ok=True
        )

        # =============================
        # SUBIR DOCUMENTOS
        # =============================

        archivos_subidos = st.file_uploader(
            f"Subir documentos para: {proyecto}",
            accept_multiple_files=True,
            type=[
                "pdf",
                "xlsx",
                "xls",
                "csv",
                "docx",
                "pptx",
                "txt",
                "png",
                "jpg",
                "jpeg",
                "zip"
            ]
        )

        if archivos_subidos:

            for archivo in archivos_subidos:

                try:

                    # ZIP

                    if archivo.name.lower().endswith(
                        ".zip"
                    ):

                        zip_bytes = io.BytesIO(
                            archivo.getvalue()
                        )

                        with zipfile.ZipFile(
                            zip_bytes,
                            "r"
                        ) as zip_ref:

                            zip_ref.extractall(
                                ruta_proyecto
                            )

                        st.success(
                            f"✅ ZIP cargado: {archivo.name}"
                        )

                    # ARCHIVO NORMAL

                    else:

                        ruta_archivo = os.path.join(
                            ruta_proyecto,
                            archivo.name
                        )

                        with open(
                            ruta_archivo,
                            "wb"
                        ) as f:

                            f.write(
                                archivo.getbuffer()
                            )

                        st.success(
                            f"✅ Archivo guardado: {archivo.name}"
                        )

                except Exception as e:

                    st.error(
                        f"Error cargando {archivo.name}: {e}"
                    )

        # =============================
        # LISTAR DOCUMENTOS
        # =============================

        st.subheader(
            "📂 Documentos disponibles"
        )

        archivos = []

        for raiz, carpetas, ficheros in os.walk(
            ruta_proyecto
        ):

            for fichero in ficheros:

                ruta_relativa = os.path.relpath(
                    os.path.join(
                        raiz,
                        fichero
                    ),
                    ruta_proyecto
                )

                archivos.append(
                    ruta_relativa
                )

        archivos.sort()

        if archivos:

            for archivo in archivos:

                ruta_archivo = os.path.join(
                    ruta_proyecto,
                    archivo
                )

                col1, col2, col3 = st.columns(
                    [6, 1, 1]
                )

                with col1:

                    st.write(
                        f"📄 {archivo}"
                    )

                with col2:

                    with open(
                        ruta_archivo,
                        "rb"
                    ) as f:

                        st.download_button(
                            "⬇️",
                            data=f.read(),
                            file_name=os.path.basename(
                                archivo
                            ),
                            key=f"download_{archivo}"
                        )

                with col3:

                    if st.button(
                        "🗑️",
                        key=f"delete_{archivo}"
                    ):

                        os.remove(
                            ruta_archivo
                        )

                        st.rerun()

        else:

            st.info(
                "No existen documentos para este proyecto."
            )

else:

    st.warning(
        "Agrega al menos un proyecto para utilizar el repositorio documental."
    )
