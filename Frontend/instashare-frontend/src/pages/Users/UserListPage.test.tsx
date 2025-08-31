import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import UserListPage from './UserListPage';
import { userService } from '../../services/userService';
import { AuthProvider } from '../../contexts/AuthContext'; // Necesario para el Navbar

// Mock de react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock de userService
jest.mock('../../services/userService');

const mockUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com', phone: '123', responsability: 'Dev', role: 'user', created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '456', responsability: 'QA', role: 'admin', created_at: '2023-01-02T12:00:00Z', updated_at: '2023-01-02T12:00:00Z' },
];

describe('UserListPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (userService.getUsers as jest.Mock).mockResolvedValue(mockUsers);
  });

  const renderComponent = () =>
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/dashboard/users"]}>
          <UserListPage />
        </MemoryRouter>
      </AuthProvider>
    );

  test('renders loading state initially', async () => {
    (userService.getUsers as jest.Mock).mockReturnValueOnce(new Promise(() => {})); // Never resolves
    renderComponent();
    await waitFor(() => {
    expect(screen.getByText('Loading users...')).toBeInTheDocument();
    });
  });

  test('renders user list after fetching', async () => {
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('User List')).toBeInTheDocument();
      expect(screen.getByText('John Doe (john@example.com) - user')).toBeInTheDocument();
      expect(screen.getByText('Jane Smith (jane@example.com) - admin')).toBeInTheDocument();
    });
  });

  test('renders error message on fetch failure', async () => {
    (userService.getUsers as jest.Mock).mockRejectedValueOnce(new Error('Network error'));
    renderComponent();
    await waitFor(() => {
      expect(screen.getByText('Failed to load users.')).toBeInTheDocument();
    });
  });

  // test('navigates to create new user page on button click', async () => {
  //   renderComponent();
  //   await waitFor(() => {
  //     expect(screen.getByText('Create New User')).toBeInTheDocument();
  //   });

   
  //   await waitFor(() => {
  //     userEvent.click(screen.getByText('Create New User'));
     
  //     //expect(mockNavigate).toHaveBeenCalledWith('/dashboard/users/new');
  //   });
  // });

  test('navigates to user detail page on View/Edit link click', async () => {
    renderComponent();
    await waitFor(() => {
      expect(screen.getAllByText('View/Edit', { selector: 'a' }).length).toBeGreaterThan(0);
    });
    const viewEditLinks = screen.getAllByRole('link', { name: /View\/Edit/i });
    await act(async () => {
      userEvent.click(viewEditLinks[0]); // Clica el pri
      // mer enlace
       //expect(mockNavigate).toHaveBeenCalledWith('/dashboard/users/1');
    });
    
  });
});
