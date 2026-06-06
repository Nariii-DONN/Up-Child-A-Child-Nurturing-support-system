"""
========================================================================
DATABASE INITIALIZATION SCRIPT
========================================================================
Initializes MySQL database with correct schema for UpChild AI/ML system.
Run this ONCE to set up the database properly.
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

import os
from dotenv import load_dotenv
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'upchild_3'),
    'password': os.getenv('DB_PASSWORD', 'vaibhav123'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'ssl_disabled': False,
    'ssl_verify_cert': False,
    'ssl_verify_identity': False
}

# SQL Schema
SCHEMA_SQL = """
-- Create Database
CREATE DATABASE IF NOT EXISTS upchild_db;
USE upchild_db;

-- Drop existing tables (CAUTION: This deletes all data!)
DROP TABLE IF EXISTS distribution_log;
DROP TABLE IF EXISTS fund_allocations;
DROP TABLE IF EXISTS funds;
DROP TABLE IF EXISTS case_reports;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS team_members;
DROP TABLE IF EXISTS reward;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS behavior_logs;
DROP TABLE IF EXISTS health_records;
DROP TABLE IF EXISTS children;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS users;

-- ========== USERS TABLE ==========
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========== CHILDREN TABLE ==========
CREATE TABLE children (
    child_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100),
    birth_date DATE,
    gender ENUM('Male', 'Female', 'Other'),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== HEALTH RECORDS ==========
CREATE TABLE health_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    record_date DATE,
    height_cm FLOAT,
    weight_kg FLOAT,
    notes TEXT,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- ========== BEHAVIOR LOGS TABLE WITH AI COLUMNS ==========
CREATE TABLE behavior_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Behavior Scores (1-5 scale)
    mood INT DEFAULT 3 COMMENT '1=very sad, 5=very happy',
    focus INT DEFAULT 3 COMMENT '1=very distracted, 5=excellent focus',
    social INT DEFAULT 3 COMMENT '1=withdrawn, 5=very social',
    tantrums INT DEFAULT 0 COMMENT 'count per day (0-5)',
    sleep_hours FLOAT DEFAULT 8.0 COMMENT 'hours of sleep',
    
    -- AI Predictions & Analysis
    ai_risk_level VARCHAR(20) DEFAULT 'low' COMMENT 'low/medium/high',
    ai_cluster VARCHAR(50) DEFAULT 'balanced' COMMENT 'psyche profile cluster',
    ai_recommendations LONGTEXT COMMENT 'JSON recommendations',
    
    -- Additional Info
    notes TEXT,
    
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE,
    INDEX idx_child_date (child_id, log_date),
    INDEX idx_risk_level (ai_risk_level)
);

-- ========== GOALS TABLE ==========
CREATE TABLE goal (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    target_date DATE,
    is_completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== REWARDS TABLE ==========
CREATE TABLE reward (
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    goal_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    awarded_date DATE,
    FOREIGN KEY (goal_id) REFERENCES goal(goal_id) ON DELETE CASCADE
);

-- ========== LESSONS TABLE ==========
CREATE TABLE lessons (
    lesson_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT,
    age_group VARCHAR(50)
);

-- ========== TEAM MEMBERS TABLE ==========
CREATE TABLE team_members (
    team_member_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'volunteer',
    permissions VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========== INVENTORY TABLE ==========
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    unit VARCHAR(20) DEFAULT 'pcs',
    description TEXT,
    created_by INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES team_members(team_member_id) ON DELETE SET NULL
);

-- ========== DISTRIBUTION LOG TABLE ==========
CREATE TABLE distribution_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INT NOT NULL,
    quantity_distributed INT NOT NULL,
    distributed_to VARCHAR(100),
    distributed_by INT NOT NULL,
    distribution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id) ON DELETE CASCADE,
    FOREIGN KEY (distributed_by) REFERENCES team_members(team_member_id) ON DELETE CASCADE
);

-- ========== FUNDS TABLE ==========
CREATE TABLE funds (
    fund_id INT AUTO_INCREMENT PRIMARY KEY,
    total_available DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_allocated DECIMAL(10, 2) DEFAULT 0,
    total_distributed DECIMAL(10, 2) DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ========== FUND ALLOCATIONS TABLE ==========
CREATE TABLE fund_allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    fund_id INT NOT NULL,
    parent_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    allocated_by INT NOT NULL,
    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (allocated_by) REFERENCES team_members(team_member_id) ON DELETE CASCADE
);

-- ========== CASE REPORTS TABLE ==========
CREATE TABLE case_reports (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    team_member_id INT NOT NULL,
    photo_url VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location_name VARCHAR(255),
    report_text LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_member_id) REFERENCES team_members(team_member_id)
);
"""

def init_database():
    """Initialize database with schema"""
    print("=" * 70)
    print("UPCHILD DATABASE INITIALIZATION")
    print("=" * 70)
    
    try:
        # Connect to MySQL
        print("\n[INFO] Connecting to MySQL...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("[OK] Connected!")
        
        # Execute schema
        print("\n[INFO] Creating database and tables...")
        for statement in SCHEMA_SQL.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"  [OK] {statement.strip()[:50]}...")
                except Error as e:
                    print(f"  [WARN] {str(e)[:80]}...")
        
        connection.commit()
        print("\n[OK] Database initialized successfully!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\n[ERROR] Error: {e}")
        return False
    
    return True

def seed_sample_data():
    """Add sample data for testing"""
    print("\n" + "=" * 70)
    print("SEEDING SAMPLE DATA")
    print("=" * 70)
    
    try:
        seed_config = DB_CONFIG.copy()
        seed_config['database'] = 'upchild_db'
        connection = mysql.connector.connect(**seed_config)
        cursor = connection.cursor()
        
        print("\n[INFO] Adding sample parent user...")
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """, ('parent1', 'parent@example.com', generate_password_hash('password123')))
        connection.commit()
        user_id = cursor.lastrowid
        print(f"  [OK] Parent created (ID: {user_id})")
        
        print("\n[INFO] Adding sample child...")
        cursor.execute("""
            INSERT INTO children (user_id, name, birth_date, gender)
            VALUES (%s, %s, %s, %s)
        """, (user_id, 'Alex', '2015-06-15', 'Male'))
        connection.commit()
        child_id = cursor.lastrowid
        print(f"  [OK] Child created (ID: {child_id})")
        
        print("\n[INFO] Adding 30 days of sample behavior data...")
        base_date = datetime.now() - timedelta(days=30)
        
        for day in range(30):
            log_date = base_date + timedelta(days=day)
            
            # Generate realistic data
            mood = random.randint(2, 5)
            focus = random.randint(2, 5)
            social = random.randint(2, 5)
            tantrums = random.randint(0, 2)
            sleep_hours = random.uniform(7.5, 9.5)
            
            cursor.execute("""
                INSERT INTO behavior_logs 
                (child_id, log_date, mood, focus, social, tantrums, sleep_hours, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (child_id, log_date, mood, focus, social, tantrums, 
                  round(sleep_hours, 1), f"Day {day+1} log"))
        
        connection.commit()
        print(f"  [OK] 30 days of behavior data added!")
        
        cursor.close()
        connection.close()
        
        print("\n[OK] Sample data seeded successfully!")
        return True
        
    except Error as e:
        print(f"\n[ERROR] Error seeding data: {e}")
        return False

if __name__ == "__main__":
    # Initialize database
    if init_database():
        # Optionally seed sample data
        response = input("\nAdd sample data for testing? (y/n): ").lower()
        if response == 'y':
            seed_sample_data()
        
        print("\n" + "=" * 70)
        print("[OK] DATABASE READY!")
        print("=" * 70)
        print("\n[INFO] Next steps:")
        print("  1. Run: python flask_app.py")
        print("  2. Open: http://localhost:3000")
        print("  3. Log in with: parent@example.com")
        print("  4. Start logging behavior data!")
        print("\n" + "=" * 70)
    else:
        print("\n[ERROR] Database initialization failed!")
