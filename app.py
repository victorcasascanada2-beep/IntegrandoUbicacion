import streamlit as st
from PIL import Image
import ia_engine
import html_generator
import google_drive_manager
import location_manager  # <--- NUEVO MOTOR

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Tasador Agrícola", page_icon="🚜", layout="centered")

# 2. LIMPIEZA MÍNIMA (Solo para quitar lo de Streamlit)
st.markdown("""
<style>
    [data-testid="stToolbar"], footer {display: none;}
    section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# 3. CONEXIÓN VERTEX
if "vertex_client" not in st.session_state:
    creds = dict(st.secrets["google"])
    st.session_state.vertex_client = ia_engine.conectar_vertex(creds)

# --- CABECERA ---
# Tu nuevo logo
logo_url = "https://raw.githubusercontent.com/victorcasascanada2-beep/CopiaPruebaClave/3e79639d3faf452777931d392257eef8ed8c6144/afoto.png"
st.image(logo_url, width=200)
st.title("Tasación Experta")
st.caption("Agrícola Noroeste")
st.divider()

# --- FORMULARIO (Si no hay informe, lo mostramos) ---
if "informe_final" not in st.session_state:
    with st.form("form_tasacion"):
        col1, col2 = st.columns(2)
        with col1:
            marca = st.text_input("Marca", placeholder="John Deere")
            modelo = st.text_input("Modelo", placeholder="6155R")
        with col2:
            anio_txt = st.text_input("Año", value="2018")
            horas_txt = st.text_input("Horas", value="5000")
        
        observaciones = st.text_area("Notas / Extras")
        fotos = st.file_uploader("Fotos", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("🚀 REALIZAR TASACIÓN", use_container_width=True)

    if submit:
        if not (marca and modelo and fotos):
            st.warning("⚠️ Rellena marca, modelo y fotos.")
        else:
            with st.spinner("Analizando..."):
                try:
                    inf = ia_engine.realizar_peritaje(st.session_state.vertex_client, marca, modelo, int(anio_txt), int(horas_txt), observaciones, fotos)
                    st.session_state.informe_final = inf
                    st.session_state.fotos_final = [Image.open(f) for f in fotos]
                    st.session_state.marca_final, st.session_state.modelo_final = marca, modelo
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

# --- RESULTADOS Y BOTONES AL FINAL ---
if "informe_final" in st.session_state:
    st.markdown(st.session_state.informe_final)
    
    with st.expander("Ver imágenes"):
        cols = st.columns(3)
        for idx, img in enumerate(st.session_state.fotos_final):
            cols[idx % 3].image(img, use_container_width=True)

    st.divider()
    
    # Preparamos el HTML
    html_doc = html_generator.generar_informe_html(
        st.session_state.marca_final, st.session_state.modelo_final, 
        st.session_state.informe_final, st.session_state.fotos_final
    )
    
    # BOTONES JUNTOS AL FINAL
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.download_button("📥 DESCARGAR", data=html_doc, file_name="tasacion.html", use_container_width=True)
    
    with c2:
        if st.button("☁️ DRIVE", use_container_width=True):
            res = google_drive_manager.subir_informe(dict(st.secrets["google"]), f"Tasacion_{st.session_state.modelo_final}.html", html_doc)
            if res: st.success("✅ Guardado")
    
    with c3:
        # Aquí está el botón de NUEVA que pedías al final
        if st.button("🔄 OTRA", use_container_width=True):
            for k in ["informe_final", "fotos_final", "marca_final", "modelo_final"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
