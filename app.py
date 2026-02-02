import streamlit as st
from PIL import Image
import ia_engine
import html_generator
import google_drive_manager
import location_manager
from streamlit_js_eval import get_geolocation
coords_usuario = None
# -------------------------------------------------
# 1. CONFIGURACIÓN BÁSICA
# -------------------------------------------------
st.set_page_config(
    page_title="Tasador Agrícola",
    page_icon="🚜",
    layout="centered"
)

# -------------------------------------------------
# 2. LIMPIEZA UI + CSS
# -------------------------------------------------
st.markdown("""
<style>
    [data-testid="stToolbar"], footer {display: none;}
    section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}
    .block-container { padding-top: 4rem !important; margin-top: -1rem !important; }
    .stSpinner > div { border-top-color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 3. DISPARO TEMPRANO DE GEOLOCALIZACIÓN (NO BLOQUEA)
# -------------------------------------------------
# Esto lanza el permiso del navegador nada más cargar la app
# y deja que el navegador trabaje mientras el usuario rellena el form

if "geo_disparada" not in st.session_state:
    try:
        get_geolocation()  # 🔥 solo dispara, no esperamos
    except Exception:
        pass
    st.session_state.geo_disparada = True

# -------------------------------------------------
# 4. CONEXIÓN A VERTEX AI
# -------------------------------------------------
if "vertex_client" not in st.session_state:
    try:
        creds = dict(st.secrets["google"])
        st.session_state.vertex_client = ia_engine.conectar_vertex(creds)
    except Exception as e:
        st.error(f"Error de credenciales: {e}")

# -------------------------------------------------
# 5. CABECERA
# -------------------------------------------------
logo_url = "https://raw.githubusercontent.com/victorcasascanada2-beep/CopiaPruebaClave/3e79639d3faf452777931d392257eef8ed8c6144/afoto.png"
st.image(logo_url, width=300)
st.title("Tasación Experta")
st.caption("Optimizando precisión de mercado según zona de peritaje.")
st.divider()

# -------------------------------------------------
# 6. FORMULARIO
# -------------------------------------------------
if "informe_final" not in st.session_state:
    with st.form("form_tasacion"):
        col1, col2 = st.columns(2)
        with col1:
            marca = st.text_input("Marca", value="John Deere")
            modelo = st.text_input("Modelo", value="6175R")
        with col2:
            anio_txt = st.text_input("Año", value="2018")
            horas_txt = st.text_input("Horas", value="5000")

        observaciones = st.text_area(
            "Notas / Extras / Equipamiento",
            value="con soportes de pala monomando y valvulas ventrales, con compresor de frenos de remolque"
        )

        fotos = st.file_uploader(
            "Fotos del tractor",
            accept_multiple_files=True,
            type=['jpg', 'jpeg', 'png']
        )

        submit = st.form_submit_button(
            "🚀 REALIZAR TASACIÓN",
            use_container_width=True
        )

    if submit:
        if not (marca and modelo and fotos):
            st.warning("⚠️ Rellena marca, modelo y sube fotos.")
        else:
            zona_spinner = st.empty()
            with zona_spinner.container():
                with st.spinner("Analizando mercado español..."):
                    try:
                        # ❌ La ubicación NO entra en la tasación
                        inf = ia_engine.realizar_peritaje(
                            st.session_state.vertex_client,
                            marca,
                            modelo,
                            int(anio_txt),
                            int(horas_txt),
                            observaciones,
                            fotos
                        )

                        st.session_state.informe_final = inf
                        st.session_state.fotos_final = [Image.open(f) for f in fotos]
                        st.session_state.marca_final = marca
                        st.session_state.modelo_final = modelo

                        # -------------------------------------------------
                        # 7. UBICACIÓN FINAL (NO BLOQUEANTE)
                        # -------------------------------------------------
                        # Aquí recogemos lo que el navegador haya resuelto
                        # Si no hay nada → fallback España inmediato

                        ubicacion_codificada = location_manager.obtener_ubicacion_final()

                        # HTML final con ubicación ya resuelta
                        st.session_state.html_listo = html_generator.generar_informe_html(
                            marca,
                            modelo,
                            inf,
                            st.session_state.fotos_final,
                            ubicacion_codificada
                        )

                        zona_spinner.empty()
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error técnico: {e}")

# -------------------------------------------------
# 8. RESULTADOS
# -------------------------------------------------
if "informe_final" in st.session_state:
    st.markdown(st.session_state.informe_final)

    with st.expander("Ver imágenes"):
        cols = st.columns(3)
        for idx, img in enumerate(st.session_state.fotos_final):
            cols[idx % 3].image(img, use_container_width=True)

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.download_button(
            "📥 DESCARGAR",
            data=st.session_state.html_listo,
            file_name=f"tasacion_{st.session_state.modelo_final}.html",
            mime="text/html",
            use_container_width=True
        )

    with c2:
        if st.button("☁️ DRIVE", use_container_width=True):
            with st.spinner("Subiendo..."):
                try:
                    creds_drive = dict(st.secrets["google"])
                    nombre = f"Tasacion_{st.session_state.marca_final}_{st.session_state.modelo_final}.html"
                    exito = google_drive_manager.subir_informe(
                        creds_drive,
                        nombre,
                        st.session_state.html_listo
                    )
                    if exito:
                        st.success("✅ Guardado")
                    else:
                        st.error("❌ Falló subida")
                except Exception as e:
                    st.error(f"Error: {e}")

    with c3:
        if st.button("🔄 OTRA", use_container_width=True):
            for k in [
                "informe_final",
                "fotos_final",
                "marca_final",
                "modelo_final",
                "html_listo",
                "geo_disparada"
            ]:
                st.session_state.pop(k, None)
            st.rerun()
