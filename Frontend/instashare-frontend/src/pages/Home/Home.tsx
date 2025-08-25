import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Home.module.css';

function Home() {
  const { currentUser, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && currentUser) {
      navigate('/dashboard');
    }
  }, [currentUser, loading, navigate]);

  if (loading) {
    return <div className={styles.App}>Loading...</div>;
  }

  return (
    <div className={styles.App}>
      <header className={styles['App-header']}>
        <p>
          Welcome to InstaShare! Please login.
        </p>
        <a
          className={styles['App-link']}
          href="/login"
          rel="noopener noreferrer"
        >
          Login
        </a>
      </header>
    </div>
  );
}

export default Home;
