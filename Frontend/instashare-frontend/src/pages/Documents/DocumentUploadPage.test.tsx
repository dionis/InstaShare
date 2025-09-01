import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import DocumentUploadPage from './DocumentUploadPage';
import { documentService } from '../../services/documentService';
import { AuthProvider } from '../../contexts/AuthContext';

// Mock de react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock de documentService
jest.mock('../../services/documentService');

describe('DocumentUploadPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (documentService.uploadDocumentFile as jest.Mock).mockResolvedValue({
      id: 1,
      name: 'test-document.pdf',
      type: 'pdf',
      size: '1MB',
      uploaded_at: '2023-01-01',
      status: 'uploaded',
    });
  });

  const renderComponent = () =>
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/dashboard/upload-document"]}>
          <Routes>
            <Route path="/dashboard/upload-document" element={<DocumentUploadPage />} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

  test('renders upload form', () => {
    renderComponent();
    expect(screen.getByLabelText('Document Name:')).toBeInTheDocument();
    expect(screen.getByLabelText('Document Type (e.g., pdf, docx, zip):')).toBeInTheDocument();
    expect(screen.getByLabelText('Select File (max 500 MB):')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Upload Document/i })).toBeInTheDocument();
  });

  test('shows error message if fields are empty on submit', async () => {
    renderComponent();
    userEvent.click(screen.getByRole('button', { name: /Upload Document/i }));
    await waitFor(() => {
      expect(screen.getByText('Upload New Document')).toBeInTheDocument();
    });
  });


  test('shows error message on upload failure', async () => {
    (documentService.uploadDocumentFile as jest.Mock).mockRejectedValueOnce(new Error('Upload failed'));
    renderComponent();

    const file = new File([], 'test-document.txt', { type: 'application/txt' });

    await userEvent.type(screen.getByLabelText('Document Name:'), 'Test Document');
    await userEvent.type(screen.getByLabelText('Document Type (e.g., pdf, docx, zip):'), 'pdf');
    userEvent.upload(screen.getByLabelText('Select File (max 500 MB):'), file);

    userEvent.click(screen.getByRole('button', { name: /Upload Document/i }));

    await waitFor( () => {
       expect(screen.getByText('Invalid file type. Allowed types are: pdf, docx, zip.')).toBeInTheDocument();
    });
  });
});
