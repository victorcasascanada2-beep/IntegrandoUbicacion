import streamlit as st
from streamlit_js_eval import get_geolocation

def obtener_ubicacion():
    """
    Lanza la petición de GPS al navegador y devuelve un texto 
    con la ubicación o un aviso de que no está disponible.
    """
    st.markdown("### 📍 Localización para Tasación Local")
    st.info("La ubicación nos permite ajustar el precio al mercado de tu zona (impuestos, logística y demanda local).")
    
    # Esto activa el pop-up de permiso en el móvil/PC
    loc = get_geolocation()
    
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        # Guardamos en sesión para no perderlo al recargar
        st.session_state.gps_data = {"lat": lat, "lon": lon}
        return f"Latitud: {lat}, Longitud: {lon} (Ubicación GPS precisa)"
    else:
        return "Ubicación no proporcionada (Tasación basada en mercado global)"
