from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io

def subir_informe(creds_dict, nombre_archivo, html_content):
    try:
        # 1. AUTENTICACIÓN
        scopes = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)

        # 2. CORRECCIÓN DEL ERROR DE BYTES (Aquí estaba el fallo del log)
        # Si ya son bytes, los usamos tal cual. Si es texto, lo convertimos.
        if isinstance(html_content, str):
            datos_binarios = html_content.encode('utf-8')
        else:
            datos_binarios = html_content  # Ya viene en bytes desde el generator

        # 3. PREPARACIÓN DEL ARCHIVO
        file_metadata = {'name': nombre_archivo}
        media = MediaIoBaseUpload(io.BytesIO(datos_binarios), mimetype='text/html', resumable=True)
        
        # 4. SUBIDA
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        
        return file.get('id')

    except Exception as e:
        print(f"Error crítico en Drive: {str(e)}")
        return None
