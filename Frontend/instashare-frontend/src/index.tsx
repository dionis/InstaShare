import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import UserListPage from './pages/Users/UserListPage';
import UserDetailPage from './pages/Users/UserDetailPage';
import DocumentUploadPage from './pages/Documents/DocumentUploadPage';
import UserDocumentsPage from './pages/Documents/UserDocumentsPage';
import DocumentDetailPage from './pages/Documents/DocumentDetailPage';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>}>
            <Route path="users" element={<UserListPage />} />
            <Route path="users/:id" element={<UserDetailPage />} />
            <Route path="upload-document" element={<DocumentUploadPage />} />
            <Route path="my-documents" element={<UserDocumentsPage />} />
            <Route path="documents/:id" element={<DocumentDetailPage />} />
            <Route index element={<h2 style={{ textAlign: 'center', padding: '20px' }}>Select an option from the sidebar</h2>} />
          </Route>
          {/* Add other top-level routes here */}
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
