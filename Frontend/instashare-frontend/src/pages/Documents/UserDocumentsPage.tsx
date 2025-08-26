import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FaUpload, FaEye } from 'react-icons/fa';
// import Navbar from '../../components/Navbar/Navbar'; // Eliminar esta línea
import { userService, UserDocumentsResponse } from '../../services/userService';
import { useAuth } from '../../contexts/AuthContext';
import styles from './UserDocumentsPage.module.css';

const UserDocumentsPage: React.FC = () => {
  const { currentUser, loading: authLoading } = useAuth();
  const [documents, setDocuments] = useState<UserDocumentsResponse['upload_documents']>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && currentUser?.id) {
      const fetchUserDocuments = async () => {
        try {
          setLoading(true);
          // Assuming currentUser.id is the ID needed by the backend endpoint
          const response = await userService.getDocumentsUploadedByUser(Number(currentUser.id));
          setDocuments(response.upload_documents);
        } catch (err) {
          console.error("Error fetching user documents:", err);
          setError("Failed to load your documents.");
        } finally {
          setLoading(false);
        }
      };
      fetchUserDocuments();
    } else if (!authLoading && !currentUser) {
      setError("Please log in to view your documents.");
      setLoading(false);
    }
  }, [currentUser, authLoading]);

  if (authLoading || loading) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.loading}>Loading your documents...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* <Navbar /> */}
      <div className={styles.header}>
        <h1>My Uploaded Documents</h1>
        <Link to="/dashboard/upload-document" className={styles.uploadButton}><FaUpload className={styles.icon} /> Upload New Document</Link>
      </div>
      {documents.length === 0 ? (
        <p className={styles.noDocuments}>You haven't uploaded any documents yet.</p>
      ) : (
        <ul className={styles.documentList}>
          {documents.map((doc) => (
            <li key={doc.id} className={styles.documentListItem}>
              <span>{doc.name} ({doc.type}) - {doc.size}</span>
              <Link to={`/dashboard/documents/${doc.id}`} className={styles.viewButton}><FaEye className={styles.icon} /> View/Manage</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default UserDocumentsPage;
