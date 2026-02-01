import streamlit as st
from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim # <--- Nueva pieza para nombres de pueblos

def obtener_ubicacion():
    st.markdown("### 📍 Ubicación del Peritaje")
    st.info("Detectando municipio para ajustar la tasación al mercado local...")
    
    loc = get_geolocation()
    
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        
        # Intentamos sacar el municipio
        try:
            geolocator = Nominatim(user_agent="tasador_agricola")
            location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
            direccion = location.address
            # Extraemos el municipio si es posible
            municipio = location.raw.get('address', {}).get('village', 
                        location.raw.get('address', {}).get('town', 
                        location.raw.get('address', {}).get('city', 'Desconocido')))
        except:
            direccion = "Dirección no disponible"
            municipio = "Cerca de coordenadas"

        st.success(f"📍 Detectado: {municipio}")
        
        # Guardamos todo el detalle para la IA
        info_completa = f"""
        - MUNICIPIO: {municipio}
        - DIRECCIÓN: {direccion}
        - COORDENADAS: {lat}, {lon}
        """
        return info_completa
    else:
        st.warning("⚠️ GPS desactivado. Se usará mercado global.")
        return "Ubicación no proporcionada."
