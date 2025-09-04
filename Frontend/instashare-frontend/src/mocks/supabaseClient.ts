import { createClient, User, Session } from '@supabase/supabase-js';
import { act } from '@testing-library/react';

// Mock values
let mockCurrentUser: User | null = null;
let mockSession: Session | null = null;
const authStateChangeCallbacks: ((event: string, session: Session | null) => void)[] = [];

// Mock Auth object
const mockAuth = {
  async getSession() {
    return { data: { session: mockSession }, error: null };
  },
  onAuthStateChange(callback: (event: string, session: Session | null) => void) {
    authStateChangeCallbacks.push(callback);
    // No need to call act here, AuthContext useEffect will handle it
    // Call with current state immediately for initial setup, but not wrapped in act
    callback('INITIAL_SESSION', mockSession);
    return {
      data: {
        subscription: {
          unsubscribe: () => {
            const index = authStateChangeCallbacks.indexOf(callback);
            if (index > -1) {
              authStateChangeCallbacks.splice(index, 1);
            }
          },
        },
      },
    };
  },
  async signInWithOAuth({ provider, options }: { provider: 'google' | 'facebook' | 'linkedin'; options: { redirectTo: string } }) {
    const user: User = {
      id: 'mock-user-id-' + provider,
      email: `${provider}@example.com`,
      aud: 'authenticated',
      app_metadata: {},
      user_metadata: { full_name: `Mock User ${provider}` },
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    const session: Session = {
      access_token: `mock-access-token-${provider}`,
      token_type: 'Bearer',
      expires_in: 3600,
      expires_at: Math.floor(Date.now() / 1000) + 3600,
      refresh_token: `mock-refresh-token-${provider}`,
      user: user,
    };

    await act(async () => {
      mockCurrentUser = user;
      mockSession = session;
      authStateChangeCallbacks.forEach(cb => cb('SIGNED_IN', session));
    });
    return { data: { user, session }, error: null };
  },
  async signOut() {
    await act(async () => {
      mockCurrentUser = null;
      mockSession = null;
      authStateChangeCallbacks.forEach(cb => cb('SIGNED_OUT', null));
    });
    return { error: null };
  },
  async signInWithPassword({ email, password }: { email: string; password: string }) {
    if (email === 'test@example.com' && password === 'password') {
      const user: User = {
        id: 'mock-user-id-email',
        email: email,
        aud: 'authenticated',
        app_metadata: {},
        user_metadata: { full_name: 'Test User' },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      const session: Session = {
        access_token: 'mock-access-token-email',
        token_type: 'Bearer',
        expires_in: 3600,
        expires_at: Math.floor(Date.now() / 1000) + 3600,
        refresh_token: 'mock-refresh-token-email',
        user: user,
      };
      await act(async () => {
        mockCurrentUser = user;
        mockSession = session;
        authStateChangeCallbacks.forEach(cb => cb('SIGNED_IN', session));
      });
      return { data: { user, session }, error: null };
    } else {
      return { data: { user: null, session: null }, error: { name: 'AuthApiError', message: 'Invalid login credentials', status: 400 } };
    }
  },
};

// Mock Supabase client
const mockSupabase = {
  auth: mockAuth,
  from: jest.fn(() => ({
    select: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    update: jest.fn().mockReturnThis(),
    delete: jest.fn().mockReturnThis(),
    single: jest.fn().mockResolvedValue({ data: null, error: null }),
    remove: jest.fn().mockReturnThis(),
    // Add other methods if needed for your tests
  })),
};

export const supabase = mockSupabase as unknown as ReturnType<typeof createClient>;
export const __setMockSession = (session: Session | null) => {
  mockSession = session;
  mockCurrentUser = session?.user || null;
  // Trigger auth state change callbacks when session is manually set, wrapped in act for tests
  act(() => {
    authStateChangeCallbacks.forEach(cb => cb(session ? 'SIGNED_IN' : 'SIGNED_OUT', session));
  });
};
export const __setInitialSession = (session: Session | null) => {
  mockSession = session;
  mockCurrentUser = session?.user || null;
};
export const __clearAuthStateChangeCallbacks = () => {
  authStateChangeCallbacks.length = 0;
};
