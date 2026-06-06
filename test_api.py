#!/usr/bin/env python3
import urllib.request
import json
import sys

print("Testing Flask API...")

# Test 1: Health check
try:
    print("\n1️⃣ Testing /health endpoint...")
    req = urllib.request.Request('http://localhost:5000/health', method='GET')
    with urllib.request.urlopen(req) as response:
        print(f"   ✅ Status: {response.status}")
        print(f"   ✅ Response: {response.read().decode()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Login
try:
    print("\n2️⃣ Testing /login endpoint...")
    data = json.dumps({
        'email': 'parent@example.com',
        'password': 'password123'
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'http://localhost:5000/login',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"   ✅ Status: {response.status}")
        print(f"   ✅ Response: {json.dumps(result, indent=2)}")
except urllib.error.HTTPError as e:
    print(f"   ❌ HTTP Error {e.code}")
    try:
        error_data = json.loads(e.read().decode())
        print(f"   Error details: {json.dumps(error_data, indent=2)}")
    except:
        print(f"   Response: {e.read().decode()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n✅ Test complete!")
