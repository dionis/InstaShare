import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import UserDocumentsPage from './UserDocumentsPage';
import { userService } from '../../services/userService';
import { AuthProvider, useAuth } from '../../contexts/AuthContext';

// Mock de react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock de userService
jest.mock('../../services/userService');

// Mock de AuthContext (para simular el usuario autenticado)
jest.mock('../../contexts/AuthContext', () => ({
  ...jest.requireActual('../../contexts/AuthContext'),
  useAuth: jest.fn(),
}));

const mockUserDocuments = {
  upload_documents: [
    { id: 1, name: 'Report.pdf', type: 'pdf', size: '1.2MB', uploaded_at: '2023-03-01', status: 'active' },
    { id: 2, name: 'ProjectPlan.docx', type: 'docx', size: '0.8MB', uploaded_at: '2023-03-05', status: 'active' },
  ],
};

describe('UserDocumentsPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (userService.getDocumentsUploadedByUser as jest.Mock).mockResolvedValue(mockUserDocuments);
    (useAuth as jest.Mock).mockReturnValue({
      currentUser: { id: 'test-user-id', email: 'test@example.com' },
      loading: false,
    });
  });

  const renderComponent = () =>
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/dashboard/my-documents"]}>
          <Routes>
            <Route path="/dashboard/my-documents" element={<UserDocumentsPage />} />
            <Route path="/dashboard/upload-document" element={<div>Upload Document Page</div>} />
            <Route path="/dashboard/documents/:id" element={<div>Document Detail Page</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

  test('renders loading state initially', () => {
    (useAuth as jest.Mock).mockReturnValue({
      currentUser: null,
      loading: true,
    });
    renderComponent();
    expect(screen.getByText('Loading your documents...')).toBeInTheDocument();
  });

  test('renders error message if not authenticated', async () => {
    (useAuth as jest.Mock).mockReturnValue({
      currentUser: null,
      loading: false,
    });
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('Please log in to view your documents.')).toBeInTheDocument();
    });
  });

  test(`renders user documents after fetching`, async () => {
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('My Uploaded Documents')).toBeInTheDocument();
      expect(screen.getByText('Report.pdf (pdf) - 1.2MB')).toBeInTheDocument();
      expect(screen.getByText('ProjectPlan.docx (docx) - 0.8MB')).toBeInTheDocument();
    });
  });

  test('renders message when no documents are uploaded', async () => {
    (userService.getDocumentsUploadedByUser as jest.Mock).mockResolvedValue({
      upload_documents: [],
    });
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('You haven\'t uploaded any documents yet.')).toBeInTheDocument();
    });
  });

  test('navigates to upload document page', async () => {
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('Upload New Document')).toBeInTheDocument();
    });
    userEvent.click(screen.getByText('Upload New Document'));
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard/upload-document');
  });

  test('navigates to document detail page on View/Manage click', async () => {
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('View/Manage', { selector: 'a' })).toBeInTheDocument();
    });
    userEvent.click(screen.getAllByText('View/Manage', { selector: 'a' })[0]); // Click the first link
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard/documents/1');
  });
});
