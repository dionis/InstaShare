import api from './api';

export interface Document {
  id: number;
  name: string;
  type: string;
  size: string;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
  uploaded_at: string;
  status?: "uploaded" | "process" | "downloaded";
}

export interface DocumentUploadInfo {
  id: number;
  name: string;
  type: string;
  uploaded_at: string;
  status: "uploaded" | "process" | "downloaded";
}

export interface DocumentListResponse extends Array<Document> {}

export interface DocumentSharedWithUser {
  id: number;
  name: string;
  email: string;
  phone: string;
  shared_date: string;
}

export interface DocumentSharedResponse extends Document {
  shared_with: DocumentSharedWithUser[];
}

export interface DeleteResponse {
  action: string;
  message: string;
}

export interface CompressionJobResponse {
  idjob: number;
  document_size: number;
  started_timed_at: string;
}

export const documentService = {
  uploadDocumentInfo: async (id: number, documentInfo: Omit<DocumentUploadInfo, 'id'>): Promise<DocumentUploadInfo> => {
    const response = await api.post<DocumentUploadInfo>(`/documents/upload_document_file/${id}`, documentInfo);
    return response.data;
  },

  // Note: The contract has two POST /upload_document/:id endpoints. 
  // One for info and one for file upload. This method is for file upload.
  uploadDocumentFile: async (
    id: number, 
    documentName: string, // Add documentName parameter
    documentType: string, // Add documentType parameter
    file: File
  ): Promise<DocumentUploadInfo> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', documentName); // Append document name
    formData.append('file_type', documentType); // Append document type
    const response = await api.post<DocumentUploadInfo>(`/documents/upload_document_file/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  deleteDocument: async (id: number): Promise<DeleteResponse> => {
    const response = await api.delete<DeleteResponse>(`/delete_document/${id}`);
    return response.data;
  },

  updateDocumentInfo: async (id: number, documentInfo: Partial<Omit<DocumentUploadInfo, 'id'>>): Promise<DocumentUploadInfo> => {
    const response = await api.put<DocumentUploadInfo>(`/update_document_info/${id}`, documentInfo);
    return response.data;
  },

  getAllDocuments: async (): Promise<DocumentListResponse> => {
    const response = await api.get<DocumentListResponse>('/documents');
    return response.data;
  },

  getDocumentById: async (id: number): Promise<Document> => {
    const response = await api.get<Document>(`/documents/${id}`);
    return response.data;
  },

  getUsersSharedWithDocument: async (id: number): Promise<DocumentSharedResponse> => {
    const response = await api.get<DocumentSharedResponse>(`/documents/${id}/shared_by/users`);
    return response.data;
  },

  startDocumentCompressionJob: async (documentId: number): Promise<CompressionJobResponse> => {
    // The contract shows a POST to /inicialize_document_compresion_job/ but the payload 
    // does not include the document ID. Assuming the backend expects the document ID in the body.
    const response = await api.post<CompressionJobResponse>('/inicialize_document_compresion_job/', { document_id: documentId });
    return response.data;
  },
};






