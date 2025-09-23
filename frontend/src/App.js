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
        <BrowserRouter>
            <AuthProvider>
                <div className="App">
                    <header className="App-header">
                        <h1>Job Application Tracker</h1>
                    </header>
                    <main>
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
