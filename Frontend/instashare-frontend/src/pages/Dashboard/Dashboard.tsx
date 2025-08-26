import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/Sidebar/Sidebar';
import styles from './Dashboard.module.css';

const Dashboard: React.FC = () => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return <div className={styles.loading}>Loading dashboard...</div>;
  }

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
};

export default Dashboard;
