"""
========================================================================
BEHAVIOR TRACKING DASHBOARD - REACT COMPONENT TEMPLATE
========================================================================
Ready-to-use React component for behavior visualization and tracking
"""

const BehaviorTrackingDashboard = `
import React, { useState, useEffect } from 'react';
import './BehaviorDashboard.css';

export default function BehaviorDashboard({ childId, token }) {
  const [psycheProfile, setPsycheProfile] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [patterns, setPatterns] = useState(null);
  const [riskReport, setRiskReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    fetchAllData();
  }, [childId]);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const [profile, recs, pat, risk] = await Promise.all([
        fetch(\`/behavior/\${childId}/psyche-profile\`, {
          headers: { 'Authorization': \`Bearer \${token}\` }
        }).then(r => r.json()),
        fetch(\`/behavior/\${childId}/recommendations\`, {
          headers: { 'Authorization': \`Bearer \${token}\` }
        }).then(r => r.json()),
        fetch(\`/behavior/\${childId}/behavior-patterns\`, {
          headers: { 'Authorization': \`Bearer \${token}\` }
        }).then(r => r.json()),
        fetch(\`/behavior/\${childId}/risk-report\`, {
          headers: { 'Authorization': \`Bearer \${token}\` }
        }).then(r => r.json())
      ]);
      
      setPsycheProfile(profile);
      setRecommendations(recs);
      setPatterns(pat);
      setRiskReport(risk);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setLoading(false);
  };

  if (loading) return <div className="loading">Analyzing behavior patterns...</div>;
  if (!psycheProfile || psycheProfile.status !== 'success') {
    return <div className="insufficient-data">Need at least 3 days of data</div>;
  }

  return (
    <div className="behavior-dashboard">
      <div className="dashboard-header">
        <h1>🧠 Behavior & Psyche Analysis</h1>
        <button onClick={fetchAllData} className="refresh-btn">↻ Refresh Analysis</button>
      </div>

      <div className="profile-overview">
        <div className="profile-card">
          <div className="profile-emoji">{psycheProfile.profile_emoji}</div>
          <div className="profile-info">
            <h2>{psycheProfile.profile_name}</h2>
            <p className="confidence">Confidence: {psycheProfile.intervention_confidence}</p>
            <p className="description">{psycheProfile.profile_description}</p>
          </div>
        </div>

        <div className="risk-card">
          <h3>⚠️ Risk Assessment</h3>
          <div className={\\`risk-level risk-\\${psycheProfile.risk_assessment.risk_level}\\`}>
            {psycheProfile.risk_assessment.risk_level.toUpperCase()}
          </div>
          <p className="risk-score">Risk Score: {psycheProfile.risk_assessment.risk_assessment.risk_score.toFixed(0)}/100</p>
          <p className="trend">Trend: {psycheProfile.risk_assessment.trend}</p>
        </div>
      </div>

      <div className="tabs">
        <button className={\\`tab \\${activeTab === 'profile' ? 'active' : ''}\\`} 
                onClick={() => setActiveTab('profile')}>Profile</button>
        <button className={\\`tab \\${activeTab === 'dimensions' ? 'active' : ''}\\`} 
                onClick={() => setActiveTab('dimensions')}>Dimensions</button>
        <button className={\\`tab \\${activeTab === 'recommendations' ? 'active' : ''}\\`} 
                onClick={() => setActiveTab('recommendations')}>Recommendations</button>
        <button className={\\`tab \\${activeTab === 'patterns' ? 'active' : ''}\\`} 
                onClick={() => setActiveTab('patterns')}>Patterns</button>
      </div>

      <div className="tab-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <h3>Profile Details</h3>
            <div className="profile-grid">
              <div className="strength-box">
                <h4>✨ Strengths</h4>
                <ul>
                  {psycheProfile.strengths.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <div className="growth-box">
                <h4>🎯 Growth Areas</h4>
                <ul>
                  {psycheProfile.growth_areas.map((g, i) => <li key={i}>{g}</li>)}
                </ul>
              </div>
            </div>
            <div className="parenting-box">
              <h4>🎓 Recommended Parenting Style</h4>
              <p><strong>{psycheProfile.parenting_style}</strong></p>
              <ul>
                {psycheProfile.key_principles.map((p, i) => <li key={i}>{p}</li>)}
              </ul>
            </div>
          </div>
        )}

        {activeTab === 'dimensions' && (
          <div className="dimensions-section">
            <h3>Behavioral Dimensions</h3>
            <div className="dimensions-grid">
              {Object.entries(psycheProfile.dimensions).map(([name, data]) => (
                <div key={name} className="dimension-card">
                  <h4>{name.replace(/_/g, ' ').toUpperCase()}</h4>
                  <div className="dimension-bar">
                    <div className="bar-fill" style={{width: \\`\${data.score}%\\`}}></div>
                  </div>
                  <p className="score">{data.score.toFixed(0)}/100</p>
                  <p className="level">({data.level})</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="recommendations-section">
            <h3>Personalized Recommendations</h3>
            
            <div className="recommendation-block">
              <h4>🚀 Immediate Actions (Next 24-48 hours)</h4>
              <ul>
                {recommendations.immediate_actions.map((action, i) => (
                  <li key={i}>{action}</li>
                ))}
              </ul>
            </div>

            <div className="recommendation-block">
              <h4>📋 Weekly Strategies</h4>
              <ul>
                {recommendations.weekly_strategies.map((strategy, i) => (
                  <li key={i}>{strategy}</li>
                ))}
              </ul>
            </div>

            <div className="recommendation-block">
              <h4>🎯 Long-Term Goals (3-6 months)</h4>
              <ul>
                {recommendations.long_term_goals.map((goal, i) => (
                  <li key={i}>{goal}</li>
                ))}
              </ul>
            </div>

            <div className="recommendation-block success">
              <h4>✅ Success Indicators</h4>
              <ul>
                {recommendations.success_indicators.map((indicator, i) => (
                  <li key={i}>{indicator}</li>
                ))}
              </ul>
            </div>

            {recommendations.professional_resources.length > 0 && (
              <div className="recommendation-block warning">
                <h4>📞 Professional Resources</h4>
                <ul>
                  {recommendations.professional_resources.map((resource, i) => (
                    <li key={i}>{resource}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'patterns' && patterns && (
          <div className="patterns-section">
            <h3>Behavioral Patterns</h3>
            
            <div className="pattern-grid">
              <div className="pattern-card">
                <h4>😊 Emotional Patterns</h4>
                <p>Average Mood: {patterns.patterns.emotional.average_mood.toFixed(1)}/5</p>
                <p>Consistency: {patterns.patterns.emotional.mood_consistency.toFixed(1)}</p>
                <p>Trend: {patterns.patterns.emotional.mood_trend}</p>
                <p>Volatility: {patterns.patterns.emotional.volatility_score.toFixed(2)}</p>
              </div>

              <div className="pattern-card">
                <h4>⚡ Impulse Control</h4>
                <p>Avg Tantrums: {patterns.patterns.impulse_control.average_tantrums.toFixed(1)}/day</p>
                <p>Frequency: {(patterns.patterns.impulse_control.tantrum_frequency * 100).toFixed(0)}% of days</p>
                <p>Escalation: {patterns.patterns.impulse_control.escalation_trend.toFixed(2)}</p>
              </div>

              <div className="pattern-card">
                <h4>😴 Sleep Patterns</h4>
                <p>Average: {patterns.patterns.sleep.average_hours.toFixed(1)} hrs/night</p>
                <p>Consistency: {(patterns.patterns.sleep.consistency * 100).toFixed(0)}%</p>
                <p>Insufficient: {patterns.patterns.sleep.insufficient_nights} nights</p>
              </div>

              <div className="pattern-card">
                <h4>🤝 Social Engagement</h4>
                <p>Level: {patterns.patterns.social.engagement_level}</p>
                <p>Score: {patterns.patterns.social.average_score.toFixed(1)}/5</p>
              </div>
            </div>

            <div className="stability-score">
              <h4>Overall Stability Score</h4>
              <div className="large-bar">
                <div className="bar-fill" style={{width: \\`\${patterns.patterns.overall_stability}%\\`}}></div>
              </div>
              <p>{patterns.patterns.overall_stability.toFixed(0)}/100</p>
            </div>
          </div>
        )}
      </div>

      {riskReport && riskReport.status === 'success' && riskReport.concerns.length > 0 && (
        <div className="risk-details">
          <h3>⚠️ Areas of Concern</h3>
          <ul>
            {riskReport.concerns.map((concern, i) => (
              <li key={i}>{concern}</li>
            ))}
          </ul>
          {riskReport.professional_evaluation_recommended && (
            <div className="alert">
              🚨 Professional evaluation recommended. Please contact a child psychologist or behavioral specialist.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
`;

// CSS Styles
const BehaviorDashboardCSS = `
.behavior-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 3px solid #667eea;
  padding-bottom: 15px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.refresh-btn {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: #5568d3;
  transform: scale(1.05);
}

.profile-overview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.profile-card, .risk-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 5px solid #667eea;
}

.profile-emoji {
  font-size: 48px;
  margin-bottom: 10px;
}

.profile-info h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 20px;
}

.confidence {
  color: #667eea;
  font-weight: bold;
  margin: 5px 0;
}

.description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.risk-card h3 {
  margin-top: 0;
  color: #333;
}

.risk-level {
  font-size: 18px;
  font-weight: bold;
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
  text-align: center;
}

.risk-level.risk-low {
  background: #e8f5e9;
  color: #2e7d32;
}

.risk-level.risk-medium {
  background: #fff3e0;
  color: #e65100;
}

.risk-level.risk-high {
  background: #ffebee;
  color: #c62828;
}

.risk-score, .trend {
  color: #666;
  margin: 8px 0;
  font-size: 14px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.tab {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #999;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab:hover {
  color: #667eea;
}

.tab-content {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.strength-box, .growth-box, .parenting-box {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.strength-box {
  border-left-color: #4caf50;
}

.growth-box {
  border-left-color: #ff9800;
}

.parenting-box {
  grid-column: 1 / -1;
  border-left-color: #2196f3;
}

.strength-box h4, .growth-box h4, .parenting-box h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.strength-box ul, .growth-box ul, .parenting-box ul {
  margin: 0;
  padding-left: 20px;
}

.strength-box li, .growth-box li, .parenting-box li {
  margin: 8px 0;
  color: #666;
}

.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.dimension-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.dimension-card h4 {
  margin: 0 0 10px 0;
  font-size: 12px;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dimension-bar {
  width: 100%;
  height: 8px;
  background: #ddd;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}

.dimension-card .score {
  font-weight: bold;
  color: #667eea;
  margin: 5px 0;
}

.dimension-card .level {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.recommendation-block {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.recommendation-block.success {
  border-left-color: #4caf50;
}

.recommendation-block.warning {
  border-left-color: #ff9800;
}

.recommendation-block h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
}

.recommendation-block ul {
  margin: 0;
  padding-left: 20px;
}

.recommendation-block li {
  margin: 8px 0;
  color: #666;
  line-height: 1.5;
}

.pattern-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.pattern-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.pattern-card h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #333;
}

.pattern-card p {
  margin: 8px 0;
  color: #666;
  font-size: 13px;
}

.stability-score {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stability-score h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.large-bar {
  width: 100%;
  height: 20px;
  background: #ddd;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.stability-score p {
  text-align: center;
  font-weight: bold;
  color: #667eea;
  margin: 0;
}

.risk-details {
  margin-top: 30px;
  padding: 20px;
  background: #fff3cd;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
}

.risk-details h3 {
  margin-top: 0;
  color: #333;
}

.risk-details ul {
  margin: 10px 0;
  padding-left: 20px;
}

.risk-details li {
  margin: 8px 0;
  color: #333;
}

.alert {
  background: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 5px;
  margin-top: 15px;
  font-weight: bold;
}

.loading, .insufficient-data {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #666;
}

@media (max-width: 768px) {
  .profile-overview {
    grid-template-columns: 1fr;
  }
  
  .profile-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 15px;
  }
}
`;

export { BehaviorTrackingDashboard, BehaviorDashboardCSS };
`;

console.log("✅ React component template created!");
console.log("\nTo use in your React app:");
console.log("1. Copy the BehaviorTrackingDashboard component");
console.log("2. Copy the BehaviorDashboardCSS styles to BehaviorDashboard.css");
console.log("3. Import and use: <BehaviorDashboard childId={123} token={token} />");
