import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import Register from './components/auth/Register';
import Login from './components/auth/Login';
import ApplicationList from './components/applications/ApplicationList';
// import ApplicationForm from './components/applications/ApplicationForm'; // Will be used later

import './App.css';

function PrivateRoute({ children }) {
    const { isAuthenticated } = useAuth();
    return isAuthenticated() ? children : <Navigate to="/login" />;
}

function App() {
    return (
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
            <AuthProvider>
                <div className="App">
                    <a href="#main-content" className="skip-link">Skip to main content</a>
                    <header className="App-header">
                        <h1 aria-label="Job Application Tracker Heading">Job Application Tracker</h1>
                    </header>
                    <main id="main-content" aria-label="Main content area">
                        <Routes>
                            <Route path="/register" element={<Register />} />
                            <Route path="/login" element={<Login />} />
                            <Route
                                path="/dashboard"
                                element={
                                    <PrivateRoute>
                                        <ApplicationList />
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
