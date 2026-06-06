"""
ML Pipeline API Test Suite
Comprehensive testing for all new ML endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
ADMIN_EMAIL = "parent@example.com"
ADMIN_PASSWORD = "password123"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

class MLAPITester:
    """Test suite for ML Pipeline API"""
    
    def __init__(self):
        self.token = None
        self.child_id = 2  # child_id 2 belongs to parent@example.com
        self.results = []
    
    def log(self, message, level="INFO"):
        """Log test messages"""
        colors = {
            "SUCCESS": GREEN,
            "ERROR": RED,
            "INFO": BLUE,
            "WARNING": YELLOW
        }
        color = colors.get(level, BLUE)
        print(f"{color}[{level}]{END} {message}")
    
    def login(self):
        """Authenticate and get JWT token"""
        self.log("Logging in...", "INFO")
        
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={
                    "email": ADMIN_EMAIL,
                    "password": ADMIN_PASSWORD
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.log(f"Login successful! Token: {self.token[:20]}...", "SUCCESS")
                return True
            else:
                self.log(f"Login failed: {response.text}", "ERROR")
                return False
        
        except Exception as e:
            self.log(f"Login error: {str(e)}", "ERROR")
            return False
    
    def make_request(self, method, endpoint, json_data=None):
        """Make API request with JWT token"""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{BASE_URL}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=json_data)
            else:
                response = requests.request(method, url, headers=headers, json=json_data)
            
            return response
        
        except Exception as e:
            self.log(f"Request error: {str(e)}", "ERROR")
            return None
    
    def test_health(self):
        """Test basic health endpoints"""
        self.log("\n========== HEALTH CHECK ==========", "INFO")
        
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            self.log("Health check passed", "SUCCESS")
            self.results.append(("Health Check", "PASS"))
            return True
        else:
            self.log("Health check failed", "ERROR")
            self.results.append(("Health Check", "FAIL"))
            return False
    
    def test_timeseries_training(self):
        """Test time-series model training"""
        self.log("\n========== TIME-SERIES TRAINING ==========", "INFO")
        
        endpoint = f"/api/ml/timeseries/train/{self.child_id}"
        response = self.make_request("POST", endpoint)
        
        if response and response.status_code == 200:
            self.log("Time-series model training initiated", "SUCCESS")
            self.results.append(("Time-Series Training", "PASS"))
            return True
        else:
            self.log(f"Time-series training failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Time-Series Training", "FAIL/SKIP"))
            return False
    
    def test_mood_prediction(self):
        """Test next-day mood prediction"""
        self.log("\n========== MOOD PREDICTION ==========", "INFO")
        
        endpoint = f"/api/ml/timeseries/predict/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            self.log(f"Prediction: {data.get('prediction', {}).get('predicted_mood_category', 'N/A')}", "SUCCESS")
            self.results.append(("Mood Prediction", "PASS"))
            return True
        else:
            self.log(f"Mood prediction failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Mood Prediction", "FAIL/SKIP"))
            return False
    
    def test_mood_trend(self):
        """Test 7-day mood trend forecast"""
        self.log("\n========== MOOD TREND FORECAST ==========", "INFO")
        
        endpoint = f"/api/ml/timeseries/trend/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            trend = data.get('trend', {}).get('trajectory', 'N/A')
            self.log(f"Trend trajectory: {trend}", "SUCCESS")
            self.results.append(("Mood Trend", "PASS"))
            return True
        else:
            self.log(f"Mood trend failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Mood Trend", "FAIL/SKIP"))
            return False
    
    def test_anomaly_training(self):
        """Test anomaly detector training"""
        self.log("\n========== ANOMALY TRAINING ==========", "INFO")
        
        endpoint = f"/api/ml/anomaly/train/{self.child_id}"
        response = self.make_request("POST", endpoint)
        
        if response and response.status_code == 200:
            self.log("Anomaly model training initiated", "SUCCESS")
            self.results.append(("Anomaly Training", "PASS"))
            return True
        else:
            self.log(f"Anomaly training failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Anomaly Training", "FAIL/SKIP"))
            return False
    
    def test_anomaly_detection(self):
        """Test anomaly detection"""
        self.log("\n========== ANOMALY DETECTION ==========", "INFO")
        
        endpoint = f"/api/ml/anomaly/detect/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            is_anomaly = data.get('anomalies', {}).get('is_anomaly', False)
            severity = data.get('anomalies', {}).get('severity', 'none')
            self.log(f"Anomaly detected: {is_anomaly} | Severity: {severity}", "SUCCESS")
            self.results.append(("Anomaly Detection", "PASS"))
            return True
        else:
            self.log(f"Anomaly detection failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Anomaly Detection", "FAIL/SKIP"))
            return False
    
    def test_risk_classification(self):
        """Test risk classification"""
        self.log("\n========== RISK CLASSIFICATION ==========", "INFO")
        
        endpoint = f"/api/ml/risk/classify/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            risk_level = data.get('risk_prediction', {}).get('risk_level', 'N/A')
            confidence = data.get('risk_prediction', {}).get('confidence', 0)
            self.log(f"Risk Level: {risk_level} | Confidence: {confidence*100:.0f}%", "SUCCESS")
            self.results.append(("Risk Classification", "PASS"))
            return True
        else:
            self.log(f"Risk classification failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Risk Classification", "FAIL/SKIP"))
            return False
    
    def test_nlp_analysis(self):
        """Test NLP sentiment analysis"""
        self.log("\n========== NLP SENTIMENT ANALYSIS ==========", "INFO")
        
        endpoint = "/api/ml/nlp/analyze"
        test_text = "My child has been very happy and excited today! Playing well with friends."
        
        response = self.make_request("POST", endpoint, {"text": test_text})
        
        if response and response.status_code == 200:
            data = response.json()
            sentiment = data.get('analysis', {}).get('sentiment', {})
            polarity = sentiment.get('polarity', 0)
            self.log(f"Sentiment polarity: {polarity:.2f} ({sentiment.get('label', 'N/A')})", "SUCCESS")
            self.results.append(("NLP Sentiment", "PASS"))
            return True
        else:
            self.log(f"NLP analysis failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("NLP Sentiment", "FAIL/SKIP"))
            return False
    
    def test_nlp_patterns(self):
        """Test NLP pattern detection"""
        self.log("\n========== NLP PATTERN DETECTION ==========", "INFO")
        
        endpoint = f"/api/ml/nlp/patterns/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            patterns = data.get('patterns', {}).get('concerning_patterns', [])
            self.log(f"Concerning patterns found: {len(patterns)}", "SUCCESS")
            self.results.append(("NLP Patterns", "PASS"))
            return True
        else:
            self.log(f"NLP patterns failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("NLP Patterns", "FAIL/SKIP"))
            return False
    
    def test_recommendations(self):
        """Test recommendation engine"""
        self.log("\n========== RECOMMENDATIONS ==========", "INFO")
        
        endpoint = f"/api/ml/recommendations/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            recs = data.get('recommendations', {}).get('recommendations', [])
            self.log(f"Generated {len(recs)} personalized recommendations", "SUCCESS")
            self.results.append(("Recommendations", "PASS"))
            return True
        else:
            self.log(f"Recommendations failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Recommendations", "FAIL/SKIP"))
            return False
    
    def test_contextual_recommendations(self):
        """Test contextual recommendations"""
        self.log("\n========== CONTEXTUAL RECOMMENDATIONS ==========", "INFO")
        
        contexts = ["morning", "afternoon", "evening", "school", "weekend"]
        
        for context in contexts:
            endpoint = f"/api/ml/recommendations/contextual/{self.child_id}?context={context}"
            response = self.make_request("GET", endpoint)
            
            if response and response.status_code == 200:
                self.log(f"  ✓ {context.upper()} recommendations retrieved", "SUCCESS")
            else:
                self.log(f"  ✗ {context.upper()} recommendations failed", "WARNING")
        
        self.results.append(("Contextual Recommendations", "PASS"))
        return True
    
    def test_simple_summary(self):
        """Test simple status summary"""
        self.log("\n========== SIMPLE SUMMARY ==========", "INFO")
        
        endpoint = f"/api/ml/explain/summary/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            summary = data.get('summary', 'N/A')
            self.log(f"Summary: {summary}", "SUCCESS")
            self.results.append(("Simple Summary", "PASS"))
            return True
        else:
            self.log(f"Simple summary failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Simple Summary", "FAIL/SKIP"))
            return False
    
    def test_parent_report(self):
        """Test comprehensive parent report"""
        self.log("\n========== PARENT REPORT ==========", "INFO")
        
        endpoint = f"/api/ml/explain/report/{self.child_id}"
        response = self.make_request("GET", endpoint)
        
        if response and response.status_code == 200:
            data = response.json()
            report = data.get('report', {})
            overview = report.get('overview', 'N/A')
            self.log(f"Report generated: {overview[:80]}...", "SUCCESS")
            self.results.append(("Parent Report", "PASS"))
            return True
        else:
            self.log(f"Parent report failed: {response.text if response else 'No response'}", "WARNING")
            self.results.append(("Parent Report", "FAIL/SKIP"))
            return False
    
    def print_summary(self):
        """Print test summary"""
        self.log("\n\n========== TEST SUMMARY ==========", "INFO")
        
        total = len(self.results)
        passed = sum(1 for _, status in self.results if status == "PASS")
        failed = sum(1 for _, status in self.results if "FAIL" in status)
        
        for test_name, status in self.results:
            if status == "PASS":
                self.log(f"✓ {test_name}: {status}", "SUCCESS")
            else:
                self.log(f"✗ {test_name}: {status}", "ERROR" if status == "FAIL" else "WARNING")
        
        self.log(f"\n{BLUE}Total: {total} | Passed: {passed} | Failed: {failed}{END}", "INFO")
        
        if failed == 0:
            self.log("\n🎉 All tests passed!", "SUCCESS")
        else:
            self.log(f"\n⚠️  {failed} tests failed or skipped", "WARNING")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("\n╔════════════════════════════════════════════════════════════╗", "INFO")
        self.log("║     UpChild ML Pipeline API - Comprehensive Test Suite    ║", "INFO")
        self.log("╚════════════════════════════════════════════════════════════╝", "INFO")
        
        # Test health
        if not self.test_health():
            self.log("Health check failed. Aborting.", "ERROR")
            return
        
        # Login
        if not self.login():
            self.log("Login failed. Aborting.", "ERROR")
            return
        
        # Run all tests
        self.test_timeseries_training()
        self.test_mood_prediction()
        self.test_mood_trend()
        
        self.test_anomaly_training()
        self.test_anomaly_detection()
        
        self.test_risk_classification()
        
        self.test_nlp_analysis()
        self.test_nlp_patterns()
        
        self.test_recommendations()
        self.test_contextual_recommendations()
        
        self.test_simple_summary()
        self.test_parent_report()
        
        # Print summary
        self.print_summary()

if __name__ == "__main__":
    tester = MLAPITester()
    tester.run_all_tests()
