import base64
from io import BytesIO

def procesar_foto_b64(foto):
    """Convierte la imagen a texto para meterla en el HTML"""
    buffered = BytesIO()
    foto.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def generar_informe_html(marca, modelo, informe_texto, lista_fotos):
    # Convertimos las fotos a formato web
    fotos_html = ""
    for foto in lista_fotos:
        img_b64 = procesar_foto_b64(foto)
        fotos_html += f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 45%; margin: 10px; border-radius: 8px;">'

    # Estructura del documento
    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            .header {{ text-align: center; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }}
            .content {{ line-height: 1.6; margin-top: 20px; }}
            .gallery {{ text-align: center; margin-top: 30px; background: #f9f9f9; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #0056b3; color: white; }}
            .footer {{ margin-top: 50px; font-size: 0.8em; text-align: center; color: #777; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Agrícola Noroeste</h1>
            <h2>Informe de Tasación Profesional</h2>
            <p><strong>Equipo:</strong> {marca} {modelo}</p>
        </div>
        
        <div class="content">
            {informe_texto.replace('\n', '<br>')}
        </div>

        <div class="gallery">
            <h3>Evidencia Fotográfica</h3>
            {fotos_html}
        </div>

        <div class="footer">
            <p>Generado por Sistema IA Noroeste - {marca} {modelo}</p>
        </div>
    </body>
    </html>
    """
    return html_template
