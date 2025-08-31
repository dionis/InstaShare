import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/Sidebar/Sidebar';
import styles from './Dashboard.module.css';

const Dashboard: React.FC = () => {
  const { currentUser, loading } = useAuth();
   const [error, setError] = useState<string | null>(null);

  if (loading) {
    return <div className={styles.loading}>Loading dashboard...</div>;
  }

  if (!loading && !currentUser) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.error}>Please log in to view the dashboard.</div>
      </div>
    );
  } else {
    return (
      <div className={styles.dashboardLayout}>
        <Sidebar />
        <div className={styles.dashboardContent}>
          <header className={styles.dashboardHeader}>
            <h1>Welcome to InstaShare Dashboard</h1>
            {currentUser && (
              <p>Hello, {currentUser.user_metadata?.full_name || currentUser.email}!</p>
            )}
          </header>
          <main className={styles.mainContent}>
            <Outlet /> {/* Render nested routes here */}
          </main>
        </div>
      </div>
    );

  } 
};

export default Dashboard;
