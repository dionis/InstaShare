import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
import styles from './Navbar.module.css'; // This import is correct for CSS Modules.
import { FaCog, FaUserCircle } from 'react-icons/fa';

const Navbar: React.FC = () => {
  const { currentUser, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
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
            <Link to="/dashboard/profile" className={styles.navButton}>
              <FaUserCircle className={styles.icon} /> Mi Perfil
            </Link>
            <Link to="/dashboard/settings" className={styles.navButton}>
              <FaCog className={styles.icon} /> Configuración
            </Link>
            <span className={styles.userName}>Welcome, {currentUser.user_metadata?.full_name || currentUser.email}</span>
            <button onClick={handleLogout} className={styles.navButton}>Logout</button>
          </>
        ) : (
          <Link to="/login" className={styles.navButton}>Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 
