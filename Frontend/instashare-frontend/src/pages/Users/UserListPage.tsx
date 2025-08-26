import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FaUserPlus, FaEdit } from 'react-icons/fa';
// import Navbar from '../../components/Navbar/Navbar'; // Eliminar esta línea
import { userService, User } from '../../services/userService';
import styles from './UserListPage.module.css';

const UserListPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const fetchedUsers = await userService.getUsers();
        setUsers(fetchedUsers);
      } catch (err) {
        console.error("Error fetching users:", err);
        setError("Failed to load users.");
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

  if (loading) {
    return (
      <div className={styles.container}>
        {/* <Navbar /> */}
        <div className={styles.loading}>Loading users...</div>
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
        <h1>User List</h1>
        <Link to="/dashboard/users/new" className={styles.createButton}><FaUserPlus className={styles.icon} /> Create New User</Link>
      </div>
      <ul className={styles.userList}>
        {users.map((user) => (
          <li key={user.id} className={styles.userListItem}>
            <span>{user.name} ({user.email}) - {user.role}</span>
            <Link to={`/dashboard/users/${user.id}`} className={styles.viewButton}><FaEdit className={styles.icon} /> View/Edit</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserListPage;
