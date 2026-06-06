import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vaibhav123",      # put your MySQL password here (leave "" if none)
        database="upchild_db"  # replace with your actual database name
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
