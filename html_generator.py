import base64
from io import BytesIO
from datetime import datetime

def generar_informe_html(marca, modelo, informe_ia, fotos_pil, ubicacion):
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    fotos_html = ""
    
    for img in fotos_pil:
        # Opcional: Redimensionar para ahorrar espacio en el HTML
        img.thumbnail((800, 800)) 
        
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85) # Calidad 85 es el punto dulce
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        fotos_html += f'<img src="data:image/jpeg;base64,{img_b64}" style="width:100%; max-width:380px; margin:5px; border: 1px solid #ddd; border-radius:8px;">'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: auto; padding: 40px; background-color: #f4f4f4; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; border-bottom: 3px solid #2e7d32; padding-bottom: 20px; }}
            .section {{ margin-top: 25px; padding: 20px; border-left: 5px solid #2e7d32; background: #fff; }}
            .fotos {{ display: flex; flex-wrap: wrap; justify-content: space-around; gap: 10px; margin-top: 20px; }}
            .footer {{ margin-top: 40px; font-size: 0.8em; color: #999; text-align: center; }}
            h1 {{ color: #2e7d32; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>INFORME DE TASACIÓN EXPERTA</h1>
                <p><strong>Vehículo:</strong> {marca} {modelo} | <strong>Fecha:</strong> {fecha_actual}</p>
            </div>

            <div class="section">
                <h2 style="margin-top:0;">Análisis del Especialista (IA)</h2>
                <div style="white-space: pre-wrap;">{informe_ia}</div>
            </div>

            <div class="section">
                <h2 style="margin-top:0;">Registro Fotográfico</h2>
                <div class="fotos">
                    {fotos_html}
                </div>
            </div>

            <div class="footer">
                <p>Generado por Tasación Agrícola Noroeste</p>
                <code>ID_REF: {ubicacion}</code>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content.encode('utf-8')
