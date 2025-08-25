from fastapi import UploadFile
from typing import List, Optional
from supabase import create_client, Client
from app.app.models.models import Document as DocumentModel, DocumentCreate, DocumentUpdate, DocumentStatus
import os
from datetime import datetime


class DocumentService:
    def __init__(self, supabase_url: str = os.getenv("SUPABASE_URL"), supabase_key: str = os.getenv("SUPABASE_KEY")):
        self.supabase: Client = create_client(supabase_url, supabase_key)

    async def upload_document_info(self, document: DocumentCreate) -> DocumentModel:
        data, count = self.supabase.from_('documents').insert(document.model_dump()).execute()
        return DocumentModel(**data[1][0])

    async def upload_document_file(self, document_id: int, file: UploadFile) -> DocumentModel:
        # Assuming 'documents' is your storage bucket
        file_path = f"documents/{document_id}/{file.filename}"
        content = await file.read()
        self.supabase.storage.from_('documents').upload(file_path, content)

        data, count = self.supabase.from_('documents').update({"uploaded_at": datetime.utcnow(), "status": DocumentStatus.uploaded}).eq("id", document_id).execute()
        return DocumentModel(**data[1][0])

    async def delete_document(self, document_id: int) -> dict:
        # Perform a soft delete by updating 'deleted_at'
        data, count = self.supabase.from_('documents').update({"deleted_at": datetime.utcnow()}).eq("id", document_id).execute()
        return {"action": "deleted", "message": "Document deleted"}

    async def update_document_info(self, document_id: int, document: DocumentUpdate) -> DocumentModel:
        data, count = self.supabase.from_('documents').update(document.model_dump(exclude_unset=True)).eq("id", document_id).execute()
        return DocumentModel(**data[1][0])

    async def list_documents(self) -> List[DocumentModel]:
        data, count = self.supabase.from_('documents').select("*", count='exact').is_("deleted_at", None).execute()
        return [DocumentModel(**item) for item in data[1]]

    async def get_document(self, document_id: int) -> DocumentModel:
        data, count = self.supabase.from_('documents').select("*", count='exact').eq("id", document_id).is_("deleted_at", None).execute()
        if data[1]:
            return DocumentModel(**data[1][0])
        return None

    async def get_shared_users_for_document(self, document_id: int) -> dict:
        # This requires joining documents with document_shared and users. Supabase client might not directly support complex joins in a single call.
        # This is a simplified approach, a more robust solution would involve views or stored procedures in Supabase, or multiple queries.
        data, count = self.supabase.from_('documents_shared').select("*, users(*)").eq("document_id", document_id).execute()
        shared_with_users = []
        for item in data[1]:
            user_info = item.get('users', {})
            if user_info:
                shared_with_users.append({
                    "id": user_info.get("id"),
                    "name": user_info.get("name"),
                    "email": user_info.get("email"),
                    "phone": user_info.get("phone"),
                    "shared_date": item.get("shared_date")
                })
        
        document_data, count = self.supabase.from_('documents').select("*").eq("id", document_id).execute()
        document_info = DocumentModel(**document_data[1][0]) if document_data[1] else {}

        return {
            **document_info.model_dump(),
            "shared_with": shared_with_users
        }

    async def inicialize_document_compresion_job(self, document_id: int) -> dict:
        # This would typically trigger an external job/queue. For now, a placeholder.
        # In a real scenario, you'd enqueue a message to a service like AWS SQS, Azure Service Bus, or a simple in-app background task queue.
        return {"idjob": 1, "document_size": 0, "started_timed_at": datetime.utcnow().isoformat()}
