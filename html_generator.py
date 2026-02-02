import base64
from io import BytesIO

def procesar_foto_b64(foto):
    """
    Convierte una imagen de PIL a una cadena Base64 optimizada para HTML.
    Añadimos una pequeña compresión para que el archivo final no sea demasiado pesado.
    """
    buffered = BytesIO()
    # Convertimos a RGB por si hay transparencias que den problemas en JPEG
    if foto.mode in ("RGBA", "P"):
        foto = foto.convert("RGB")
    
    # Guardamos con calidad optimizada
    foto.save(buffered, format="JPEG", quality=75)
    return base64.b64encode(buffered.getvalue()).decode()

def generar_informe_html(marca, modelo, informe_texto, lista_fotos, ubicacion_b64):
    """
    Genera el documento HTML profesional.
    Recibe la ubicación ya codificada en Base64 para insertarla discretamente.
    """
    
    # 1. Procesamos las fotos para el reporte
    fotos_html = ""
    for foto in lista_fotos:
        img_b64 = procesar_foto_b64(foto)
        fotos_html += f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 45%; margin: 10px; border-radius: 8px; border: 1px solid #ddd;">'

    # 2. Estructura del documento con diseño limpio (Sin mención visual a GPS)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 40px; color: #333; background-color: #f4f4f4; }}
            .container {{ background-color: white; max-width: 800px; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; border-bottom: 3px solid #2e7d32; padding-bottom: 20px; margin-bottom: 20px; }}
            .header h1 {{ color: #2e7d32; margin: 0; font-size: 28px; }}
            .header h2 {{ color: #555; font-size: 18px; margin: 5px 0; }}
            .content {{ line-height: 1.6; font-size: 16px; }}
            .gallery {{ text-align: center; margin-top: 30px; background: #fafafa; padding: 20px; border-radius: 8px; }}
            .gallery h3 {{ color: #2e7d32; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .footer {{ margin-top: 50px; font-size: 0.75em; text-align: center; color: #888; border-top: 1px solid #eee; padding-top: 20px; }}
            .ref-tecnica {{ color: #f9f9f9; font-size: 8px; }} /* Casi invisible para el ojo humano */
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Agrícola Noroeste</h1>
                <h2>Certificado de Tasación Profesional</h2>
                <p><strong>Equipo:</strong> {marca} {modelo}</p>
            </div>
            
            <div class="content">
                {informe_texto.replace('\\n', '<br>')}
            </div>

            <div class="gallery">
                <h3>Registro Fotográfico del Peritaje</h3>
                {fotos_html}
            </div>

            <div class="footer">
                <p>Este informe ha sido emitido mediante el sistema de tasación inteligente de Agrícola Noroeste.</p>
                <p>La valoración se basa en el estado visual, datos técnicos y análisis de mercado local actual.</p>
                <br>
                <span class="ref-tecnica">RefDocumento: {ubicacion_b64}</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Devolvemos el HTML codificado en bytes para que sea compatible con Descarga y Drive
    return html_template.encode('utf-8')
