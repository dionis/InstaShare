import { documentService, Document, DocumentListResponse, DocumentUploadInfo, DeleteResponse, CompressionJobResponse, DocumentSharedResponse } from './documentService';
import api from './api'; // Mocked by Jest

jest.mock('./api');
const mockedApi = api as jest.Mocked<typeof api>;

describe('documentService', () => {
  beforeEach(() => {
    mockedApi.get.mockClear();
    mockedApi.post.mockClear();
    mockedApi.put.mockClear();
    mockedApi.delete.mockClear();
  });

  test('uploadDocumentInfo should upload document metadata', async () => {
    const docId = 23;
    const docInfo: Omit<DocumentUploadInfo, 'id'> = {
      name: 'book_programing', type: 'docx', uploaded_at: '2025-04-22', status: 'uploaded'
    };
    const mockResponse: DocumentUploadInfo = { id: docId, ...docInfo };
    mockedApi.post.mockResolvedValueOnce({ data: mockResponse });

    const response = await documentService.uploadDocumentInfo(docId, docInfo);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith(`/upload_document/${docId}`, docInfo);
    expect(response).toEqual(mockResponse);
  });

  test('uploadDocumentFile should upload a file', async () => {
    const docId = 23;
    const mockFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    const mockResponse: DocumentUploadInfo = {
      id: docId, name: 'test.pdf', type: 'pdf', uploaded_at: '2025-04-22', status: 'uploaded'
    };
    mockedApi.post.mockResolvedValueOnce({ data: mockResponse });

    const formData = new FormData();
    formData.append('file', mockFile);

    const response = await documentService.uploadDocumentFile(docId, mockFile);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith(`/upload_document/${docId}`, expect.any(FormData), {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    expect(response).toEqual(mockResponse);
  });

  test('deleteDocument should delete a document by ID', async () => {
    const deleteResponse: DeleteResponse = { action: 'deleted', message: 'Document deleted' };
    mockedApi.delete.mockResolvedValueOnce({ data: deleteResponse });

    const response = await documentService.deleteDocument(23);

    expect(mockedApi.delete).toHaveBeenCalledTimes(1);
    expect(mockedApi.delete).toHaveBeenCalledWith('/delete_document/23');
    expect(response).toEqual(deleteResponse);
  });

  test('updateDocumentInfo should update document metadata', async () => {
    const docId = 23;
    const updatedDocInfo: Partial<Omit<DocumentUploadInfo, 'id'>> = { name: 'updated_book' };
    const mockResponse: DocumentUploadInfo = {
      id: docId, name: 'updated_book', type: 'docx', uploaded_at: '2025-04-22', status: 'uploaded'
    };
    mockedApi.put.mockResolvedValueOnce({ data: mockResponse });

    const response = await documentService.updateDocumentInfo(docId, updatedDocInfo);

    expect(mockedApi.put).toHaveBeenCalledTimes(1);
    expect(mockedApi.put).toHaveBeenCalledWith(`/update_document_info/${docId}`, updatedDocInfo);
    expect(response).toEqual(mockResponse);
  });

  test('getAllDocuments should fetch a list of documents', async () => {
    const mockDocuments: DocumentListResponse = [
      { id: 23, name: 'book_programing', type: 'docx', size: '456M', uploaded_at: '2025-04-22' },
    ];
    mockedApi.get.mockResolvedValueOnce({ data: mockDocuments });

    const documents = await documentService.getAllDocuments();

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/documents');
    expect(documents).toEqual(mockDocuments);
  });

  test('getDocumentById should fetch a single document by ID', async () => {
    const mockDocument: Document = { id: 23, name: 'book_programing', type: 'docx', size: '456M', uploaded_at: '2025-04-22' };
    mockedApi.get.mockResolvedValueOnce({ data: mockDocument });

    const document = await documentService.getDocumentById(23);

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/documents/23');
    expect(document).toEqual(mockDocument);
  });

  test('getUsersSharedWithDocument should fetch users shared with a document', async () => {
    const mockSharedResponse: DocumentSharedResponse = {
      id: 23, name: 'book_programing', type: 'docx', size: '456M', uploaded_at: '2025-04-22',
      shared_with: [
        { id: 1, name: 'John Smith', email: 'john@gmail.com', phone: '+143234554', shared_date: '2025-01-23' },
      ],
    };
    mockedApi.get.mockResolvedValueOnce({ data: mockSharedResponse });

    const response = await documentService.getUsersSharedWithDocument(23);

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/documents/23/shared_by/users');
    expect(response).toEqual(mockSharedResponse);
  });

  test('startDocumentCompressionJob should initiate a compression job', async () => {
    const docId = 123;
    const mockResponse: CompressionJobResponse = {
      idjob: 1, document_size: 234, started_timed_at: '2025-04-22'
    };
    mockedApi.post.mockResolvedValueOnce({ data: mockResponse });

    const response = await documentService.startDocumentCompressionJob(docId);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/inicialize_document_compresion_job/', { document_id: docId });
    expect(response).toEqual(mockResponse);
  });
});






