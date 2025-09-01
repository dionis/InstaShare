import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import DocumentDetailPage from './DocumentDetailPage';
import { documentService } from '../../services/documentService';
import { userService } from '../../services/userService';
import { AuthProvider } from '../../contexts/AuthContext';

// Mock de react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
  useParams: jest.fn(),
}));

// Mock de documentService
jest.mock('../../services/documentService');

// Mock de userService
jest.mock('../../services/userService');

const mockDocument = {
  id: 1,
  name: 'My Awesome Document',
  type: 'pdf',
  size: '2.5MB',
  uploaded_at: '2023-01-15',
  status: 'active',
  created_at: '2023-01-10T10:00:00Z',
  updated_at: '2023-01-15T11:00:00Z',
};

const mockSharedWith = [
  { id: 101, name: 'Alice', email: 'alice@example.com', shared_date: '2023-02-01' },
  { id: 102, name: 'Bob', email: 'bob@example.com', shared_date: '2023-02-05' },
];

const mockAvailableUsers = [
  { id: 201, name: 'Charlie', email: 'charlie@example.com', phone: '', responsability: '', role: 'user', created_at: '', updated_at: '' },
  { id: 202, name: 'Diana', email: 'diana@example.com', phone: '', responsability: '', role: 'user', created_at: '', updated_at: '' },
];

describe('DocumentDetailPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // @ts-ignore
    jest.spyOn(require('react-router-dom'), 'useParams').mockReturnValue({ id: '1' });
    (documentService.getDocumentById as jest.Mock).mockResolvedValue(mockDocument);
    (documentService.getUsersSharedWithDocument as jest.Mock).mockResolvedValue({
      shared_with: mockSharedWith,
    });
    (userService.getUsers as jest.Mock).mockResolvedValue(mockAvailableUsers);
    (documentService.updateDocumentInfo as jest.Mock).mockResolvedValue(mockDocument);
    (documentService.deleteDocument as jest.Mock).mockResolvedValue({});
    (documentService.startDocumentCompressionJob as jest.Mock).mockResolvedValue({ idjob: 'job-123' });
  });

  const renderComponent = (path: string, initialEntries: string[]) =>
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={initialEntries}>
          <Routes>
            <Route path={path} element={<DocumentDetailPage />} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

  test('renders loading state initially', async () => {
    (documentService.getDocumentById as jest.Mock).mockReturnValueOnce(new Promise( () => {}));
    renderComponent('/dashboard/documents/:id', ['/dashboard/documents/1']);

    await waitFor( () => {
       expect(screen.getByText('Loading document details...')).toBeInTheDocument();
    });
  });

  test('renders document details', async () => {
    renderComponent('/dashboard/documents/:id', ['/dashboard/documents/1']);
    await waitFor(() => {
      expect(screen.getByText(`Document Details: ${mockDocument.name}`)).toBeInTheDocument();
      expect(screen.getByText(`Name:`)).toBeInTheDocument();
      expect(screen.getByText(`${mockDocument.name}`)).toBeInTheDocument();
      expect(screen.getByText(`Type:`)).toBeInTheDocument();
      expect(screen.getByText(`${mockDocument.type}`)).toBeInTheDocument();
      expect(screen.getByText(`Size:`)).toBeInTheDocument();
      expect(screen.getByText(`${mockDocument.size}`)).toBeInTheDocument();
      expect(screen.getByText(`Shared With:`)).toBeInTheDocument();
     });
  });

  test('switches to edit mode and updates document info', async () => {
    renderComponent('/dashboard/documents/:id', ['/dashboard/documents/1']);
    await waitFor(async () => screen.getByText(`Document Details: ${mockDocument.name}`));

    userEvent.click(screen.getByText('Edit Info'));

    const nameInput = await screen.findByLabelText('Name:') as HTMLInputElement;
    userEvent.clear(nameInput);
    await userEvent.type(nameInput, 'Updated Document Name');

    userEvent.click(screen.getByRole('button', { name: /Save Changes/i }));

    await waitFor(async() => {
      expect(screen.getByText('Document updated successfully!')).toBeInTheDocument();
      expect(screen.getByText(`Name:`)).toBeInTheDocument();
      expect(screen.getByText(`Updated Document Name`)).toBeInTheDocument();
    });
  });
 

  test('handles document deletion', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true);
    renderComponent('/dashboard/documents/:id', ['/dashboard/documents/1']);
    await waitFor(() => screen.getByText(`Document Details: ${mockDocument.name}`));

    userEvent.click(screen.getByText('Delete Document'));

    await waitFor(() => {
      expect(documentService.deleteDocument).toHaveBeenCalledWith(1);
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard/my-documents');
      expect(screen.getByText('Document deleted successfully!')).toBeInTheDocument();
    });
  });

  test('handles starting compression job', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true);
    renderComponent('/dashboard/documents/:id', ['/dashboard/documents/1']);
    await waitFor(() => screen.getByText(`Document Details: ${mockDocument.name}`));

    userEvent.click(screen.getByText('Start Compression Job'));

    await waitFor(() => {
      expect(documentService.startDocumentCompressionJob).toHaveBeenCalledWith(1);
      expect(screen.getByText('Compression job started successfully for document. Job ID: job-123')).toBeInTheDocument();
    });
  });
});
