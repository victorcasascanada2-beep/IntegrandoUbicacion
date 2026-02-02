import streamlit as st
from streamlit_js_eval import get_geolocation
import base64

def obtener_ubicacion():
    """
    Obtiene la ubicación. Si falla, devuelve un código neutro.
    """
    # Intentamos capturar la ubicación
    loc = get_geolocation()
    
    # Si loc es None o está vacío, Streamlit aún está esperando al navegador
    if loc is None:
        return "REF_BUSCANDO"

    if isinstance(loc, dict) and 'coords' in loc:
        try:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Codificamos a Base64 para el informe
            datos_raw = f"{lat},{lon}"
            b64_ref = base64.b64encode(datos_raw.encode()).decode()
            return f"REF_ID_{b64_ref}"
        except Exception:
            return "REF_ID_ERROR"
            
    return "REF_ID_NO_DISPONIBLE"
