import streamlit as st
from PIL import Image
import ia_engine
import html_generator
import google_drive_manager
import location_manager 

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Tasador Agrícola", page_icon="🚜", layout="centered")

# 2. LIMPIEZA MÍNIMA Y CSS
st.markdown("""
<style>
    [data-testid="stToolbar"], footer {display: none;}
    section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}
    .block-container { padding-top: 1rem !important; margin-top: -1rem !important; }
    .stSpinner > div { border-top-color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE UBICACIÓN (Invisible y persistente)
if "texto_ubicacion" not in st.session_state:
    st.session_state.texto_ubicacion = location_manager.obtener_ubicacion()

# 4. CONEXIÓN VERTEX
if "vertex_client" not in st.session_state:
    try:
        creds = dict(st.secrets["google"])
        st.session_state.vertex_client = ia_engine.conectar_vertex(creds)
    except Exception as e:
        st.error(f"Error de credenciales: {e}")

# --- CABECERA ---
logo_url = "https://raw.githubusercontent.com/victorcasascanada2-beep/CopiaPruebaClave/3e79639d3faf452777931d392257eef8ed8c6144/afoto.png"
st.image(logo_url, width=200)
st.title("Tasación Experta")
# Mensaje discreto sobre la ubicación
st.caption("Optimizando precisión de mercado según zona de peritaje.") 
st.divider()

# --- FORMULARIO ---
if "informe_final" not in st.session_state:
    with st.form("form_tasacion"):
        col1, col2 = st.columns(2)
        with col1:
            marca = st.text_input("Marca", placeholder="John Deere")
            modelo = st.text_input("Modelo", placeholder="6155R")
        with col2:
            anio_txt = st.text_input("Año", value="2018")
            horas_txt = st.text_input("Horas", value="5000")
        
        observaciones = st.text_area("Notas / Extras / Equipamiento")
        fotos = st.file_uploader("Fotos del tractor", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("🚀 REALIZAR TASACIÓN", use_container_width=True)

    if submit:
        if not (marca and modelo and fotos):
            st.warning("⚠️ Rellena marca, modelo y sube fotos.")
        else:
            zona_spinner = st.empty()
            with zona_spinner.container():
                with st.spinner("Analizando mercado local..."):
                    try:
                        # Inyectamos la ubicación codificada en las notas de la IA de forma interna
                        # La IA usará esto para el contexto pero no mostrará las coordenadas
                        notas_ia = f"{observaciones}\n\n[REF_SISTEMA: {st.session_state.texto_ubicacion}]"
                        
                        inf = ia_engine.realizar_peritaje(
                            st.session_state.vertex_client, 
                            marca, modelo, int(anio_txt), int(horas_txt), 
                            notas_ia, fotos
                        )
                        
                        st.session_state.informe_final = inf
                        st.session_state.fotos_final = [Image.open(f) for f in fotos]
                        st.session_state.marca_final, st.session_state.modelo_final = marca, modelo
                        
                        # Generamos el HTML aquí con la ubicación en Base64 para el pie de página
                        st.session_state.html_listo = html_generator.generar_informe_html(
                            marca, modelo, inf, st.session_state.fotos_final, st
