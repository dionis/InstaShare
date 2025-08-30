import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { supabase } from '../../services/supabaseClient';
import { useNavigate } from 'react-router-dom';
import styles from './Login.module.css';
import { FcGoogle } from 'react-icons/fc';
import { FaFacebook, FaLinkedin } from 'react-icons/fa';

const Login: React.FC = () => {
  const { signInWithOAuth, currentUser, loading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState<string | null>(null);
  const navigate = useNavigate();
  const handleOAuthLogin = async (provider: 'google' | 'facebook' | 'linkedin') => {
    setLoginError(null);
    try {
      await signInWithOAuth(provider);
    } catch (error) {
      console.error(`Error during ${provider} login:`, error);
      setLoginError(`Failed to log in with ${provider}. Please try again.`);
    }
  };

  const handleEmailPasswordLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    try {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) {
        if (error.message.includes("invalid login credentials")) {
          setLoginError("Invalid email or password.");
        } else {
          throw error;
        }
      } else {
        console.log("Email/Password login successful");
        // No need to redirect manually here, AuthContext will update and Home.tsx will redirect
      }
    } catch (error: any) {
      console.error("Error during email/password login:", error);
      setLoginError(error.message || "Failed to log in with email and password.");
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (currentUser) {
     navigate('/dashboard');
  }

  return (
    <div className={styles.loginContainer}>
      <h1>Login to InstaShare</h1>

      <form onSubmit={handleEmailPasswordLogin} className={styles.loginForm}>
        <div className={styles.inputGroup}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className={styles.emailPasswordButton}>
          Login with Email
        </button>
      </form>

      {loginError && <p className={styles.error}>{loginError}</p>}

      <div className={styles.socialLoginSeparator}>OR</div>

      <div className={styles.socialLoginButtons}>
        <button onClick={() => handleOAuthLogin('google')} className={styles.googleButton}>
          <FcGoogle className={styles.icon} /> Sign in with Google
        </button>
        <button onClick={() => handleOAuthLogin('facebook')} className={styles.facebookButton}>
          <FaFacebook className={styles.icon} /> Sign in with Facebook
        </button>
        <button onClick={() => handleOAuthLogin('linkedin')} className={styles.linkedinButton}>
          <FaLinkedin className={styles.icon} /> Sign in with LinkedIn
        </button>
      </div>
    </div>
  );
};

export default Login;
