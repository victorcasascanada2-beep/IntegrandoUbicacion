import streamlit as st
from PIL import Image
import ia_engine
import html_generator
import google_drive_manager
import location_manager 

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Tasador Agrícola", page_icon="🚜", layout="centered")

# 2. LIMPIEZA MÍNIMA Y AJUSTE DE ALTURA (CSS optimizado)
st.markdown("""
<style>
    [data-testid="stToolbar"], footer {display: none;}
    section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}
    
    .block-container {
        padding-top: 1.5rem !important;
        margin-top: -1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. LLAMADA AL GPS (Controlada por sesión para evitar errores de clave duplicada)
if "texto_ubicacion" not in st.session_state:
    # Se ejecuta solo la primera vez o hasta que se obtenga
    st.session_state.texto_ubicacion = location_manager.obtener_ubicacion()

# 4. CONEXIÓN VERTEX
if "vertex_client" not in st.session_state:
    creds = dict(st.secrets["google"])
    st.session_state.vertex_client = ia_engine.conectar_vertex(creds)

# --- CABECERA ---
logo_url = "https://raw.githubusercontent.com/victorcasascanada2-beep/CopiaPruebaClave/3e79639d3faf452777931d392257eef8ed8c6144/afoto.png"
st.image(logo_url, width=300)
st.title("Tasación Experta Agrícola Noroeste")
st.divider()

# --- FORMULARIO OPTIMIZADO ---
if "informe_final" not in st.session_state:
    with st.form("form_tasacion"):
        # PASO 1: Subida de fotos
        st.markdown("##### 1. Imágenes del tractor")
        fotos = st.file_uploader("Sube las fotos aquí", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        
        st.divider()
        
        # PASO 2: Datos técnicos
        st.markdown("##### 2. Detalles del vehículo")
        col1, col2 = st.columns(2)
        with col1:
            marca = st.text_input("Marca", placeholder="John Deere")
            modelo = st.text_input("Modelo", placeholder="6155R")
        with col2:
            anio_txt = st.text_input("Año", value="2018")
            horas_txt = st.text_input("Horas", value="5000")
        
        observaciones = st.text_area("Notas / Equipamiento Extra")
        
        # El botón de envío
        submit = st.form_submit_button("🚀 REALIZAR TASACIÓN", use_container_width=True)

    # Procesado del formulario
    if submit:
        if not (marca and modelo and fotos):
            st.warning("⚠️ Rellena marca, modelo y sube al menos una foto.")
        else:
            with st.spinner("Generando informe técnico..."):
                try:
                    # Incluimos la ubicación oculta en las notas para la IA
                    notas_finales = f"{observaciones}\n\n[REF_METADATA: {st.session_state.texto_ubicacion}]"
                    
                    inf = ia_engine.realizar_peritaje(
                        st.session_state.vertex_client, 
                        marca, 
                        modelo, 
                        int(anio_txt), 
                        int(horas_txt), 
                        notas_finales, 
                        fotos
                    )
                    
                    # Guardamos todo en la sesión
                    st.session_state.informe_final = inf
                    st.session_state.fotos_final = [Image.open(f) for f in fotos]
                    st.session_state.marca_final = marca
                    st.session_state.modelo_final = modelo
                    st.rerun()
                except Exception as e: 
                    st.error(f"Error en el procesado: {e}")

# --- RESULTADOS Y BOTONES DE EXPORTACIÓN ---
if "informe_final" in st.session_state:
    st.markdown(st.session_state.informe_final)
    
    with st.expander("Ver imágenes"):
        cols = st.columns(3)
        for idx, img in enumerate(st.session_state.fotos_final):
            cols[idx % 3].image(img, use_container_width=True)

    st.divider()
    
    # Generamos el HTML una sola vez para evitar retrasos en los botones
    if "html_listo" not in st.session_state:
        st.session_state.html_listo = html_generator.generar_informe_html(
            st.session_state.marca_final, 
            st.session_state.modelo_final, 
            st.session_state.informe_final, 
            st.session_state.fotos_final,
            st.session_state.texto_ubicacion
        )
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.download_button(
            label="📥 DESCARGAR", 
            data=st.session_state.html_listo, 
            file_name=f"tasacion_{st.session_state.modelo_final}.html", 
            mime="text/html",
            use_container_width=True
        )
    
    with c2:
        if st.button("☁️ DRIVE", use_container_width=True):
            # El spinner SI está aquí, pero solo funciona si el código es correcto
            with st.spinner("Subiendo a Google Drive..."):
                try:
                    creds_drive = dict(st.secrets["google"])
                    nombre_archivo = f"Tasacion_{st.session_state.marca_final}_{st.session_state.modelo_final}.html"
                    
                    # AQUÍ ESTABA EL ERROR (Debe ser la llamada completa al manager)
                    res = google_drive_manager.subir_informe(
                        creds_drive, 
                        nombre_archivo, 
                        st.session_state.html_listo
                    )
                    
                    if res: 
                        st.success("✅ Guardado correctamente")
                except Exception as e:
                    st.error(f"Error al subir: {e}")
