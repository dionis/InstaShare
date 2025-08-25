import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Navbar.module.css';

const Navbar: React.FC = () => {
  const { currentUser, logOut } = useAuth();

  const handleLogout = async () => {
    try {
      await logOut();
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.brand}>InstaShare</div>
      <div className={styles.navLinks}>
        {currentUser ? (
          <>
            <span className={styles.userName}>Welcome, {currentUser.displayName || currentUser.email}</span>
            <button onClick={handleLogout} className={styles.navButton}>Logout</button>
          </>
        ) : (
          <a href="/login" className={styles.navButton}>Login</a>
        )}
      </div>
    </nav>
  );
};

export default Navbar;




