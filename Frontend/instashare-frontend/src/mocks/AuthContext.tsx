import React, { createContext, useContext, useState } from 'react';
import { User, Session } from '@supabase/supabase-js';

interface AuthContextType {
  currentUser: User | null;
  session: Session | null;
  loading: boolean;
  signInWithOAuth: (provider: 'google' | 'facebook' | 'linkedin') => Promise<void>;
  logOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true); // Start as loading, like the real AuthContext

  const signInWithOAuth = jest.fn(async (provider: 'google' | 'facebook' | 'linkedin') => {
    console.log(`Mock signInWithOAuth called for ${provider}`);
    const mockUser: User = { 
      id: 'mock-user-id', 
      email: 'mock@example.com', 
      aud: 'authenticated', 
      app_metadata: {}, 
      user_metadata: { full_name: 'Mock User' }, 
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    const mockSession: Session = {
      access_token: 'mock-access-token',
      token_type: 'Bearer',
      expires_in: 3600,
      expires_at: Math.floor(Date.now() / 1000) + 3600,
      refresh_token: 'mock-refresh-token',
      user: mockUser,
    };
    setCurrentUser(mockUser);
    setSession(mockSession);
    setLoading(false); // Set loading to false after sign in
  });

  const logOut = jest.fn(async () => {
    console.log("Mock logOut called");
    setCurrentUser(null);
    setSession(null);
    setLoading(false); // Set loading to false after sign out
  });

  // Helper to control the loading state from tests
  const __setMockLoading = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  const value = {
    currentUser,
    session,
    loading,
    signInWithOAuth,
    logOut,
    __setMockLoading, // Expose helper for tests
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};






