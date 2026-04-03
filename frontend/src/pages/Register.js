import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API = 'http://localhost:8080/api';
function Register() {
  const navigate = useNavigate();
  const [form, setForm]       = useState({ name: '', email: '', password: '' });
  const [error, setError]     = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async e => {
    e.preventDefault();
    setError(''); setSuccess(''); setLoading(true);
    try {
      const res = await axios.post(`${API}/register`, form);
      localStorage.setItem('token',    res.data.token);
      localStorage.setItem('userName', res.data.name);
      setSuccess('Registration ho gayi! Dashboard pe ja raha hoon...');
      setTimeout(() => navigate('/dashboard'), 1000);
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
          <div className="emoji">🌿</div>
          <h1>Account Banao</h1>
          <p>Free mein apna carbon footprint track karo</p>
        </div>

        {error   && <div className="error-msg">⚠️ {error}</div>}
        {success && <div className="success-msg">✅ {success}</div>}

        <form onSubmit={submit}>
          <div className="form-group">
            <label>Poora Naam</label>
            <input
              type="text" name="name" required
              placeholder="Tumhara naam"
              value={form.name} onChange={handle}
            />
          </div>
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
              placeholder="Kam se kam 6 characters"
              value={form.password} onChange={handle}
            />
          </div>
          <button className="btn-primary" disabled={loading}>
            {loading ? 'Account ban raha hai...' : 'Register Karo'}
          </button>
        </form>

        <div className="auth-switch">
          Pehle se account hai? <Link to="/login">Login karo</Link>
        </div>
      </div>
    </div>
  );
}

export default Register;