import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { AuthProvider, useAuth } from '../context/AuthContext';

// Mock localStorage
const localStorageMock = (function () {
  let store = {};
  return {
    getItem: function (key) {
      return store[key] || null;
    },
    setItem: function (key, value) {
      store[key] = value.toString();
    },
    removeItem: function (key) {
      delete store[key];
    },
    clear: function () {
      store = {};
    },
  };
})();
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// A test component to consume the AuthContext
const TestComponent = () => {
  const { user, token, login, logout, isAuthenticated } = useAuth();
  return (
    <div>
      <span data-testid="user">{user ? user.username : 'No User'}</span>
      <span data-testid="token">{token || 'No Token'}</span>
      <span data-testid="authenticated">
        {isAuthenticated() ? 'Authenticated' : 'Not Authenticated'}
      </span>
      <button onClick={() => login('testuser', 'testpass')}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  it('provides initial unauthenticated state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('user')).toHaveTextContent('No User');
    expect(screen.getByTestId('token')).toHaveTextContent('No Token');
    expect(screen.getByTestId('authenticated')).toHaveTextContent(
      'Not Authenticated'
    );
  });

  it('logs in a user successfully and stores token', async () => {
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ access_token: 'new-fake-token' }),
      })
    );

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(localStorage.getItem('access_token')).toBe('new-fake-token');
    });
    expect(screen.getByTestId('user')).toHaveTextContent('testuser');
    expect(screen.getByTestId('token')).toHaveTextContent('new-fake-token');
    expect(screen.getByTestId('authenticated')).toHaveTextContent(
      'Authenticated'
    );
  });

  it('logs out a user and clears token', async () => {
    localStorage.setItem('access_token', 'existing-token');
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially, user should be authenticated from localStorage token
    expect(screen.getByTestId('authenticated')).toHaveTextContent(
      'Authenticated'
    );

    fireEvent.click(screen.getByRole('button', { name: /logout/i }));

    await waitFor(() => {
      expect(localStorage.getItem('access_token')).toBeNull();
    });
    expect(screen.getByTestId('user')).toHaveTextContent('No User');
    expect(screen.getByTestId('token')).toHaveTextContent('No Token');
    expect(screen.getByTestId('authenticated')).toHaveTextContent(
      'Not Authenticated'
    );
  });
});
