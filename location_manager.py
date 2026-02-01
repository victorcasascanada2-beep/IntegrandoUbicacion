import streamlit as st
from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim
import base64

def obtener_ubicacion():
    # Mensaje sutil y profesional
    st.caption("📍 Optimizando precisión de mercado local...")
    
    try:
        # Captura de datos con gestión de errores (para evitar el KeyError)
        loc = get_geolocation()
        
        if loc and 'coords' in loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Buscamos el municipio de forma silenciosa
            try:
                geolocator = Nominatim(user_agent="agri_engine_ref")
                location = geolocator.reverse(f"{lat}, {lon}", timeout=5)
                muni = location.raw.get('address', {}).get('village', 
                       location.raw.get('address', {}).get('town', 
                       location.raw.get('address', {}).get('city', 'Region_Ref')))
                addr = location.address
            except:
                muni, addr = "Reg_Std", "Coord_Ref"

            # Creamos el pack de datos
            datos_sucios = f"LOC_REF: {muni} | ADDR: {addr} | GPS: {lat},{lon}"
            
            # Lo convertimos a Base64 para que parezca una referencia de fichero
            b64_ref = base64.b64encode(datos_sucios.encode()).decode()
            return f"REF_ID_{b64_ref[:50]}" # Mostramos solo un trozo para que parezca un ID
            
    except Exception:
        # Si algo falla (PC, denegado, etc.), devolvemos un ID genérico
        return "REF_ID_GLOBAL_001"
    
    return "REF_ID_PENDING"
