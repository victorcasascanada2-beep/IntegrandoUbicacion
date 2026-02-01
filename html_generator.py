import base64
from io import BytesIO

def generar_informe_html(marca, modelo, informe_ia, fotos_pil, ubicacion):
    """
    Genera un archivo HTML profesional con las fotos incrustadas y 
    la ubicación oculta como referencia técnica.
    """
    
    # 1. Convertimos las fotos de PIL a Base64 para que se vean en el HTML
    fotos_html = ""
    for img in fotos_pil:
        buf = BytesIO()
        img.save(buf, format="JPEG")
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        fotos_html += f'<img src="data:image/jpeg;base64,{img_b64}" style="width:100%; max-width:400px; margin:10px; border-radius:8px;">'

    # 2. Construcción del documento HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #2e7d32; padding-bottom: 10px; }}
            .section {{ margin-top: 20px; padding: 15px; background: #f9f9f9; border-radius: 5px; }}
            .fotos {{ display: flex; flex-wrap: wrap; justify-content: center; }}
            .footer {{ margin-top: 50px; font-size: 0.7em; color: #888; border-top: 1px solid #eee; padding-top: 10px; }}
            h1 {{ color: #2e7d32; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>INFORME DE TASACIÓN EXPERTA</h1>
            <p><strong>Vehículo:</strong> {marca} {modelo}</p>
        </div>

        <div class="section">
            <h2>Análisis Técnico de la IA</h2>
            <div style="white-space: pre-wrap;">{informe_ia}</div>
        </div>

        <div class="section">
            <h2>Evidencias Fotográficas</h2>
            <div class="fotos">
                {fotos_html}
            </div>
        </div>

        <div class="footer">
            <p>Este informe ha sido generado automáticamente por el sistema de Tasación Agrícola Noroeste.</p>
            <p style="color: #ccc;">REF_SISTEMA: {ubicacion}</p>
        </div>
    </body>
    </html>
    """
    
    # Devolvemos el HTML listo para ser descargado o subido a Drive
    return html_content.encode('utf-8')
