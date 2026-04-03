import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate  = useNavigate();
  const name      = localStorage.getItem('userName') || 'User';

  const logout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/dashboard" className="navbar-brand">
        🌱 Carbon<span>Tracker</span>
      </Link>
      <div className="navbar-links">
        <span style={{ color: '#95d5b2', fontSize: 14 }}>👋 {name}</span>
        <button className="btn-logout" onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;