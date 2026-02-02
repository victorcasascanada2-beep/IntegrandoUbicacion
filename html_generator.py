import base64
from io import BytesIO

def procesar_foto_b64(foto):
    """Convierte la imagen a texto para el HTML con compresión"""
    buffered = BytesIO()
    if foto.mode in ("RGBA", "P"):
        foto = foto.convert("RGB")
    foto.save(buffered, format="JPEG", quality=75)
    return base64.b64encode(buffered.getvalue()).decode()

def generar_informe_html(marca, modelo, informe_texto, lista_fotos, ubicacion_b64):
    """Genera el HTML con estructura de párrafos y diseño limpio"""
    
    # 1. Procesamos las fotos
    fotos_html = ""
    for foto in lista_fotos:
        img_b64 = procesar_foto_b64(foto)
        fotos_html += f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 45%; margin: 10px; border-radius: 8px; border: 1px solid #ddd;">'

    # 2. TRATAMIENTO DEL TEXTO: Convertimos saltos de línea en párrafos reales
    # Esto evita que salga "amogollonado"
    parrafos = informe_texto.split('\n')
    texto_estructurado = ""
    for p in parrafos:
        if p.strip(): # Si el párrafo no está vacío
            texto_estructurado += f'<p style="margin-bottom: 15px; text-align: justify;">{p.strip()}</p>'

    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; color: #333; background-color: #f4f4f4; }}
            .container {{ background-color: white; max-width: 850px; margin: auto; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
            .header {{ text-align: center; border-bottom: 4px solid #2e7d32; padding-bottom: 20px; margin-bottom: 30px; }}
            .header h1 {{ color: #2e7d32; margin: 0; font-size: 32px; text-transform: uppercase; }}
            .content {{ line-height: 1.8; font-size: 17px; color: #444; }}
            .gallery {{ text-align: center; margin-top: 40px; background: #fdfdfd; padding: 25px; border: 1px solid #eee; border-radius: 10px; }}
            .footer {{ margin-top: 60px; font-size: 0.85em; text-align: center; color: #666; border-top: 1px solid #eee; padding-top: 25px; }}
            .ref-doc {{ 
                margin-top: 20px; 
                font-family: monospace; 
                color: #bbb; /* Color gris claro, ahora sí se ve pero no molesta */
                font-size: 10px; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Agrícola Noroeste</h1>
                <p style="font-size: 20px; font-weight: bold; margin: 10px 0;">INFORME PROFESIONAL DE TASACIÓN</p>
                <p><strong>Vehículo:</strong> {marca} {modelo}</p>
            </div>
            
            <div class="content">
                {texto_estructurado}
            </div>

            <div class="gallery">
                <h3 style="color: #2e7d32; margin-bottom: 20px;">Evidencias del Peritaje</h3>
                {fotos_html}
            </div>

            <div class="footer">
                <p>Este documento es una tasación técnica generada por el sistema de IA de Agrícola Noroeste.</p>
                <div class="ref-doc">ID_VERIFICACIÓN: {ubicacion_b64}</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template.encode('utf-8')
