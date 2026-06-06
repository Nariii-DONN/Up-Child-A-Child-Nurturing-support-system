# UpChild - Behavior Pattern & Psyche AI/ML Model

## Overview

The UpChild AI/ML system provides **advanced behavior pattern recognition and psyche profiling** to help parents and caregivers understand child development, detect early risk signs, and provide timely interventions to keep children on a positive path.

---

## 🧠 Core Features

### 1. **Psyche Profile Clustering**
Classifies children into 6 psychological profiles based on behavioral patterns:

| Cluster | Emoji | Risk Level | Description |
|---------|-------|-----------|-------------|
| **Balanced & Resilient** | ✅ | Low | Emotionally stable, good impulse control, positive social engagement |
| **High Energy / Impulsive** | ⚡ | Medium | High activity, quick reactions, needs structure and guidance |
| **Sensitive / Anxious** | 😰 | Medium | High sensitivity, worries, needs reassurance and calm environment |
| **Withdrawn / Reserved** | 😔 | High | Low social engagement, quiet, needs gentle encouragement |
| **Challenging / High-Risk** | 🚨 | High | Multiple concerning signs - tantrums, aggression, poor sleep |
| **Low Energy / Lethargic** | 😞 | High | Persistent low mood, lacks motivation, possible depression |

---

## 📊 Advanced Feature Extraction

The system extracts 20+ behavioral features:

### Emotional Metrics
- Average mood, mood consistency (std), mood range
- Mood trend (improving/declining)
- Mood volatility (day-to-day swings)

### Impulse Control
- Average tantrums per day
- Tantrum frequency ratio (% of days with tantrums)
- Tantrum escalation trend

### Sleep Patterns
- Average sleep hours
- Sleep consistency
- Insufficient sleep ratio
- Sleep quality score

### Social Engagement
- Average social interaction score
- Engagement level classification

### Composite Metrics
- **Overall Stability Score** (0-100)
- **Self-Regulation Index** (0-100)
- **Emotional Resilience Score** (0-1)

---

## 🎯 Behavioral Dimensions

Each child's profile includes 6 key dimensions scored 0-100:

### 1. **Emotional Stability**
How consistently the child maintains mood. Affected by:
- Mood consistency
- Emotional regulation
- Absence of severe mood swings

### 2. **Impulse Control**
Ability to manage reactions. Evaluated by:
- Tantrum frequency
- Behavioral spikes
- Frustration tolerance

### 3. **Social Engagement**
Quality of peer interactions and group participation:
- Group interaction comfort
- Peer relationship quality
- Social initiative

### 4. **Self-Regulation**
Ability to manage sleep, attention, and routines:
- Sleep pattern consistency
- Focus ability
- Routine adherence

### 5. **Cognitive Focus**
Attention span and task completion:
- Concentration ability
- Task persistence
- Learning readiness

### 6. **Emotional Resilience**
Ability to bounce back from difficulties:
- Recovery from low moods
- Stress management
- Problem-solving ability

---

## 🚨 Risk Assessment

### Red Flag Counting
The system identifies serious concern indicators:

| Red Flag | Threshold |
|----------|-----------|
| High tantrums | > 2 per day on average |
| Sleep deprivation | < 7 hours on 40%+ of days |
| Persistent low mood | < 2.5/5 average mood |
| Social withdrawal | < 2/5 average social score |
| Mood volatility | > 1.5 point swings daily |
| Focus problems | < 2/5 average focus |

**Score Calculation:**
- 0 red flags = Low risk ✅
- 1-2 red flags = Monitor closely 🟡
- 3-4 red flags = Medium-High risk ⚠️
- 4+ red flags = Professional evaluation recommended 🚨

### Trend Analysis
Tracks whether behavior is improving, stable, or declining based on:
- Recent mood changes
- Tantrum escalation
- Sleep improvement
- Focus maintenance

---

## 💡 Personalized Interventions

### Immediate Actions (24-48 hours)
**Example - High Impulse Child:**
- Establish wake/sleep consistency
- Schedule 20+ mins vigorous physical activity
- Use timers for transitions (5 min warnings)
- Set ONE clear daily rule

**Example - Anxious Child:**
- Create predictable routine with visual schedule
- Teach breathing exercise (4-count in, 6-count out)
- Use identical bedtime routine
- Identify specific worry triggers

### Weekly Strategies
Tailored to weak dimensions:
- Daily mood check-ins
- Impulse control games
- Structured peer interaction
- Sleep hygiene improvements

### Long-Term Goals (3-6 months)
- Maintain positive trajectory
- Build specific skills
- Strengthen relationships
- Develop resilience

---

## 📱 API Endpoints

### 1. Log Behavior
```
POST /behavior/<child_id>/log
Headers: Authorization: Bearer <token>
Body: {
  "mood": 1-5,
  "focus": 1-5,
  "social": 1-5,
  "tantrums": 0-5,
  "sleep_hours": float,
  "notes": "optional notes"
}
```

### 2. Get Psyche Profile
```
GET /behavior/<child_id>/psyche-profile
Returns: Complete profile with dimensions and risk assessment
```

### 3. Get Personalized Recommendations
```
GET /behavior/<child_id>/recommendations
Returns: Immediate actions, weekly strategies, long-term goals
```

### 4. Get Behavior Patterns
```
GET /behavior/<child_id>/behavior-patterns
Returns: Detailed pattern analysis across all dimensions
```

### 5. Get Risk Report
```
GET /behavior/<child_id>/risk-report
Returns: Comprehensive risk assessment and urgent recommendations
```

### 6. Get Insights
```
GET /behavior/<child_id>/insights
Returns: Quick overview of latest analysis
```

---

## 🔄 How It Works

### 1. **Data Collection**
Parents/caregivers log daily observations:
- Mood (1-5 scale)
- Focus ability (1-5)
- Social engagement (1-5)
- Tantrum/outburst count
- Sleep hours
- Optional notes

### 2. **Feature Extraction**
System analyzes last 30 days of data:
- Calculates 20+ behavioral features
- Identifies patterns and trends
- Measures consistency and volatility

### 3. **Profile Generation**
Multi-step classification:
- Evaluates against psyche profiles
- Scores 6 behavioral dimensions
- Calculates risk assessment
- Generates confidence score

### 4. **Recommendation Engine**
Generates personalized plan:
- Immediate crisis interventions (if needed)
- Weekly actionable strategies
- Long-term development goals
- Parenting approach recommendations
- Professional resources (if needed)

### 5. **Continuous Learning**
System improves as more data accumulates:
- More logs = higher confidence
- Pattern recognition strengthens
- Recommendations become more specific

---

## 🎓 Parenting Approaches

### High Energy / Impulsive
**Style:** Structured & Supportive
- Be calm and consistent—they mirror your energy
- Set clear consequences immediately
- Redirect before explosion
- Break down tasks into small steps

### Anxious / Sensitive
**Style:** Validating & Gradual
- Acknowledge fears without judgment
- Provide reassurance and predictability
- Use gradual exposure
- Celebrate small brave steps

### Withdrawn
**Style:** Patient & Inviting
- Never force social interaction
- Create low-pressure opportunities
- Find and build on interests
- Be present without expectations

### Challenging / High-Risk
**Style:** Firm & Compassionate
- Stay calm during outbursts
- Set clear, enforceable limits
- Underlying cause may be trauma
- Seek professional support

---

## ✅ Success Indicators

Know interventions are working by watching for:

**High Impulse Child:**
- Fewer tantrum episodes per week
- Can wait 5+ minutes without distress
- Listens better to instructions

**Anxious Child:**
- Attempts previously avoided activities
- Sleep improves, bedtime battles decrease
- Asks for help rather than withdrawing

**Withdrawn Child:**
- Initiates conversation/play more often
- Smiles or shows enjoyment
- Expresses interest in activities

**All Children:**
- More consistent positive mood
- Better sleep and energy
- Increased engagement
- Improved relationships

---

## 🚨 When to Seek Professional Help

### Green Flags (Monitor)
- 0-1 red flags present
- Stable or improving trend
- Child functioning well in school/activities

### Yellow Flags (Watch Carefully)
- 2-3 red flags
- Some concerning patterns
- Parents feeling overwhelmed

### Red Flags (Professional Evaluation Needed)
- 4+ red flags
- Declining trend despite interventions
- Behavior worsening over time
- Aggression or safety concerns
- Persistent depression or withdrawal

### Crisis Resources
- **988 Suicide & Crisis Lifeline** (US)
- Child psychiatrist referral
- Pediatric behavioral specialist
- Family therapy services
- Crisis assessment at local ER if safety concerned

---

## 📈 Data Privacy & Security

- All data encrypted in transit and at rest
- Only authorized parents/caregivers can view child's profile
- No data shared with third parties
- Compliant with HIPAA/FERPA standards
- Regular security audits

---

## 🔧 Technical Details

### ML Model Architecture

**Feature Extraction:**
- 20+ behavioral features extracted
- Data normalized to 0-1 scale
- Outliers handled gracefully

**Classification:**
- Rule-based psyche clustering
- Random Forest for confidence scoring
- Trend analysis using polynomial fit

**Recommendations:**
- Profile-matched intervention strategies
- Dimensionally-targeted action items
- Evidence-based parenting approaches

### Data Requirements
- Minimum: 3 days of data for basic analysis
- Optimal: 7+ days for pattern recognition
- Best: 30 days for trend identification

---

## 💾 Sample Report

```
╔════════════════════════════════════════════════════════════════╗
║              UPCHILD BEHAVIOR & PSYCHE ANALYSIS                ║
╚════════════════════════════════════════════════════════════════╝

📊 PSYCHE PROFILE: High Energy / Impulsive
⚡

Profile Description:
High activity level, quick emotional reactions, needs structure.

────────────────────────────────────────────────────────────────
🧠 BEHAVIORAL DIMENSIONS:

• Emotional Stability:    MODERATE (48/100)
• Impulse Control:        POOR (35/100)
• Social Engagement:      HIGH (78/100)
• Self-Regulation:        DEVELOPING (55/100)
• Cognitive Focus:        MODERATE (52/100)
• Emotional Resilience:   MODERATE (62/100)

────────────────────────────────────────────────────────────────
⚠️ RISK ASSESSMENT:

Risk Level: MEDIUM
Trend: STABLE

Concerns:
  • High frequency of tantrums/outbursts
  • Sleep deprivation may be impacting behavior

────────────────────────────────────────────────────────────────
✨ STRENGTHS TO BUILD ON:
  • enthusiastic
  • creative
  • spontaneous
  • action_oriented

🎯 GROWTH AREAS:
  • impulse control
  • planning ahead
  • following through

────────────────────────────────────────────────────────────────
🚀 IMMEDIATE ACTIONS (Next 24-48 hours):
  ⏰ Establish consistent wake/sleep times
  🏃 Schedule 20+ mins vigorous activity
  ⏱️ Use timers for transitions (5 min warning)
  🎯 Set ONE clear rule for today

────────────────────────────────────────────────────────────────
📋 WEEKLY STRATEGIES:
  Practice waiting games and impulse control activities
  Reward good behavior with attention, not things
  Implement consistent daily schedule
  Reduce screen time by 30 mins each day
  Structured routines reduce behavioral spikes

────────────────────────────────────────────────────────────────
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install pandas numpy scikit-learn
```

### 2. Initialize the Model
```python
from behavior_ai_model import BehaviorMLModel
ai_model = BehaviorMLModel()
```

### 3. Start Logging
Parents log daily observations through the app

### 4. Get Insights
After 3+ days: `GET /behavior/<child_id>/psyche-profile`

### 5. Apply Recommendations
Follow the personalized action plan

---

## 📞 Support

For questions or concerns about the analysis:
1. Review the detailed profile report
2. Consult recommended professional resources
3. Contact UpChild support team
4. Seek professional mental health evaluation if recommended

---

**Version:** 1.0
**Last Updated:** February 2026
**Status:** Active & Learning
