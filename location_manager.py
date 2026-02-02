import streamlit as st
from streamlit_js_eval import get_geolocation
import base64

def obtener_ubicacion():
    """
    Intenta obtener el GPS. Si no puede (PC, permiso denegado, error),
    devuelve un código seguro para que la app NO se rompa.
    """
    # Usamos una key única para evitar conflictos internos de Streamlit
    loc = get_geolocation(component_key="gps_universal_fix")

    # 1. CASO DE ÉXITO: Tenemos datos y coordenadas
    if loc and isinstance(loc, dict) and 'coords' in loc:
        try:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Formateamos bonito para la IA
            datos_gps = f"LAT:{lat}|LON:{lon}"
            b64_ref = base64.b64encode(datos_gps.encode()).decode()
            return f"REF_GPS_{b64_ref}"
        except Exception:
            # Si falla la conversión, no rompemos nada
            return "REF_ERROR_FORMATO"

    # 2. CASO DE ERROR CONOCIDO (El navegador dice qué pasó)
    if loc and isinstance(loc, dict) and 'error' in loc:
        # El usuario dijo "No" o el PC no tiene sensor
        return "REF_GPS_DENEGADO_O_PC"

    # 3. CASO DE ESPERA / SIN DATOS (Aún cargando o PC sin respuesta)
    return "REF_MODO_PC_SIN_GPS"
