import mysql.connector
from mysql.connector import Error
import ssl
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load Railway credentials
HOST = os.getenv("MYSQLHOST")
USER = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQLPASSWORD")
DATABASE = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT", 3306)

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            ssl_disabled=False,
            ssl_verify_cert=False
        )
        print("✅ Connected to Railway MySQL")
        return conn
    except Error as e:
        print("❌ Connection Error:", e)
        return None


def run_interactive_console():
    conn = connect_db()
    if conn is None:
        return
    
    cursor = conn.cursor()

    print("\n===============================")
    print("  🚀 Railway Interactive SQL")
    print("  Type SQL commands below.")
    print("  Type 'exit' to quit.")
    print("===============================\n")

    while True:
        query = input("SQL> ")

        if query.lower() in ("exit", "quit"):
            print("👋 Exiting SQL console...")
            break

        if not query.strip().endswith(";"):
            print("⚠️ Add semicolon ';' at the end of SQL command.")
            continue

        try:
            cursor.execute(query.rstrip(";"))
            conn.commit()

            # If SELECT, fetch results
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                print("\n--- Result ---")
                for row in rows:
                    print(row)
                print("--------------\n")
            else:
                print("✅ SQL executed successfully\n")

        except Error as err:
            print("❌ SQL Error:", err)

    cursor.close()
    conn.close()
    print("🔌 Disconnected from Railway.")


if __name__ == "__main__":
    run_interactive_console()
