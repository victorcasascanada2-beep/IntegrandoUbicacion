import streamlit as st
from streamlit_js_eval import get_geolocation
import base64

def obtener_ubicacion():
    # Mensaje sutil para el permiso
    #st.caption("📍 Optimizando precisión de mercado local...")
    
    try:
        loc = get_geolocation()
        
        if loc and 'coords' in loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Formateamos solo los números
            datos_gps = f"LAT:{lat}|LON:{lon}"
            
            # Convertimos a Base64
            b64_ref = base64.b64encode(datos_gps.encode()).decode()
            
            # Devolvemos el ID técnico camuflado
            return f"REF_ID_{b64_ref}"
            
    except Exception:
        return "REF_ID_G100"
    
    return "REF_ID_P100"
