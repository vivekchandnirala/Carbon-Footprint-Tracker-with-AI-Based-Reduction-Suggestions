import React from 'react';

const categoryIcons = {
  Transport : '🚗',
  Food      : '🥗',
  Energy    : '⚡',
  Waste     : '♻️',
  Lifestyle : '👕',
  Overall   : '🌍',
  General   : '🌿',
};

function RecommendationCard({ rec }) {
  return (
    <div className={`rec-card ${rec.priority}`}>
      <div className="rec-icon">
        {categoryIcons[rec.category] || '💡'}
      </div>
      <div className="rec-body">
        <div className="rec-category">
          {rec.category}
          <span className={`priority-badge priority-${rec.priority}`}>
            {rec.priority}
          </span>
        </div>
        <div className="rec-tip">{rec.tip}</div>
        {rec.impact_kg > 0 && (
          <div className="rec-impact">
            💚 ~{rec.impact_kg} kg CO₂ bacha sakte ho/year
          </div>
        )}
      </div>
    </div>
  );
}

export default RecommendationCard;