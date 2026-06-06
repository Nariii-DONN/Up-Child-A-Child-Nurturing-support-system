import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PWD = os.getenv("DB_PASSWORD")
DB = os.getenv("DB_NAME")

print(f"Connecting to {HOST}...")

try:
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PWD,
        database=DB,
        ssl_disabled=False,
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )
    print("SUCCESS: Connection 1 (ssl_disabled=False) worked!")
    conn.close()
except Exception as e:
    print(f"FAILED: Connection 1: {e}")

try:
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PWD,
        database=DB,
        ssl_mode='REQUIRED'
    )
    print("SUCCESS: Connection 2 (ssl_mode='REQUIRED') worked!")
    conn.close()
except Exception as e:
    print(f"FAILED: Connection 2: {e}")
