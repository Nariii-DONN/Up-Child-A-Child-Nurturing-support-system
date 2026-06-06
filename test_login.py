#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

# Test login endpoint
url = 'http://localhost:5000/login'
data = json.dumps({
    'email': 'parent@example.com',
    'password': 'password123'
}).encode('utf-8')

headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print("✅ LOGIN SUCCESS!")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"❌ Error: {e}")
