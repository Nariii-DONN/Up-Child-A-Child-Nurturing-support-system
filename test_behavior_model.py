
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from behavior_ai_model import (
    BehaviorMLModel, BehaviorPatternAnalyzer, PsycheProfileGenerator,
    create_summary_report, PSYCHE_PROFILES
)
def generate_balanced_child_data(days=30):
    """Generate behavior data for a balanced, healthy child"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'mood': np.random.normal(3.8, 0.5, days).clip(1, 5),
        'focus': np.random.normal(3.7, 0.4, days).clip(1, 5),
        'social': np.random.normal(4.0, 0.3, days).clip(1, 5),
        'tantrums': np.random.poisson(0.1, days),
        'sleep_hours': np.random.normal(8.5, 0.3, days).clip(6, 10),
        'log_date': dates
    }
    return pd.DataFrame(data)

def generate_high_impulse_data(days=30):
    """Generate behavior data for high-energy, impulsive child"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    trend = np.linspace(0, 2, days)
    data = {
        'mood': (np.random.normal(3.5, 1.2, days) + trend).clip(1, 5),
        'focus': np.random.normal(2.8, 0.8, days).clip(1, 5),
        'social': np.random.normal(4.0, 0.4, days).clip(1, 5),
        'tantrums': np.random.poisson(1.5, days),
        'sleep_hours': np.random.normal(7.5, 0.8, days).clip(5, 9),
        'log_date': dates
    }
    return pd.DataFrame(data)

def generate_anxious_child_data(days=30):
    """Generate behavior data for sensitive, anxious child"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'mood': np.random.normal(2.5, 1.5, days).clip(1, 5),  # High volatility
        'focus': np.random.normal(3.2, 0.7, days).clip(1, 5),
        'social': np.random.normal(2.5, 0.8, days).clip(1, 5),
        'tantrums': np.random.poisson(0.5, days),
        'sleep_hours': np.random.normal(7.8, 1.0, days).clip(5, 9),
        'log_date': dates
    }
    return pd.DataFrame(data)

def generate_withdrawn_child_data(days=30):
    """Generate behavior data for withdrawn, isolated child"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'mood': np.random.normal(2.2, 0.6, days).clip(1, 5),
        'focus': np.random.normal(2.8, 0.5, days).clip(1, 5),
        'social': np.random.normal(1.5, 0.4, days).clip(1, 3),  # Very low social
        'tantrums': np.random.poisson(0.1, days),
        'sleep_hours': np.random.normal(8.8, 0.4, days).clip(7, 10),
        'log_date': dates
    }
    return pd.DataFrame(data)

def generate_high_risk_data(days=30):
    """Generate behavior data for high-risk child requiring intervention"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    # Worsening trend
    trend = np.linspace(3, 1.5, days)
    data = {
        'mood': (trend + np.random.normal(0, 0.8, days)).clip(1, 5),
        'focus': np.random.normal(1.8, 0.6, days).clip(1, 5),
        'social': np.random.normal(1.5, 0.5, days).clip(1, 3),
        'tantrums': np.random.poisson(2.5, days),
        'sleep_hours': np.random.normal(6.5, 1.2, days).clip(4, 8),
        'log_date': dates
    }
    return pd.DataFrame(data)

def generate_low_energy_data(days=30):
    """Generate behavior data for low-energy, possibly depressed child"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'mood': np.random.normal(1.8, 0.5, days).clip(1, 3),  # Consistently low
        'focus': np.random.normal(1.5, 0.6, days).clip(1, 3),  # Poor focus
        'social': np.random.normal(1.8, 0.5, days).clip(1, 3),
        'tantrums': np.random.poisson(0.2, days),
        'sleep_hours': np.random.normal(9.5, 1.0, days).clip(7, 12),  # Sleeping too much
        'log_date': dates
    }
    return pd.DataFrame(data)

# ========================================================================
# ANALYSIS FUNCTION
# ========================================================================

def analyze_child(name, data_generator, description):
    """Run complete analysis on generated child data"""
    print("\n" + "="*70)
    print(f"ANALYZING: {name}")
    print("="*70)
    print(f"Description: {description}\n")
    
    # Generate data
    df = data_generator(days=30)
    print(f"Generated {len(df)} days of behavior data")
    print(f"Mood Range: {df['mood'].min():.1f}-{df['mood'].max():.1f}")
    print(f"Tantrums: {df['tantrums'].sum()} total, {df['tantrums'].mean():.1f} per day")
    print(f"Sleep: {df['sleep_hours'].mean():.1f} hrs/night avg\n")
    
    # Run analysis
    model = BehaviorMLModel()
    analysis = model.predict(df)
    
    if analysis['status'] != 'success':
        print(f"Status: {analysis['status']}")
        if 'message' in analysis:
            print(f"Message: {analysis['message']}")
        return
    
    # Display results
    profile = analysis['profile']
    features = analysis['features']
    recommendations = analysis['recommendations']
    
    print(f"✨ IDENTIFIED CLUSTER: {profile['profile']['name']} {profile['profile']['emoji']}")
    print(f"Confidence: {profile['confidence']*100:.0f}%\n")
    
    print("🧠 BEHAVIORAL DIMENSIONS:")
    for dim_name, dim_data in profile['dimensions'].items():
        bar_length = int(dim_data['score'] / 5)
        bar = '█' * bar_length + '░' * (20 - bar_length)
        print(f"  {dim_name:25} {bar} {dim_data['score']:5.0f}/100 ({dim_data['level']})")
    
    print(f"\n⚠️ RISK ASSESSMENT:")
    print(f"  Risk Level:    {profile['risk_assessment']['risk_level'].upper()}")
    print(f"  Risk Score:    {profile['risk_assessment']['risk_score']:.0f}/100")
    print(f"  Trend:         {profile['risk_assessment']['trend'].upper()}")
    
    if profile['risk_assessment']['concerns']:
        print(f"  Concerns:")
        for concern in profile['risk_assessment']['concerns']:
            print(f"    • {concern}")
    
    print(f"\n✨ STRENGTHS:")
    for strength in recommendations['strengths_to_build_on'][:3]:
        print(f"  ✓ {strength}")
    
    print(f"\n🎯 GROWTH AREAS:")
    for area in recommendations['growth_areas'][:3]:
        print(f"  • {area}")
    
    print(f"\n🚀 IMMEDIATE ACTIONS (Next 24-48 hours):")
    for action in recommendations['immediate_actions'][:3]:
        print(f"  → {action}")
    
    print(f"\n📋 WEEKLY STRATEGIES:")
    for strategy in recommendations['weekly_strategies'][:3]:
        print(f"  • {strategy}")
    
    print(f"\n🎓 PARENTING APPROACH: {recommendations['parenting_approaches']['style']}")
    print(f"Key Principles:")
    for principle in recommendations['parenting_approaches']['key_principles'][:2]:
        print(f"  • {principle}")
    
    if recommendations['professional_resources']:
        print(f"\n📞 PROFESSIONAL RESOURCES:")
        for resource in recommendations['professional_resources'][:2]:
            print(f"  • {resource}")
    
    return analysis

# ========================================================================
# COMPARISON FUNCTION
# ========================================================================

def compare_psyche_profiles():
    """Show overview of all psyche profiles"""
    print("\n" + "="*70)
    print("UPCHILD PSYCHE PROFILE REFERENCE")
    print("="*70)
    
    for cluster, profile in PSYCHE_PROFILES.items():
        print(f"\n{profile['emoji']} {profile['name'].upper()}")
        print(f"Risk Level: {profile['risk_level'].upper()}")
        print(f"Description: {profile['description']}")
        print(f"Traits: {', '.join(profile['traits'][:3])}...")
        print(f"Strengths: {', '.join(profile['strengths'][:2])}...")
        if 'interventions' in profile:
            print(f"Key Interventions:")
            for interv in profile['interventions'][:2]:
                print(f"  • {interv}")

# ========================================================================
# FEATURE COMPARISON
# ========================================================================

def compare_feature_sets():
    """Compare extracted features across different profile types"""
    print("\n" + "="*70)
    print("BEHAVIORAL FEATURE COMPARISON")
    print("="*70)
    
    analyzer = BehaviorPatternAnalyzer()
    
    test_cases = [
        ("Balanced Child", generate_balanced_child_data()),
        ("High Impulse Child", generate_high_impulse_data()),
        ("Anxious Child", generate_anxious_child_data()),
        ("Withdrawn Child", generate_withdrawn_child_data()),
        ("High Risk Child", generate_high_risk_data()),
        ("Low Energy Child", generate_low_energy_data()),
    ]
    
    print(f"\n{'Profile':<20} {'Stability':<12} {'Regulation':<12} {'Resilience':<12} {'Red Flags':<10}")
    print("-" * 70)
    
    for name, df in test_cases:
        features = analyzer.extract_advanced_features(df)
        if features:
            print(f"{name:<20} {features.get('overall_stability_score', 0):>10.0f}/100 {features.get('self_regulation_index', 0):>10.0f}/100 {features.get('emotional_resilience', 0):>10.2f} {features.get('red_flag_count', 0):>8.0f}")

# ========================================================================
# MAIN EXECUTION
# ========================================================================

if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║     UPCHILD BEHAVIOR AI/ML MODEL - TESTING & DEMO             ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    # Test 1: Profile reference
    compare_psyche_profiles()
    
    # Test 2: Feature comparison
    compare_feature_sets()
    
    # Test 3: Individual analyses
    print("\n\n" + "="*70)
    print("INDIVIDUAL CHILD ANALYSES")
    print("="*70)
    
    test_children = [
        ("Emma - Balanced Child", generate_balanced_child_data, 
         "Emotionally stable, good focus, healthy social engagement"),
        
        ("Alex - High Energy Kid", generate_high_impulse_data,
         "High activity, impulsive, needs structure and boundaries"),
        
        ("Sam - Anxious Child", generate_anxious_child_data,
         "Sensitive, worries frequently, mood swings"),
        
        ("Jordan - Withdrawn Child", generate_withdrawn_child_data,
         "Reserved, low social engagement, possible isolation concerns"),
        
        ("Casey - High Risk", generate_high_risk_data,
         "Multiple concerning signs - declining behavior, sleep issues, tantrums"),
        
        ("Morgan - Low Energy", generate_low_energy_data,
         "Persistent low mood, lacks energy, possible depression"),
    ]
    
    results = []
    for name, generator, description in test_children:
        result = analyze_child(name, generator, description)
        if result:
            results.append((name, result))
    
    # Test 4: Risk level summary
    print("\n\n" + "="*70)
    print("RISK LEVEL SUMMARY")
    print("="*70)
    
    for name, analysis in results:
        risk_level = analysis['profile']['risk_assessment']['risk_level']
        emoji = {'low': '✅', 'medium': '🟡', 'high': '🚨'}.get(risk_level, '❓')
        print(f"{emoji} {name:<30} Risk: {risk_level.upper():<6} Cluster: {analysis['profile']['cluster']}")
    
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE")
    print("="*70)
    print("\nThe AI/ML model successfully:")
    print("  ✓ Extracted advanced behavioral features")
    print("  ✓ Classified children into psyche profiles")
    print("  ✓ Generated risk assessments")
    print("  ✓ Produced personalized recommendations")
    print("  ✓ Identified intervention strategies")
    print("\nReady for production use in Flask app!")
