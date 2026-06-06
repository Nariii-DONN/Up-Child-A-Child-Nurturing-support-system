import requests
import random
import string

BASE_URL = "http://127.0.0.1:5000"

# ----------- Helpers -----------
def rand_str(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

TEST_USER = {
    "name": f"TestUser_{rand_str()}",
    "email": f"test_{rand_str()}@example.com",
    "password": "testpass123"
}

TEST_CHILD = {
    "name": f"Child_{rand_str()}",
    "age": 5,
    "gender": "Female"
}

# ----------- Utility Shortcuts -----------
def GET(path, headers=None):
    return requests.get(f"{BASE_URL}{path}", headers=headers or {})

def POST(path, json=None, headers=None):
    return requests.post(f"{BASE_URL}{path}", json=json or {}, headers=headers or {})

def DELETE(path, headers=None):
    return requests.delete(f"{BASE_URL}{path}", headers=headers or {})

# ----------- Tests -----------
def test_health():
    print("\n🔹 Testing /api/health ...")
    r = GET("/api/health")
    ok = (r.status_code == 200 and r.json().get("status") == "healthy")
    print("✅ PASS" if ok else f"❌ FAIL: {r.text}")
    return ok

def test_db():
    print("\n🔹 Testing /test_db ...")
    r = GET("/test_db")
    ok = (r.status_code == 200 and "connected_to" in r.json())
    print("✅ PASS" if ok else f"❌ FAIL: {r.text}")
    return ok

def add_user():
    print(f"\n🔹 Testing /add_user for {TEST_USER['email']}")
    r = POST("/add_user", json=TEST_USER)
    if r.status_code == 201:
        print("✅ User added successfully.")
        return True
    if "already" in r.text or "Duplicate" in r.text:
        print("ℹ️ User already exists, continuing.")
        return True
    print(f"❌ FAIL: {r.status_code} {r.text}")
    return False

def login():
    print("\n🔹 Testing /login ...")
    r = POST("/login", json={"email": TEST_USER["email"], "password": TEST_USER["password"]})
    if r.status_code == 200 and "token" in r.json():
        token = r.json()["token"]
        print("✅ Login successful, token received.")
        return token
    print(f"❌ FAIL: {r.status_code} {r.text}")
    return None

def profile(token):
    print("\n🔹 Testing /profile (protected) ...")
    headers = {"Authorization": f"Bearer {token}"}
    r = GET("/profile", headers=headers)
    ok = (r.status_code == 200 and r.json().get("email") == TEST_USER["email"])
    print("✅ PASS" if ok else f"❌ FAIL: {r.status_code} {r.text}")
    return ok

def add_child(token):
    print(f"\n🔹 Testing /add_child for {TEST_CHILD['name']} ...")
    headers = {"Authorization": f"Bearer {token}"}
    r = POST("/add_child", json=TEST_CHILD, headers=headers)
    ok = (r.status_code == 201)
    print("✅ Child added successfully." if ok else f"❌ FAIL: {r.status_code} {r.text}")
    return ok

def list_children(token):
    print("\n🔹 Testing /children (protected) ...")
    headers = {"Authorization": f"Bearer {token}"}
    r = GET("/children", headers=headers)
    if r.status_code != 200:
        print(f"❌ FAIL: {r.status_code} {r.text}")
        return None, None
    children = r.json()
    print(f"ℹ️ Returned children: {children}")
    match = next((c for c in children if c["name"] == TEST_CHILD["name"]), None)
    print("✅ Child verified in list." if match else "❌ Child not found.")
    return children, match

def fetch_user_id():
    r = GET("/users")
    if r.status_code != 200:
        return None
    for u in r.json():
        if u.get("email") == TEST_USER["email"]:
            return u.get("id")
    return None

def cleanup(child_id, user_id):
    print("\n🧹 Cleaning up test data ...")
    if child_id:
        r = DELETE(f"/delete_child/{child_id}")
        print("✅ Child deleted" if r.status_code == 200 else f"⚠️ Failed to delete child: {r.status_code}")
    if user_id:
        r = DELETE(f"/delete_user/{user_id}")
        print("✅ User deleted" if r.status_code == 200 else f"⚠️ Failed to delete user: {r.status_code}")

# ----------- Main Runner -----------
def run():
    print("\n🚀 Starting Automated Backend Test Suite...\n")

    if not test_health(): return
    if not test_db(): return
    if not add_user(): return

    token = login()
    if not token: return

    if not profile(token):
        print("⛔ Stopping tests — profile route failed.")
        return

    if not add_child(token):
        print("⛔ Stopping tests — add_child failed.")
        uid = fetch_user_id()
        cleanup(child_id=None, user_id=uid)
        return

    children, match = list_children(token)
    uid = fetch_user_id()
    cid = match["child_id"] if match else None

    cleanup(cid, uid)

    print("\n✅✅ All Tests Completed Successfully.\n")

if __name__ == "__main__":
    run()
