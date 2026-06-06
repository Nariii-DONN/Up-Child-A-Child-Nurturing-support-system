-- Create Database
CREATE DATABASE IF NOT EXISTS upchild_db;
USE upchild_db;

-- Drop existing tables (CAUTION: This deletes all data!)
DROP TABLE IF EXISTS distribution_log;
DROP TABLE IF EXISTS fund_allocations;
DROP TABLE IF EXISTS funds;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS team_members;
DROP TABLE IF EXISTS reward;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS behavior_log;
DROP TABLE IF EXISTS health_records;
DROP TABLE IF EXISTS children;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS users;

-- ========== PARENT/USER TABLES ==========

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE children (
    child_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100),
    birth_date DATE,
    gender ENUM('Male', 'Female', 'Other'),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE health_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    record_date DATE,
    height_cm FLOAT,
    weight_kg FLOAT,
    notes TEXT,
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE
);

-- UPDATED BEHAVIOR LOG TABLE WITH AI COLUMNS
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
    ai_recommendations LONGTEXT DEFAULT '' COMMENT 'JSON recommendations',
    
    -- Additional Info
    notes TEXT,
    
    FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE,
    INDEX idx_child_date (child_id, log_date),
    INDEX idx_risk_level (ai_risk_level)
);

CREATE TABLE goal (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    target_date DATE,
    is_completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE reward (
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    goal_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    awarded_date DATE,
    FOREIGN KEY (goal_id) REFERENCES goal(goal_id) ON DELETE CASCADE
);

CREATE TABLE lessons (
    lesson_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT,
    age_group VARCHAR(50)
);

-- ========== TEAM MEMBER TABLES ==========

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

-- ========== INVENTORY TABLES ==========

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

-- ========== FUND MANAGEMENT TABLES ==========

CREATE TABLE funds (
    fund_id INT AUTO_INCREMENT PRIMARY KEY,
    total_available DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_allocated DECIMAL(10, 2) DEFAULT 0,
    total_distributed DECIMAL(10, 2) DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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
CREATE TABLE case_reports (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    team_member_id INT NOT NULL,
    photo_url VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location_name VARCHAR(255),
    priority_level ENUM('Low', 'Medium', 'High', 'Critical'),
    description TEXT,
    category ENUM('Child', 'Family', 'Medical', 'Education', 'Food', 'Shelter', 'Other'),
    child_name VARCHAR(100),
    child_age INT,
    status ENUM('New', 'In Progress', 'Assigned', 'Resolved'),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (team_member_id) REFERENCES team_members(team_member_id)
);

CREATE TABLE case_interactions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    team_member_id INT,
    action VARCHAR(100),
    comment TEXT,
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES case_reports(case_id) ON DELETE CASCADE,
    FOREIGN KEY (team_member_id) REFERENCES team_members(team_member_id)
);

-- ========== INITIALIZE DATA ==========

-- Insert default funds record
INSERT INTO funds (total_available, total_allocated, total_distributed) VALUES (0, 0, 0);

-- Verification Queries
SELECT 'Users Table' AS table_name;
SELECT 'Children Table' AS table_name;
SELECT 'Health Records Table' AS table_name;
SELECT 'Behavior Log Table' AS table_name;
SELECT 'Goals Table' AS table_name;
SELECT 'Rewards Table' AS table_name;
SELECT 'Lessons Table' AS table_name;
SELECT 'Team Members Table' AS table_name;
SELECT 'Inventory Table' AS table_name;
SELECT 'Distribution Log Table' AS table_name;
SELECT 'Funds Table' AS table_name;
SELECT 'Fund Allocations Table' AS table_name;
CREATE TABLE social_posts (
  post_id INT AUTO_INCREMENT PRIMARY KEY,
  team_member_id INT NOT NULL,
  image_path VARCHAR(255) NOT NULL,
  caption TEXT,
  need_type VARCHAR(100),
  location VARCHAR(255),
  priority VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (team_member_id) REFERENCES team_members(team_member_id)
);

