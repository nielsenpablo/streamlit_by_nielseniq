# =====================================
# REPOSITORIO DE DOCUMENTOS
# =====================================

st.divider()
st.subheader("📁 Repositorio de Documentos")

# Selección de proyecto
proyecto = st.selectbox(
    "Proyecto",
    df_editado["Tarea"].unique()
)

# Cargar archivos
archivos_subidos = st.file_uploader(
    f"Subir documentos para: {proyecto}",
    accept_multiple_files=True,
    type=["pdf", "docx", "xlsx", "csv", "png", "jpg", "jpeg"]
)

# Inicializar almacenamiento en sesión
if "repositorio" not in st.session_state:
    st.session_state.repositorio = {}

if proyecto not in st.session_state.repositorio:
    st.session_state.repositorio[proyecto] = []

# Guardar archivos en memoria
if archivos_subidos:
    for archivo in archivos_subidos:

        existe = any(
            doc["nombre"] == archivo.name
            for doc in st.session_state.repositorio[proyecto]
        )

        if not existe:
            st.session_state.repositorio[proyecto].append(
                {
                    "nombre": archivo.name,
                    "tipo": archivo.type,
                    "contenido": archivo.getvalue()
                }
            )

    st.success("✅ Documentos agregados")

# Mostrar documentos
st.markdown("### Documentos del proyecto")

documentos = st.session_state.repositorio[proyecto]

if documentos:

    for i, doc in enumerate(documentos):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"📄 {doc['nombre']}")

        with col2:
            st.download_button(
                label="⬇️",
                data=doc["contenido"],
                file_name=doc["nombre"],
                mime=doc["tipo"],
                key=f"descarga_{proyecto}_{i}"
            )

else:
    st.info("No hay documentos cargados para este proyecto.")
