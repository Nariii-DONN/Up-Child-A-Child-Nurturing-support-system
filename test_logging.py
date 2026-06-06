"""
BEHAVIOR LOGGING - DIAGNOSTIC & TEST SCRIPT
Tests the behavior logging system to identify issues
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("BEHAVIOR LOGGING SYSTEM - DIAGNOSTIC TEST")
print("=" * 70)

# ========== TEST 1: Backend Connection ==========
print("\n✓ TEST 1: Backend Connection")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"  ✅ Backend responding on {BASE_URL}")
except Exception as e:
    print(f"  ❌ Backend not responding: {e}")
    print(f"  📌 Make sure Flask is running: python flask_app.py")
    exit(1)

# ========== TEST 2: Database Connection ==========
print("\n✓ TEST 2: Database Connection")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/children")
    if response.status_code == 401:
        print(f"  ✅ Database connected (requires auth)")
    else:
        print(f"  ✅ Database responding")
except Exception as e:
    print(f"  ❌ Database issue: {e}")

# ========== TEST 3: Get Sample Parent & Child ==========
print("\n✓ TEST 3: Finding Sample Data")
print("-" * 70)

# Try login with sample account
login_payload = {
    "email": "parent@example.com",
    "password": "password123"  # Default from sample data
}

try:
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    
    if response.status_code == 200:
        auth_data = response.json()
        token = auth_data.get("access_token")
        print(f"  ✅ Sample parent logged in successfully")
        print(f"  📌 Token: {token[:20]}...")
        
        # Get children
        headers = {"Authorization": f"Bearer {token}"}
        children_response = requests.get(f"{BASE_URL}/children", headers=headers)
        
        if children_response.status_code == 200:
            children = children_response.json()
            if children and len(children) > 0:
                child = children[0]
                child_id = child.get("id") or child.get("child_id")
                print(f"  ✅ Found child: {child.get('name')} (ID: {child_id})")
                
                # ========== TEST 4: Test Behavior Logging ==========
                print("\n✓ TEST 4: Test Behavior Logging")
                print("-" * 70)
                
                log_payload = {
                    "mood": 4,
                    "focus": 3,
                    "social": 4,
                    "tantrums": 0,
                    "sleep_hours": 8.5,
                    "notes": "Test entry - diagnostic script"
                }
                
                log_response = requests.post(
                    f"{BASE_URL}/behavior/{child_id}/log",
                    json=log_payload,
                    headers=headers
                )
                
                print(f"  Response Status: {log_response.status_code}")
                
                if log_response.status_code == 201:
                    print(f"  ✅ BEHAVIOR LOGGING WORKS!")
                    print(f"  Response: {log_response.json()}")
                elif log_response.status_code == 200:
                    print(f"  ✅ BEHAVIOR LOGGED (status 200)")
                    print(f"  Response: {log_response.json()}")
                else:
                    print(f"  ❌ Failed to log behavior")
                    print(f"  Error: {log_response.json()}")
                    
            else:
                print(f"  ❌ No children found for parent")
                print(f"  📌 Create a child in the app first")
        else:
            print(f"  ❌ Could not fetch children: {children_response.status_code}")
            
    elif response.status_code == 401:
        print(f"  ❌ Login failed - wrong password")
        print(f"  📌 Check database for correct password")
    else:
        print(f"  ❌ Login failed: {response.status_code}")
        print(f"  Response: {response.json()}")
        
except Exception as e:
    print(f"  ❌ Login error: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 70)
print("\n📌 NEXT STEPS:")
print("   1. Ensure Flask is running: python flask_app.py")
print("   2. Ensure React is running: npm start")
print("   3. Check browser console (F12) for errors")
print("   4. Check Flask terminal for error messages")
print("   5. Verify child is selected before logging")
print("\n")
