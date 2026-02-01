import streamlit as st
from streamlit_js_eval import get_geolocation
import base64

def obtener_ubicacion():
    # El mensaje sutil
    st.caption("📍 Optimizando precisión de mercado local...")
    
    try:
        # IMPORTANTE: Añadimos una key fija para que no se duplique el componente
        loc = get_geolocation(key="gps_tracker_pro")
        
        if loc and 'coords' in loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Formateamos solo los números
            datos_gps = f"LAT:{lat}|LON:{lon}"
            
            # Convertimos a Base64
            b64_ref = base64.b64encode(datos_gps.encode()).decode()
            
            return f"REF_ID_{b64_ref}"
            
    except Exception:
        return "REF_ID_OFFLINE"
    
    return "REF_ID_SEARCHING"
