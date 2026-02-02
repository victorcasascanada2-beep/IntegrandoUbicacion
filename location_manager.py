import streamlit as st
from streamlit_js_eval import get_geolocation
import base64
import requests

def obtener_ubicacion():
    """
    Intenta obtener ubicación por GPS. 
    Si falla (como en PC), intenta obtenerla por la red (IP).
    """
    # 1. Intentamos el GPS del navegador (Cualquier dispositivo)
    loc = get_geolocation(component_key="gps_network_hybrid")
    
    if loc and isinstance(loc, dict) and 'coords' in loc:
        try:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            datos_raw = f"{lat},{lon}"
            b64_ref = base64.b64encode(datos_raw.encode()).decode()
            return f"REF_ID_{b64_ref}"
        except:
            pass

    # 2. Si el GPS falla o es PC, usamos la RED (IP Geolocation)
    # Esto no pide permiso y funciona por la conexión a internet
    try:
        # Usamos un servicio gratuito y rápido de geolocalización por IP
        response = requests.get('https://ipapi.co/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            lat = data.get('latitude')
            lon = data.get('longitude')
            if lat and lon:
                datos_raw = f"{lat},{lon}"
                b64_ref = base64.b64encode(datos_raw.encode()).decode()
                return f"REF_ID_NET_{b64_ref}"
    except:
        pass

    return "REF_ID_BUSCANDO"
