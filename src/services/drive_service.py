from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import pickle
from io import BytesIO
from docx import Document
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DriveService:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self):
        self.credentials = self._get_credentials()
        self.service = build('drive', 'v3', credentials=self.credentials)
    
    def _get_credentials(self):
        """
        Authenticate and get Google Drive credentials
        """
        creds = None
        token_path = settings.google_drive_token_path
        creds_path = settings.google_drive_credentials_path
        
        # Load existing token
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(
                        f"Google credentials file not found at {creds_path}. "
                        "Download from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds
    
    def upload_document(self, content: str, filename: str) -> str:
        """
        Upload briefing document to Google Drive as .docx
        """
        try:
            # Create Word document
            doc = Document()
            doc.add_paragraph(content)
            
            # Save to BytesIO
            doc_io = BytesIO()
            doc.save(doc_io)
            doc_io.seek(0)
            
            # Prepare file metadata
            file_metadata = {
                'name': filename if filename.endswith('.docx') else f"{filename}.docx",
                'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            
            if settings.google_drive_folder_id and settings.google_drive_folder_id != "optional_folder_id":
                file_metadata['parents'] = [settings.google_drive_folder_id]
            
            # Upload file
            media = MediaIoBaseUpload(
                doc_io,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            logger.info(f"Document uploaded successfully: {file.get('webViewLink')}")
            return file.get('webViewLink')
            
        except Exception as e:
            logger.error(f"Failed to upload to Google Drive: {str(e)}")
            raise
