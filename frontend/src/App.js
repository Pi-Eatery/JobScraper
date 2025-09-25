import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import Register from './components/auth/Register';
import Login from './components/auth/Login';

import Dashboard from './components/Dashboard'; // Import the Dashboard component
import KeywordManager from './components/keywords/KeywordManager'; // Import KeywordManager

import './App.css';

// Accessibility Note: Ensure all new components and modifications adhere to WCAG 2.1 AA standards.
// This includes proper ARIA attributes, keyboard navigation, and focus management.

function PrivateRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  console.log('PrivateRoute - Loading:', loading);
  console.log('PrivateRoute - isAuthenticated:', isAuthenticated());

  if (loading) {
    return <div>Loading authentication...</div>; // Or a spinner component
  }

  return isAuthenticated() ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <AuthProvider>
        <div className="App">
          <a href="#main-content" className="skip-link">
            Skip to main content
          </a>
          <header className="App-header">
            <h1 aria-label="Job Application Tracker Heading">
              Job Application Tracker
            </h1>
            <nav>
              <ul
                style={{
                  listStyle: 'none',
                  padding: 0,
                  display: 'flex',
                  gap: '15px',
                }}
              >
                <li>
                  <a href="/dashboard">Dashboard</a>
                </li>
                <li>
                  <a href="/keywords">Manage Keywords</a>
                </li>
              </ul>
            </nav>
          </header>
          <main id="main-content" aria-label="Main content area">
            <Routes>
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login />} />
              <Route
                path="/dashboard"
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/keywords"
                element={
                  <PrivateRoute>
                    <KeywordManager />
                  </PrivateRoute>
                }
              />
              <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
