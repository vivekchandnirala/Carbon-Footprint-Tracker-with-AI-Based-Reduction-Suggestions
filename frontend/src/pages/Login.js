import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API = 'http://localhost:8080/api';
function Login() {
  const navigate = useNavigate();
  const [form, setForm]     = useState({ email: '', password: '' });
  const [error, setError]   = useState('');
  const [loading, setLoading] = useState(false);

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async e => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      const res = await axios.post(`${API}/login`, form);
      localStorage.setItem('token',    res.data.token);
      localStorage.setItem('userName', res.data.name);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Kuch gadbad ho gayi!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-logo">
          <div className="emoji">🌱</div>
          <h1>Carbon Tracker</h1>
          <p>Apna carbon footprint track karo</p>
        </div>

        {error && <div className="error-msg">⚠️ {error}</div>}

        <form onSubmit={submit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email" name="email" required
              placeholder="apna@email.com"
              value={form.email} onChange={handle}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password" name="password" required
              placeholder="••••••••"
              value={form.password} onChange={handle}
            />
          </div>
          <button className="btn-primary" disabled={loading}>
            {loading ? 'Login ho raha hai...' : 'Login Karo'}
          </button>
        </form>

        <div className="auth-switch">
          Account nahi hai? <Link to="/register">Register karo</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;