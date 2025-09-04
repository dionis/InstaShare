from sheduler_app import app as celery_app
from db.base import get_supabase_client, create_client, Client
from services.log_service import LogService
from schemas.log import LogCreate
from schemas.document import DocumentUpdate
from dotenv import load_dotenv
from datetime import datetime

from models.document import Document as DocumentModel, DocumentStatus
from services.document_service import DocumentService
import os
import io
import zipfile
import asyncio

from dotenv import load_dotenv

COMPRESSED_FILES_DIR = "./compressed_files"

load_dotenv()


async def _run_compression_logic(mensaje: str):
    os.makedirs(COMPRESSED_FILES_DIR, exist_ok=True)
    supabase: Client = get_supabase_client()
    log_service = LogService(supabase)
    document_service = DocumentService(supabase)
 
    
    user_aux_id = 1

    try:
        documents_to_compress_response = supabase.from_('documents').select("*").eq('status', DocumentStatus.uploaded.value).execute()
        documents_to_compress = documents_to_compress_response.data
        
        for doc_data in documents_to_compress:
            document = DocumentModel(**doc_data)
            print(f"Processing document: {document.name} (ID: {document.id})")
            user_aux_id = document.user_id
            
            log_entry = LogCreate(
                event="Scheduled Task Execution",
                user_id = user_aux_id, # Assuming a default user for scheduled tasks, or pass it as an argument
                event_description=f"Scheduled compression task started at: {datetime.now().isoformat()}"
            )
            await log_service.create_log(
                event=log_entry.event, 
                user_id=log_entry.user_id, 
                event_description=log_entry.event_description
            )

            if not document.file_url:
                print(f"Document {document.id} has no file_url. Skipping.")
                continue
            
            path_parts = document.file_url.split('/public/')
            if len(path_parts) < 2:
                print(f"Invalid file_url for document {document.id}: {document.file_url}. Skipping.")
                continue
            
            storage_path = path_parts[1]
            bucket_name = storage_path.split('/')[0]
            file_in_bucket_path = '/'.join(storage_path.split('/')[1:])

            print(f"Downloading file from bucket: {bucket_name}, path: {file_in_bucket_path}")
            file_content_response = supabase.storage.from_(bucket_name).download(file_in_bucket_path)
            
            if not file_content_response:
                print(f"Failed to download file for document {document.id}. Skipping.")
                continue

            compressed_file_name = f"{os.path.splitext(document.name)[0]}.zip"
            compressed_file_path_in_storage = f"{bucket_name}/{document.id}/{compressed_file_name}"
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.writestr(document.name, file_content_response)
            zip_buffer.seek(0)

            # Save compressed file to local filesystem
            local_compressed_file_path = os.path.join(COMPRESSED_FILES_DIR, compressed_file_name)
            with open(local_compressed_file_path, "wb") as f:
                f.write(zip_buffer.getvalue())
            print(f"Compressed file saved locally to: {local_compressed_file_path}")
            
            print(f"Uploading compressed file to {compressed_file_path_in_storage}")
            # Since we're uploading a new file, the `file_in_bucket_path` should be for the new file
            # The `upload` method takes the storage path and content
            supabase.storage.from_(bucket_name).upload(compressed_file_path_in_storage, zip_buffer.getvalue(), {'upsert': 'true'})
            
            print(f"Compressed file uploaded to {compressed_file_path_in_storage}")
            new_public_url = supabase.storage.from_(bucket_name).get_public_url(f"{document.id}/{compressed_file_name}")

            print(f"New public URL: {new_public_url}")
            document_update = DocumentUpdate(
                status=DocumentStatus.process,
                file_url=new_public_url,
                updated_at=datetime.now().isoformat()
            )
            await document_service.update_document(
                document.id, 
                document_update
            )
            print(f"Document {document.id} compressed and updated. New URL: {new_public_url}")

            log_entry_success = LogCreate(
                event="Document Compression Success",
                user_id= document.user_id,
                event_description=f"Document {document.name} (ID: {document.id}) successfully compressed and updated."
            )
            await log_service.create_log(
                event=log_entry_success.event,
                user_id=log_entry_success.user_id,
                event_description=log_entry_success.event_description
            )

    except Exception as e:
        print(f"Error during scheduled compression task: {e}")
        log_entry_error = LogCreate(
            event="Scheduled Task Error",
            user_id = user_aux_id,
            event_description=f"Error during document compression task: {e}"
        )
        await log_service.create_log(
            event=log_entry_error.event,
            user_id=log_entry_error.user_id,
            event_description=log_entry_error.event_description
        )

    return f"Scheduled compression task completed at: {datetime.now().isoformat()}"


@celery_app.task
def mi_tarea_planificada(mensaje):
    print(f"La tarea planificada se ha ejecutado. Mensaje: {mensaje}")
    asyncio.run(_run_compression_logic(mensaje))

# @celery_app.task
# async def mi_tarea_planificada(mssg):
    # print(f"La tarea planificada se ha ejecutado. Mensaje: {mssg}")
   
    # supabase: Client = get_supabase_client()
    # log_service = LogService(supabase)
    
    # # Log the event
    # log_entry = LogCreate(
    #     event="Scheduled Task Execution",
    #     user_id=1, # Assuming a default user for scheduled tasks, or pass it as an argument
    #     event_description=f"Compress {mssg} file execution at: {datetime.now()}"
    # )
    # # The create_log method in LogService expects event, user_id, event_description separately
    # log_service.create_log(
    #     event=log_entry.event, 
    #     user_id=log_entry.user_id, 
    #     event_description=log_entry.event_description
    # )
    
    