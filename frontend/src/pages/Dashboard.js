import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API = 'http://localhost:8080/api';
const initialForm = {
  body_type             : 'normal',
  diet                  : 'omnivore',
  transport             : 'public transport',
  vehicle_monthly_km    : 0,
  energy_source         : 'mixed',
  monthly_grocery_inr   : 3000,
  social_activity       : 'sometimes',
  flights_per_year      : 1,
  home_size             : 'medium',
  recycles              : 'sometimes',
  heating_cooling_usage : 'sometimes',
  new_clothes_monthly   : 3,
  internet_hours_daily  : 5,
};

function Dashboard() {
  const navigate       = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  const handle = e => {
    const val = ['vehicle_monthly_km','monthly_grocery_inr','flights_per_year',
                  'new_clothes_monthly','internet_hours_daily'].includes(e.target.name)
      ? Number(e.target.value)
      : e.target.value;
    setForm({ ...form, [e.target.name]: val });
  };

  const submit = async e => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await axios.post(`${API}/predict`, form, { headers });
      navigate('/result', { state: { result: res.data, formData: form } });
    } catch (err) {
      setError(err.response?.data?.error || 'Server se connect nahi ho pa raha!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">🌍 Apna Carbon Footprint Calculate Karo</h1>
      <p className="page-subtitle">
        Niche diye gaye forms mein apni daily activities fill karo — AI tumhara CO₂ score calculate karega
      </p>

      {error && <div className="error-msg">⚠️ {error}</div>}

      <form onSubmit={submit}>

        {/* Section 1: Personal */}
        <div className="form-card">
          <h3>👤 Personal Info</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Body Type</label>
              <select name="body_type" value={form.body_type} onChange={handle}>
                <option value="underweight">Underweight</option>
                <option value="normal">Normal</option>
                <option value="overweight">Overweight</option>
                <option value="obese">Obese</option>
              </select>
            </div>
            <div className="form-group">
              <label>Ghar ka Size</label>
              <select name="home_size" value={form.home_size} onChange={handle}>
                <option value="small">Chota (1-2 rooms)</option>
                <option value="medium">Medium (3-4 rooms)</option>
                <option value="large">Bada (5+ rooms)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Diet */}
        <div className="form-card">
          <h3>🥗 Khaana Peena</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Diet Type</label>
              <select name="diet" value={form.diet} onChange={handle}>
                <option value="vegan">Vegan (sirf plant-based)</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="pescatarian">Pescatarian (fish+veg)</option>
                <option value="omnivore">Omnivore (sab kuch)</option>
              </select>
            </div>
            <div className="form-group">
              <label>Monthly Grocery (₹)</label>
              <input
                type="number" name="monthly_grocery_inr" min="500" max="20000"
                value={form.monthly_grocery_inr} onChange={handle}
              />
            </div>
          </div>
        </div>

        {/* Section 3: Transport */}
        <div className="form-card">
          <h3>🚗 Transport</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Main Transport</label>
              <select name="transport" value={form.transport} onChange={handle}>
                <option value="walk/cycle">Paidal / Cycle</option>
                <option value="public transport">Bus / Metro / Train</option>
                <option value="motorbike">Motorbike / Scooter</option>
                <option value="private car">Private Car</option>
              </select>
            </div>
            <div className="form-group">
              <label>Private Vehicle Monthly km</label>
              <input
                type="number" name="vehicle_monthly_km" min="0" max="5000"
                value={form.vehicle_monthly_km} onChange={handle}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Flights Per Year ✈️</label>
              <input
                type="number" name="flights_per_year" min="0" max="50"
                value={form.flights_per_year} onChange={handle}
              />
            </div>
          </div>
        </div>

        {/* Section 4: Energy */}
        <div className="form-card">
          <h3>⚡ Energy & Ghar</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Energy Source</label>
              <select name="energy_source" value={form.energy_source} onChange={handle}>
                <option value="renewable">Renewable (Solar/Wind)</option>
                <option value="mixed">Mixed</option>
                <option value="natural gas">Natural Gas</option>
                <option value="coal">Coal / Grid</option>
              </select>
            </div>
            <div className="form-group">
              <label>AC/Heater Use</label>
              <select name="heating_cooling_usage" value={form.heating_cooling_usage} onChange={handle}>
                <option value="never">Kabhi nahi</option>
                <option value="rarely">Bahut kam</option>
                <option value="sometimes">Kabhi kabhi</option>
                <option value="often">Zyada tar</option>
                <option value="always">Hamesha</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 5: Lifestyle */}
        <div className="form-card">
          <h3>🌿 Lifestyle</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Recycling Karte Ho?</label>
              <select name="recycles" value={form.recycles} onChange={handle}>
                <option value="never">Kabhi nahi</option>
                <option value="rarely">Bahut kam</option>
                <option value="sometimes">Kabhi kabhi</option>
                <option value="often">Zyada tar</option>
                <option value="always">Hamesha</option>
              </select>
            </div>
            <div className="form-group">
              <label>Social Activity</label>
              <select name="social_activity" value={form.social_activity} onChange={handle}>
                <option value="rarely">Bahut kam</option>
                <option value="sometimes">Kabhi kabhi</option>
                <option value="often">Zyada tar</option>
                <option value="always">Hamesha</option>
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Naye Kapde Per Month (items)</label>
              <input
                type="number" name="new_clothes_monthly" min="0" max="50"
                value={form.new_clothes_monthly} onChange={handle}
              />
            </div>
            <div className="form-group">
              <label>Internet Use Daily (hours)</label>
              <input
                type="number" name="internet_hours_daily" min="0" max="24" step="0.5"
                value={form.internet_hours_daily} onChange={handle}
              />
            </div>
          </div>
        </div>

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? '🔄 AI Calculate kar raha hai...' : '🌱 Calculate My Carbon Footprint'}
        </button>

      </form>
    </div>
  );
}

export default Dashboard;