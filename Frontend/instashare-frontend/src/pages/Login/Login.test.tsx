import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { AuthProvider, useAuth } from '../../contexts/AuthContext'; // Import from actual context, but it will be mocked by Jest
import Login from './Login';

// Mock the useAuth hook to control authentication state during tests
jest.mock('../../contexts/AuthContext', () => ({
  // Keep actual AuthProvider for wrapping components if needed for broader tests, 
  // or replace it with a simple passthrough if only useAuth is mocked.
  AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  useAuth: jest.fn(),
}));

const mockUseAuth = useAuth as jest.MockedFunction<typeof useAuth>;

describe('Login Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockUseAuth.mockReset();
  });

  test('renders loading state correctly', () => {
    mockUseAuth.mockReturnValue({
      currentUser: null,
      session: null,
      loading: true,
      signInWithOAuth: jest.fn(),
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders welcome message when authenticated', () => {
    mockUseAuth.mockReturnValue({
      currentUser: {
        id: '123',
        email: 'test@example.com',
        aud: 'authenticated',
        app_metadata: {},
        user_metadata: { full_name: 'Test User' },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      session: {} as any,
      loading: false,
      signInWithOAuth: jest.fn(),
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    expect(screen.getByText('Welcome, Test User!')).toBeInTheDocument();
  });

  test('renders login buttons when unauthenticated', () => {
    mockUseAuth.mockReturnValue({
      currentUser: null,
      session: null,
      loading: false,
      signInWithOAuth: jest.fn(),
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    expect(screen.getByText('Login to InstaShare')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in with Google/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in with Facebook/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in with LinkedIn/i })).toBeInTheDocument();
  });

  test('calls signInWithOAuth with google provider when Google button is clicked', () => {
    const mockSignInWithOAuth = jest.fn();
    mockUseAuth.mockReturnValue({
      currentUser: null,
      session: null,
      loading: false,
      signInWithOAuth: mockSignInWithOAuth,
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sign in with Google/i }));
    expect(mockSignInWithOAuth).toHaveBeenCalledTimes(1);
    expect(mockSignInWithOAuth).toHaveBeenCalledWith('google');
  });

  test('calls signInWithOAuth with facebook provider when Facebook button is clicked', () => {
    const mockSignInWithOAuth = jest.fn();
    mockUseAuth.mockReturnValue({
      currentUser: null,
      session: null,
      loading: false,
      signInWithOAuth: mockSignInWithOAuth,
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sign in with Facebook/i }));
    expect(mockSignInWithOAuth).toHaveBeenCalledTimes(1);
    expect(mockSignInWithOAuth).toHaveBeenCalledWith('facebook');
  });

  test('calls signInWithOAuth with linkedin provider when LinkedIn button is clicked', () => {
    const mockSignInWithOAuth = jest.fn();
    mockUseAuth.mockReturnValue({
      currentUser: null,
      session: null,
      loading: false,
      signInWithOAuth: mockSignInWithOAuth,
      logOut: jest.fn(),
    });
    render(
      <AuthProvider>
        <Login />
      </AuthProvider>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sign in with LinkedIn/i }));
    expect(mockSignInWithOAuth).toHaveBeenCalledTimes(1);
    expect(mockSignInWithOAuth).toHaveBeenCalledWith('linkedin');
  });
});



