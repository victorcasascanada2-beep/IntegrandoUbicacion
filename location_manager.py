import base64
import requests

HEADERS = {"User-Agent": "tasador-agricola"}
TIMEOUT = 2

def _encode(texto: str) -> str:
    return base64.urlsafe_b64encode(texto.encode()).decode()

def _reverse_geocode(lat: float, lon: float) -> str | None:
    url = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?lat={lat}&lon={lon}&format=json&zoom=14"
    )
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    data = r.json()
    addr = data.get("address", {})
    return (
        addr.get("village")
        or addr.get("town")
        or addr.get("city")
        or addr.get("municipality")
    )

def obtener_ubicacion_final(coords: tuple[float, float] | None) -> str:
    """
    coords: (lat, lon) o None
    Devuelve SIEMPRE algo codificado.
    """
    if coords:
        try:
            pueblo = _reverse_geocode(coords[0], coords[1])
            if pueblo:
                return f"LOC_{_encode(pueblo)}"
        except Exception:
            pass

    # fallback estable
    return f"LOC_{_encode('ES')}"
