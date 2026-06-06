# 📊 Behavior Logs & Pattern Prediction Guide

## 🎯 Where Everything Is

### 1. **BEHAVIOR LOGS** - Where They're Stored
- **Database Table:** `behavior_logs` in MySQL (`upchild_db`)
- **Columns:** `child_id`, `mood`, `focus`, `social`, `tantrums`, `sleep_hours`, `notes`, `log_date`, `ai_risk_level`, `ai_cluster`, `ai_recommendations`
- **How Logs Are Created:**
  - User fills form in Behavior tab → BehaviorLogger.js (lines 1-311)
  - POST to `/behavior/<child_id>/log` endpoint (flask_app.py, lines 669-751)
  - Auto-saves in database + triggers AI analysis

### 2. **PATTERN PREDICTION (AI Insights)** - Where It Happens
- **AI Engine:** `behavior_ai_model.py` (~1,200 lines)
  - 6 Psyche Profiles: Resilient, Anxious, Aggressive, Withdrawn, Hyperactive, Balanced
  - 20+ Behavioral Features analyzed
  - ML-based Risk Assessment (scikit-learn)
  - Pattern Detection & Recommendations
  
- **AI Analysis Trigger:** 
  - Runs after each behavior log (flask_app.py, lines 727-735)
  - Function: `generate_ai_insights()` (flask_app.py, lines 830+)
  - Also runs on-demand via `/behavior/<child_id>/insights` endpoint

### 3. **FETCHING LOGS & INSIGHTS** - API Endpoints

#### Get AI Insights & Recent Logs
```
GET /behavior/<child_id>/insights
Headers: Authorization: Bearer <token>

Response includes:
{
  "risk_level": "HIGH" | "MEDIUM" | "LOW" | "NO_DATA",
  "risk_emoji": "🔴" | "🟡" | "🟢" | "⏳",
  "behavior_type": "Anxious" | "Resilient" | etc,
  "recommendations": ["Recommendation 1", "Recommendation 2", ...],
  "last_updated": "2026-02-06 10:30:00",
  "recent_logs": [
    {
      "date": "2026-02-06",
      "mood": 4,
      "focus": 3,
      "social": 5,
      "tantrums": 0,
      "sleep": 8
    }
  ]
}
```

### 4. **FRONTEND DISPLAY** - Where Logs/Insights SHOULD Appear

#### Currently Implemented:
- ✅ BehaviorLogger form in "Behavior" tab (upchild-frontend/upchild-frontend/src/App.js, lines 1920-1932)
- ✅ Fetches insights after logging (line 1925-1926)
- ✅ State: `behaviorInsights` (line 52)

#### Missing / Not Displayed:
- ❌ **No UI to show recent behavior logs**
- ❌ **No UI to show risk level/pattern prediction**
- ❌ **No AI recommendations display**
- ❌ **No charts/graphs of behavior trends**

---

## 🚀 To See Your Logs & Predictions

### Option 1: Check Database Directly
```bash
# Login to MySQL
mysql -u upchild_3 -p vaibhav123 -h 127.0.0.1

# View all behavior logs
SELECT * FROM upchild_db.behavior_logs;

# View logs for specific child (replace 1 with child_id)
SELECT * FROM upchild_db.behavior_logs WHERE child_id = 1;

# View AI predictions
SELECT 
  log_date, 
  ai_risk_level, 
  ai_cluster, 
  ai_recommendations 
FROM upchild_db.behavior_logs 
WHERE child_id = 1 
ORDER BY log_date DESC;
```

### Option 2: Test API Directly (via terminal)
```bash
curl -X GET "http://localhost:5000/behavior/1/insights" \
  -H "Authorization: Bearer <your_token>"
```

### Option 3: Add UI Dashboard (Next Step)
Need to display the `behaviorInsights` data in the Behavior tab:
- Recent behavior logs table
- Risk level indicator with emoji
- Behavior pattern/type display
- AI recommendations list
- 7-day trend chart

---

## 📈 What Pattern Prediction Shows

**Example Output:**
```
Risk Level: HIGH 🔴
Behavior Type: Anxious
Pattern Detected: High mood swings, poor focus, sleep disruption
Psyche Profile: Anxious personality type
Recommendations:
- Create structured routine with clear schedules
- Practice relaxation techniques (deep breathing)
- Limit screen time 1 hour before bed
- Schedule daily 15-minute focused activities
- Consult child psychologist if symptoms persist
Risk Factors: Inconsistent sleep, high tantrums (3-4/day), low focus
```

---

## 🔧 Implementation Status

| Feature | Status | Location |
|---------|--------|----------|
| Log Storage | ✅ Complete | behavior_logs table |
| AI Prediction Engine | ✅ Complete | behavior_ai_model.py |
| Backend API | ✅ Complete | /behavior/<id>/log, /behavior/<id>/insights |
| Frontend Logging Form | ✅ Complete | BehaviorLogger.js |
| Fetch Insights | ✅ Complete | App.js line 276 |
| Display Logs | ❌ TODO | App.js Behavior Tab |
| Display Predictions | ❌ TODO | App.js Behavior Tab |
| Recommendations Display | ❌ TODO | App.js Behavior Tab |
| Trend Charts | ❌ TODO | New component needed |

---

## 💡 Next Steps

1. **Quick Fix (5 min):** Add simple UI to show insights in Behavior tab
2. **Medium Fix (20 min):** Create dashboard component with logs table + risk indicator
3. **Full Enhancement (1 hour):** Add charts, trend analysis, export functionality

Would you like me to implement the UI to display logs and predictions?
