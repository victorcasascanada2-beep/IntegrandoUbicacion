import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

# --- CONFIGURACIÓN DE AGRÍCOLA NOROESTE ---
# Sustituye este ID por el de tu Unidad Compartida (el código de la URL)
ID_CARPETA_DRIVE = "0AEU0RHjR-mDOUk9PVA" 

# Usamos el scope completo para evitar problemas de permisos en unidades compartidas
SCOPES = ["https://www.googleapis.com/auth/drive"]

def subir_informe(creds_dict, nombre_archivo, contenido_html):
    """
    Sube el informe a una Unidad Compartida de Google Drive.
    Incluye los parámetros 'supportsAllDrives' necesarios para estas unidades.
    """
    try:
        # 1. Autenticación con la cuenta de servicio
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, 
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)

        # 2. Metadatos del archivo
        # 'parents' debe contener el ID de la unidad o carpeta compartida
        file_metadata = {
            'name': nombre_archivo,
            'parents': [ID_CARPETA_DRIVE],
            'mimeType': 'text/html'
        }
        
        # 3. Preparar el flujo de datos (Stream)
        fh = io.BytesIO(contenido_html.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype='text/html', resumable=True)

        # 4. Creación del archivo
        # IMPORTANTE: Para Unidades Compartidas es obligatorio 'supportsAllDrives=True'
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True # Permite trabajar con Unidades Compartidas
        ).execute()

        return file.get('id')

    except Exception as e:
        # Imprimimos el error en los logs de Streamlit para diagnóstico
        print(f"Error técnico en Google Drive Manager: {str(e)}")
        return None
