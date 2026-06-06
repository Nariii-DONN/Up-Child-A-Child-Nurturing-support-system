#!/usr/bin/env python3
import json
import urllib.request

print("Testing Flask login response format...")

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

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print("\n✅ Login Response:")
        print(json.dumps(result, indent=2))
        print("\n📋 Response keys:", list(result.keys()))
        print(f"\n🔐 Token field name: {'access_token' if 'access_token' in result else 'token' if 'token' in result else 'NOT FOUND'}")
except Exception as e:
    print(f"❌ Error: {e}")
