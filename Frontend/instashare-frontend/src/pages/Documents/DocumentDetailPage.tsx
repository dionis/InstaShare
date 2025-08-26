import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaEdit, FaTrash, FaCompressAlt, FaShareAlt, FaSave, FaBan, FaArrowLeft } from 'react-icons/fa';
// import Navbar from '../../components/Navbar/Navbar'; // Eliminar esta línea
import { documentService, Document, DocumentUploadInfo, DocumentSharedWithUser, CompressionJobResponse } from '../../services/documentService';
import { userService, User } from '../../services/userService'; // To fetch users for sharing
import styles from './DocumentDetailPage.module.css';

const DocumentDetailPage: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<Document | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedDocument, setEditedDocument] = useState<Partial<DocumentUploadInfo> | null>(null);
  const [sharedUsers, setSharedUsers] = useState<DocumentSharedWithUser[]>([]);
  const [availableUsers, setAvailableUsers] = useState<User[]>([]);
  const [selectedUserToShare, setSelectedUserToShare] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) {
        setError("Document ID is missing.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const fetchedDocument = await documentService.getDocumentById(Number(id));
        setDocument(fetchedDocument);
        setEditedDocument({ 
          name: fetchedDocument.name, 
          type: fetchedDocument.type, 
          uploaded_at: fetchedDocument.uploaded_at, 
          status: fetchedDocument.status 
        });

        const sharedResponse = await documentService.getUsersSharedWithDocument(Number(id));
        setSharedUsers(sharedResponse.shared_with);

        const usersResponse = await userService.getUsers();
        setAvailableUsers(usersResponse.filter(user => !sharedResponse.shared_with.some(su => su.id === user.id)));

      } catch (err) {
        console.error("Error fetching document details:", err);
        setError("Failed to load document details.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setEditedDocument((prev) => (prev ? { ...prev, [name]: value } : null));
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !editedDocument) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      await documentService.updateDocumentInfo(Number(id), editedDocument);
      setDocument((prev) => (prev ? { ...prev, ...editedDocument as Document } : null));
      setIsEditing(false);
      setMessage("Document updated successfully!");
    } catch (err: any) {
      console.error("Error updating document:", err);
      setError(err.message || "Failed to update document.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id || !window.confirm("Are you sure you want to delete this document?")) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      await documentService.deleteDocument(Number(id));
      setMessage("Document deleted successfully!");
      navigate('/dashboard/my-documents'); // Redirect after deletion
    } catch (err: any) {
      console.error("Error deleting document:", err);
      setError(err.message || "Failed to delete document.");
    } finally {
      setLoading(false);
    }
  };

  const handleShareDocument = async () => {
    if (!id || !selectedUserToShare) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      // This endpoint is not explicitly defined in 00_contract.md, 
      // assuming a POST to a /share_document endpoint with document_id and user_id.
      // For now, let's simulate or add a placeholder call.
      // For a full implementation, the backend needs a specific endpoint for sharing.
      console.log(`Sharing document ${id} with user ${selectedUserToShare}`);
      // await documentService.shareDocument(Number(id), Number(selectedUserToShare)); // Example call
      setMessage(`Document shared with user ${selectedUserToShare} successfully! (Simulated)`);
      setSelectedUserToShare('');
      // Re-fetch data to update shared users list
      const sharedResponse = await documentService.getUsersSharedWithDocument(Number(id));
      setSharedUsers(sharedResponse.shared_with);
      const usersResponse = await userService.getUsers();
      setAvailableUsers(usersResponse.filter(user => !sharedResponse.shared_with.some(su => su.id === user.id)));

    } catch (err: any) {
      console.error("Error sharing document:", err);
      setError(err.message || "Failed to share document.");
    } finally {
      setLoading(false);
    }
  };

  const handleStartCompressionJob = async () => {
    if (!id || !window.confirm("Are you sure you want to start a compression job for this document?")) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response: CompressionJobResponse = await documentService.startDocumentCompressionJob(Number(id));
      setMessage(`Compression job started successfully for document. Job ID: ${response.idjob}`);
    } catch (err: any) {
      console.error("Error starting compression job:", err);
      setError(err.message || "Failed to start compression job.");
    } finally {
      setLoading(false);
    }
  };

  if (loading && !document) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.loading}>Loading document details...</div>
      </div>
    );
  }

  if (error && !document) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  if (!document) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.noDocument}>Document not found.</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* <Navbar /> */}
      <div className={styles.header}>
        <h1>Document Details: {document.name}</h1>
        <div className={styles.headerActions}>
          <button onClick={() => setIsEditing(!isEditing)} className={styles.editButton}>
            {isEditing ? <><FaBan className={styles.icon} /> Cancel Edit</> : <><FaEdit className={styles.icon} /> Edit Info</>}
          </button>
          <button onClick={handleDelete} className={styles.deleteButton}>
            <FaTrash className={styles.icon} /> Delete Document
          </button>
          <button onClick={handleStartCompressionJob} className={styles.compressButton}>
            <FaCompressAlt className={styles.icon} /> Start Compression Job
          </button>
        </div>
      </div>

      <div className={styles.content}>
        {message && <p className={styles.successMessage}>{message}</p>}
        {error && <p className={styles.errorMessage}>{error}</p>}

        {!isEditing ? (
          <div className={styles.details}>
            <p><strong>ID:</strong> {document.id}</p>
            <p><strong>Name:</strong> {document.name}</p>
            <p><strong>Type:</strong> {document.type}</p>
            <p><strong>Size:</strong> {document.size}</p>
            <p><strong>Status:</strong> {document.status}</p>
            <p><strong>Uploaded At:</strong> {new Date(document.uploaded_at).toLocaleDateString()}</p>
            {document.created_at && <p><strong>Created At:</strong> {new Date(document.created_at).toLocaleDateString()}</p>}
            {document.updated_at && <p><strong>Last Updated:</strong> {new Date(document.updated_at).toLocaleDateString()}</p>}
          </div>
        ) : (
          <form onSubmit={handleUpdate} className={styles.editForm}>
            <div className={styles.inputGroup}>
              <label htmlFor="editedName">Name:</label>
              <input
                type="text"
                id="editedName"
                name="name"
                value={editedDocument?.name || ''}
                onChange={handleChange}
                required
              />
            </div>
            <div className={styles.inputGroup}>
              <label htmlFor="editedType">Type:</label>
              <input
                type="text"
                id="editedType"
                name="type"
                value={editedDocument?.type || ''}
                onChange={handleChange}
                required
              />
            </div>
            <div className={styles.actions}>
              <button type="submit" className={styles.saveButton}><FaSave className={styles.icon} /> Save Changes</button>
              <button type="button" onClick={() => setIsEditing(false)} className={styles.cancelButton}><FaBan className={styles.icon} /> Cancel</button>
            </div>
          </form>
        )}

        <div className={styles.sharingSection}>
          <h2>Share Document</h2>
          <div className={styles.shareForm}>
            <select
              value={selectedUserToShare}
              onChange={(e) => setSelectedUserToShare(e.target.value)}
              disabled={availableUsers.length === 0}
            >
              <option value="">Select a user to share with</option>
              {availableUsers.map(user => (
                <option key={user.id} value={user.id}>{user.name} ({user.email})</option>
              ))}
            </select>
            <button onClick={handleShareDocument} className={styles.shareButton} disabled={!selectedUserToShare}>
              <FaShareAlt className={styles.icon} /> Share
            </button>
          </div>
          
          <h3>Shared With:</h3>
          {sharedUsers.length === 0 ? (
            <p>Not shared with anyone yet.</p>
          ) : (
            <ul className={styles.sharedUserList}>
              {sharedUsers.map(user => (
                <li key={user.id}>
                  {user.name} ({user.email}) - Shared on: {new Date(user.shared_date).toLocaleDateString()}
                </li>
              ))}
            </ul>
          )}
        </div>

        <button type="button" onClick={() => navigate('/dashboard/my-documents')} className={styles.backButton} style={{ marginTop: '20px' }}>
          <FaArrowLeft className={styles.icon} /> Back to My Documents
        </button>
      </div>
    </div>
  );
};

export default DocumentDetailPage;
