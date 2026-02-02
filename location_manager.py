import streamlit as st
from streamlit_js_eval import get_geolocation
import base64
import requests
import time

def obtener_ubicacion():
    """
    Intenta capturar GPS. Si el Maps funciona pero aquí no, 
    es por un retraso en el permiso del navegador. 
    Usamos la red como apoyo inmediato tras 10s.
    """
    # 1. Forzamos la petición al navegador
    # Usamos una key dinámica para que el navegador no "se duerma"
    t_key = int(time.time() / 5) # Cambia cada 5 segundos
    loc = get_geolocation(component_key=f"gps_agri_{t_key}")
    
    if "inicio_gps" not in st.session_state:
        st.session_state.inicio_gps = time.time()

    # Si el navegador responde con coordenadas (lo que hace el punto azul de Maps)
    if loc and isinstance(loc, dict) and 'coords' in loc:
        try:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            b64 = base64.b64encode(f"{lat},{lon}".encode()).decode()
            st.session_state.pop("inicio_gps", None)
            return f"REF_ID_{b64}"
        except: pass

    # 2. Si pasan los 10 segundos y el navegador sigue "pensando"
    tiempo_espera = time.time() - st.session_state.inicio_gps
    if tiempo_espera > 10:
        try:
            # Saltamos a la red (IP) que es lo que no falla nunca
            res = requests.get('https://ipapi.co/json/', timeout=2)
            if res.status_code == 200:
                data = res.json()
                lat, lon = data.get('latitude'), data.get('longitude')
                if lat and lon:
                    b64 = base64.b64encode(f"{lat},{lon}".encode()).decode()
                    st.session_state.pop("inicio_gps", None)
                    return f"REF_ID_NET_{b64}"
        except: pass
        
        # Último recurso si no hay internet ni GPS
        return "REF_ID_ZAMORA_DEFAULT"

    return "REF_ID_BUSCANDO"
