from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io

def subir_informe(creds_dict, nombre_archivo, html_content):
    try:
        # 1. Verificamos que el contenido no esté vacío
        if not html_content:
            print("ERROR: El contenido HTML llegó vacío al manager")
            return None

        scopes = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)

        # 2. Aseguramos que el contenido sean bytes
        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8')

        file_metadata = {'name': nombre_archivo}
        
        # 3. Creamos el stream de datos
        fh = io.BytesIO(html_content)
        media = MediaIoBaseUpload(fh, mimetype='text/html', resumable=True)
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        
        return file.get('id')
    except Exception as e:
        # Esto saldrá en tus logs de Streamlit si algo falla
        print(f"FALLO CRÍTICO DRIVE: {str(e)}")
        return None
