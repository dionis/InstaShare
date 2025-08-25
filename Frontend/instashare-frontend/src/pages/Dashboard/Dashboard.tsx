import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { userService, User } from '../../services/userService';
import Navbar from '../../components/Navbar/Navbar';
import styles from './Dashboard.module.css';

const Dashboard: React.FC = () => {
  const { currentUser, loading } = useAuth();
  const [userData, setUserData] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentUser && !loading) {
      const fetchUserData = async () => {
        try {
          // Assuming the backend has a way to get user data based on the authenticated user
          // For now, we'll just display Firebase user info.
          // In a real application, you'd fetch user data from your backend using currentUser.uid or email.
          // For demonstration, let's simulate fetching user data:
          // const fetchedUser = await userService.getUserById(someId);
          setUserData({ 
            id: 0, // Placeholder, as we don't have a backend ID yet from Firebase auth
            name: currentUser.displayName || '',
            email: currentUser.email || '',
            phone: '', 
            responsability: '',
            role: 'authenticated',
          });
        } catch (err) {
          console.error("Error fetching user data:", err);
          setError("Failed to fetch user data.");
        }
      };
      fetchUserData();
    }
  }, [currentUser, loading]);

  if (loading) {
    return <div className={styles.loading}>Loading dashboard...</div>;
  }

  if (!currentUser) {
    return <div className={styles.unauthorized}>Please log in to view the dashboard.</div>; // This should ideally be handled by routing protection
  }

  return (
    <div className={styles.dashboardContainer}>
      <Navbar />
      <header className={styles.dashboardHeader}>
        <h1>Welcome to InstaShare Dashboard</h1>
        {currentUser && (
          <p>Hello, {currentUser.user_metadata?.full_name || currentUser.email}!</p>
        )}
        {error && <p className={styles.error}>{error}</p>}
        {/* Add more dashboard content here */}
      </header>
    </div>
  );
};

export default Dashboard;
