import React from 'react';
import { NavLink } from 'react-router-dom';
import styles from './Sidebar.module.css';
import { FaTachometerAlt, FaUsers, FaFileAlt, FaUpload } from 'react-icons/fa';

const Sidebar: React.FC = () => {
  return (
    <div className={styles.sidebar}>
      <nav className={styles.navMenu}>
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.active}` : styles.navLink
          }
          end
        >
          <FaTachometerAlt className={styles.icon} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink
          to="/dashboard/users"
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.active}` : styles.navLink
          }
        >
          <FaUsers className={styles.icon} />
          <span>List Users</span>
        </NavLink>
        <NavLink
          to="/dashboard/my-documents"
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.active}` : styles.navLink
          }
        >
          <FaFileAlt className={styles.icon} />
          <span>My Documents</span>
        </NavLink>
        <NavLink
          to="/dashboard/upload-document"
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.active}` : styles.navLink
          }
        >
          <FaUpload className={styles.icon} />
          <span>Upload Document</span>
        </NavLink>
      </nav>
    </div>
  );
};

export default Sidebar;
