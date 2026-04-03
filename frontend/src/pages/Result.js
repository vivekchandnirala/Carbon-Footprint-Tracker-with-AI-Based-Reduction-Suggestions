import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import RecommendationCard from '../components/RecommendationCard';

function Result() {
  const location = useLocation();
  const navigate  = useNavigate();
  const [barWidth, setBarWidth] = useState(0);

  const result   = location.state?.result;
  const formData = location.state?.formData;

  useEffect(() => {
    if (!result) { navigate('/dashboard'); return; }
    // Animate bar after mount
    const t = setTimeout(() => {
      const pct = Math.min((result.predicted_co2_kg_year / 15000) * 100, 100);
      setBarWidth(pct);
    }, 200);
    return () => clearTimeout(t);
  }, [result, navigate]);

  if (!result) return null;

  const co2     = Math.round(result.predicted_co2_kg_year);
  const level   = result.level;
  const avg     = result.india_average_kg;
  const recs    = result.recommendations;
  const diff    = co2 - avg;
  const diffPct = Math.abs(Math.round((diff / avg) * 100));

  // Gauge chart data (max = 15000 kg for scale)
  const gaugeData = [{ value: Math.min(co2, 15000), fill: level === 'Low' ? '#16a34a' : level === 'Medium' ? '#ca8a04' : '#dc2626' }];

  return (
    <div className="result-container">

      {/* ── Score Card ── */}
      <div className="score-card">
        <div className="score-label">Tera Annual Carbon Footprint</div>

        {/* Gauge */}
        <div style={{ height: 200 }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart
              cx="50%" cy="85%" innerRadius="60%" outerRadius="100%"
              startAngle={180} endAngle={0}
              data={gaugeData}
            >
              <PolarAngleAxis type="number" domain={[0, 15000]} tick={false} />
              <RadialBar dataKey="value" cornerRadius={8} background={{ fill: '#e5e7eb' }} />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>

        <div className={`score-number score-${level}`}>
          {co2.toLocaleString('en-IN')}
        </div>
        <div className="score-unit">kg CO₂ / year</div>

        <div className={`level-badge level-${level}`}>
          {level === 'Low' ? '🟢' : level === 'Medium' ? '🟡' : '🔴'} {level} Footprint
        </div>

        {/* Compare with India average */}
        <div className="compare-bar-wrap">
          <p>
            India average ({avg.toLocaleString('en-IN')} kg) se{' '}
            <strong style={{ color: diff > 0 ? '#dc2626' : '#16a34a' }}>
              {diffPct}% {diff > 0 ? 'zyada ❌' : 'kam ✅'}
            </strong>
          </p>
          <div className="bar-track">
            <div
              className={`bar-fill ${level}`}
              style={{ width: `${barWidth}%` }}
            />
          </div>
          <p style={{ fontSize: 11, color: '#999', marginTop: 4 }}>
            Scale: 0 — 15,000 kg/year
          </p>
        </div>

        {/* Quick stats */}
        <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 16, flexWrap: 'wrap' }}>
          {[
            { label: 'Daily', value: `${Math.round(co2/365)} kg` },
            { label: 'Monthly', value: `${Math.round(co2/12)} kg` },
            { label: 'India Avg', value: `${avg} kg` },
          ].map(s => (
            <div key={s.label} style={{
              background: '#f0fdf4', borderRadius: 12, padding: '12px 20px', textAlign: 'center'
            }}>
              <div style={{ fontSize: 18, fontWeight: 800, color: '#1b4332' }}>{s.value}</div>
              <div style={{ fontSize: 11, color: '#666', marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Recommendations ── */}
      <div className="recs-section">
        <h2>💡 Personalized Suggestions ({recs.length})</h2>
        {recs.map((rec, i) => (
          <RecommendationCard key={i} rec={rec} />
        ))}
      </div>

      {/* ── Total potential saving ── */}
      {(() => {
        const totalSaving = recs.reduce((sum, r) => sum + (r.impact_kg || 0), 0);
        return totalSaving > 0 ? (
          <div style={{
            background: 'linear-gradient(135deg, #1b4332, #2d6a4f)',
            color: '#fff', borderRadius: 16, padding: '24px 28px',
            marginTop: 24, textAlign: 'center'
          }}>
            <div style={{ fontSize: 13, opacity: 0.8, letterSpacing: 1 }}>AGAR SAB TIPS FOLLOW KARO</div>
            <div style={{ fontSize: 42, fontWeight: 800, margin: '8px 0' }}>
              ~{totalSaving.toLocaleString('en-IN')} kg
            </div>
            <div style={{ fontSize: 14, opacity: 0.9 }}>CO₂ per year bacha sakte ho 🌱</div>
          </div>
        ) : null;
      })()}

      {/* ── Back button ── */}
      <div style={{ textAlign: 'center' }}>
        <button className="btn-back" onClick={() => navigate('/dashboard')}>
          ← Dobara Calculate Karo
        </button>
      </div>
    </div>
  );
}

export default Result;