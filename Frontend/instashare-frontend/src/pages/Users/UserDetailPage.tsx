import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaSave, FaTrash, FaUserTag, FaArrowLeft } from 'react-icons/fa';
import { userService, User } from '../../services/userService';
import styles from './UserDetailPage.module.css';

const UserDetailPage: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const isNewUser = id === 'new';

  const [user, setUser] = useState<Partial<User>>({
    name: '',
    email: '',
    phone: '',
    responsability: '',
    role: 'user', // Default role
    password: '',
    confirmPassword: '', // Initialize confirmPassword
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [passwordMismatchError, setPasswordMismatchError] = useState<string | null>(null);

  useEffect(() => {
    if (!isNewUser && id) {
      const fetchUser = async () => {
        try {
          setLoading(true);
          const fetchedUser = await userService.getUserById(Number(id));
          setUser(fetchedUser);
        } catch (err) {
          console.error("Error fetching user:", err);
          setError("Failed to load user data.");
        } finally {
          setLoading(false);
        }
      };
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [id, isNewUser]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setPasswordMismatchError(null); // Clear mismatch error on change
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    setPasswordMismatchError(null); // Clear mismatch error on submit

    try {
      if (isNewUser) {
        if (!user.name || !user.email || !user.password || !user.responsability) {
          throw new Error("Please fill in all required fields.");
        }
        if (user.password !== user.confirmPassword) {
          setPasswordMismatchError("Passwords do not match.");
          setLoading(false);
          return; // Stop form submission
        }
        await userService.createUser({ 
          name: user.name, 
          email: user.email, 
          phone: user.phone || '', 
          responsability: user.responsability, 
          password: user.password 
        });
        setMessage("User created successfully!");
        navigate('/dashboard/users');
      } else if (id) {
        await userService.updateUser(Number(id), user);
        setMessage("User updated successfully!");
      }
    } catch (err: any) {
      console.error("Error saving user:", err);
      setError(err.message || "Failed to save user.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id || isNewUser) return;
    if (!window.confirm("Are you sure you want to delete this user?")) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      await userService.deleteUser(Number(id));
      setMessage("User deleted successfully!");
      navigate('/dashboard/users'); // Redirect to user list after deletion
    } catch (err: any) {
      console.error("Error deleting user:", err);
      setError(err.message || "Failed to delete user.");
    } finally {
      setLoading(false);
    }
  };

  const handleAssignRole = async () => {
    if (!id || isNewUser || !user.role) return;
    if (!window.confirm(`Are you sure you want to assign ${user.role} to this user?`)) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      // This endpoint assumes role_id is passed, but our current contract only has role_name.
      // For a full implementation, we would need a role service to get role ID by name.
      // For now, let's assume a mapping or simplify.
      // For demonstration, let's call with a placeholder roleId.
      await userService.assignRoleToUser(Number(id), 1); // Placeholder roleId
      setMessage(`Role '${user.role}' assigned successfully!`);
    } catch (err: any) {
      console.error("Error assigning role:", err);
      setError(err.message || "Failed to assign role.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading user data...</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* <Navbar /> */}
      <div className={styles.header}>
        <h1>{isNewUser ? 'Create New User' : `User Details for ${user.name || user.email}`}</h1>
      </div>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputGroup}>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={user.name || ''}
            onChange={handleChange}
            required           
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={user.email || ''}
            onChange={handleChange}
            required
            disabled={!isNewUser}
          />
        </div>
        {!isNewUser && user.created_at && (
          <div className={styles.inputGroup}>
            <label>Created At:</label>
            <input type="text" value={new Date(user.created_at).toLocaleDateString()} disabled />
          </div>
        )}
        {!isNewUser && user.updated_at && (
          <div className={styles.inputGroup}>
            <label>Updated At:</label>
            <input type="text" value={new Date(user.updated_at).toLocaleDateString()} disabled />
          </div>
        )}
        {isNewUser && (
          <div className={styles.inputGroup}>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={user.password || ''}
              onChange={handleChange}
              required={isNewUser}
            />
          </div>
        )}
        {isNewUser && (
          <div className={styles.inputGroup}>
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={user.confirmPassword || ''}
              onChange={handleChange}
              required={isNewUser}
            />
          </div>
        )}
        <div className={styles.inputGroup}>
          <label htmlFor="phone">Phone:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={user.phone || ''}            
            onChange={handleChange}
            maxLength={20}
            pattern="[0-9]{7,20}" // Assuming phone numbers are 7-20 digits and only numbers
            title="Please enter only digits for the phone number (7-20 characters)"
            inputMode="numeric" // Added to enforce numeric keyboard on mobile devices
          />
          <small className={styles.inputHint}>Enter 7-20 digits for the phone number.</small>
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="responsability">Responsibility:</label>
          <input
            type="text"
            id="responsability"
            name="responsability"
            value={user.responsability || ''}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="role">Role:</label>
          <select
            id="role"
            name="role"
            value={user.role || ''}
            onChange={handleChange}
            required
          >
            <option value="">Select a role</option>
            <option value="user">User</option>
            <option value="admin">Admin</option>
            {/* Add more roles as needed from backend */}
          </select>
        </div>

        <div className={styles.actions}>
          <button type="submit" className={styles.saveButton} disabled={loading}>
            {isNewUser ? <><FaSave className={styles.icon} /> Create User</> : <><FaSave className={styles.icon} /> Update User</>}
          </button>
          {!isNewUser && (
            <button type="button" onClick={handleDelete} className={styles.deleteButton} disabled={loading}>
              <FaTrash className={styles.icon} /> Delete User
            </button>
          )}
          {!isNewUser && (
            <button type="button" onClick={handleAssignRole} className={styles.assignRoleButton} disabled={loading}>
              <FaUserTag className={styles.icon} /> Assign Role
            </button>
          )}
          <button type="button" onClick={() => navigate('/dashboard/users')} className={styles.backButton} disabled={loading}>
            <FaArrowLeft className={styles.icon} /> Back to List
          </button>
        </div>
      </form>
      {message && <p className={styles.successMessage}>{message}</p>}
      {error && <p className={styles.errorMessage}>{error}</p>}
      {passwordMismatchError && <p className={styles.errorMessage}>{passwordMismatchError}</p>}
    </div>
  );
};

export default UserDetailPage;
