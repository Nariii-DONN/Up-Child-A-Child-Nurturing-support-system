# DEBUG: Script started
print("=== Flask app script started ===")
# [DEBUG] Importing Flask and dependencies...
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import os, uuid
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from sqlalchemy import text

# [DEBUG] Importing AI/ML modules...
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Legacy behavior_ai_model - optional
try:
    from behavior_ai_model import (
        BehaviorMLModel, BehaviorPatternAnalyzer, PsycheProfileGenerator,
        InterventionRecommender, create_summary_report, PSYCHE_PROFILES
    )
    print("=== behavior_ai_model imported ===")
    ai_model_available = True
except Exception as e:
    print(f"[WARNING] behavior_ai_model not available: {e}")
    print("[INFO] Using new ML pipeline instead")
    ai_model_available = False
    BehaviorMLModel = None

# Import new ML modules
try:
    from ml_models import (
        TimeSeriesPredictor, AnomalyDetector, RiskClassifier,
        NLPAnalyzer, RecommendationEngine, Explainer
    )
    print("=== ML Pipeline modules imported ===")
except Exception as e:
    print(f"[IMPORT ERROR] Could not import ML Pipeline: {e}")
# ========================================

# [DEBUG] Initializing Flask app...
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    print(f"[DEBUG] Creating upload folder: {UPLOAD_FOLDER}")
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = "uploads/posts"
if not os.path.exists(UPLOAD_FOLDER):
    print(f"[DEBUG] Creating upload posts folder: {UPLOAD_FOLDER}")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Enable CORS for all routes
print("[DEBUG] Enabling CORS...")
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------- MySQL / SQLAlchemy Configuration ----------------
print("[DEBUG] Configuring MySQL/SQLAlchemy for Cloud DB...")
from dotenv import load_dotenv
load_dotenv()

MYSQL_USER = os.getenv('DB_USER', 'upchild_3')
MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'vaibhav123')
MYSQL_HOST = os.getenv('DB_HOST', '127.0.0.1')
MYSQL_PORT = os.getenv('DB_PORT', '3306')
MYSQL_DB = os.getenv('DB_NAME', 'upchild_db')

# Cloud DBs usually require ssl
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl_disabled": False,
        "ssl_verify_cert": False,
        "ssl_verify_identity": False
    }
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

print("[DEBUG] Initializing SQLAlchemy...")
db = SQLAlchemy(app)
print("[DEBUG] Initializing JWT Manager...")
jwt = JWTManager(app)

# ========== INITIALIZE AI/ML MODELS ========== 
print("[DEBUG] Initializing AI/ML models...")

# Initialize legacy model if available
if ai_model_available:
    ai_model = BehaviorMLModel()
else:
    ai_model = None

# Initialize new ML Pipeline components
try:
    ts_predictor = TimeSeriesPredictor(model_type='lstm', sequence_length=14)
    anomaly_detector = AnomalyDetector(method='isolation_forest')
    risk_classifier = RiskClassifier(algorithm='randomforest')
    nlp_analyzer = NLPAnalyzer(use_transformer=False)  # TextBlob only (no transformer download)
    recommendation_engine = RecommendationEngine()
    explainer = Explainer()
    print("=== All ML Pipeline components initialized ===")
except Exception as e:
    print(f"[WARNING] ML Pipeline initialization incomplete: {e}")
# ==========================================

# ========== DATABASE MODELS ==========
class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column("team_member_id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default="volunteer")
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FeedPost(db.Model):
    __tablename__ = "feed_posts"

    id = db.Column(db.Integer, primary_key=True)

    team_member_id = db.Column(
        db.Integer,
        db.ForeignKey("team_members.team_member_id"),
        nullable=False
    )

    image_url = db.Column(db.String(255), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    team_member = db.relationship("TeamMember", backref="feed_posts")

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Child(db.Model):
    __tablename__ = 'children'
    child_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))

# ========== BEHAVIOR MODEL - NEW ==========
class BehaviorLog(db.Model):
    __tablename__ = 'behavior_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.child_id'), nullable=False)
    log_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Behavior scores (1-5 scale)
    mood = db.Column(db.Integer, default=3)  # 1=very sad, 5=very happy
    focus = db.Column(db.Integer, default=3)
    social = db.Column(db.Integer, default=3)  # social interaction
    tantrums = db.Column(db.Integer, default=0)  # count per day
    sleep_hours = db.Column(db.Float, default=8.0)
    
    # AI Predictions - NEW COLUMNS
    ai_risk_level = db.Column(db.String(20), default='low')  # low/medium/high
    ai_cluster = db.Column(db.String(50), default='balanced')  # high_impulse, anxious, resilient, etc.
    ai_recommendations = db.Column(db.Text, default='')
    
    notes = db.Column(db.Text)
    
    child = db.relationship("Child", backref="behavior_logs")

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20), default='pcs')
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('team_members.team_member_id'))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DistributionLog(db.Model):
    __tablename__ = 'distribution_log'
    log_id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'), nullable=False)
    quantity_distributed = db.Column(db.Integer, nullable=False)
    distributed_to = db.Column(db.String(100))
    distributed_by = db.Column(db.Integer, db.ForeignKey('team_members.team_member_id'), nullable=False)
    distribution_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

class Fund(db.Model):
    __tablename__ = 'funds'
    fund_id = db.Column(db.Integer, primary_key=True)
    total_available = db.Column(db.Numeric(10, 2), default=0)
    total_allocated = db.Column(db.Numeric(10, 2), default=0)
    total_distributed = db.Column(db.Numeric(10, 2), default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FundAllocation(db.Model):
    __tablename__ = 'fund_allocations'
    allocation_id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.fund_id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    allocated_by = db.Column(db.Integer, db.ForeignKey('team_members.team_member_id'), nullable=False)
    allocation_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

class CaseReport(db.Model):
    __tablename__ = 'case_reports'
    case_id = db.Column(db.Integer, primary_key=True)
    team_member_id = db.Column(db.Integer, db.ForeignKey('team_members.team_member_id'), nullable=False)
    photo_url = db.Column(db.String(255))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    location_name = db.Column(db.String(255))
    priority_level = db.Column(db.Enum('Low', 'Medium', 'High', 'Critical'))
    description = db.Column(db.Text)
    category = db.Column(db.Enum('Child', 'Family', 'Medical', 'Education', 'Food', 'Shelter', 'Other'))
    child_name = db.Column(db.String(100))
    child_age = db.Column(db.Integer)
    status = db.Column(db.Enum('New', 'In Progress', 'Assigned', 'Resolved'), default='New')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ========== HEALTH CHECK ROUTES ==========

@app.route("/api/test", methods=["GET"])
def test_connection():
    return jsonify({"message": "Flask connection working"}), 200

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/test_db", methods=["GET"])
def test_db():
    try:
        result = db.session.execute(text("SELECT DATABASE();"))
        db_name = list(result)[0][0]
        return jsonify({"connected_to": db_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== PARENT USER ROUTES ==========
@app.route("/uploads/posts/<filename>")
def serve_post_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/register", methods=["POST", "OPTIONS"])
def register_user():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        data = request.get_json()
        print("Registration data received:", data)
        
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if email exists
        existing = db.session.execute(
            text("SELECT * FROM users WHERE email = :email"), {"email": email}
        ).fetchone()

        if existing:
            return jsonify({"error": "Email already registered"}), 400

        # Hash password and insert
        hashed_password = generate_password_hash(password)
        db.session.execute(
            text("INSERT INTO users (username, email, password_hash) VALUES (:n, :e, :p)"),
            {"n": name, "e": email, "p": hashed_password}
        )
        db.session.commit()
        
        print(f"User {name} registered successfully")
        return jsonify({"message": f"User {name} registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print("Registration error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST", "OPTIONS"])
def login_user():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = db.session.execute(
            text("SELECT user_id, username, email, password_hash FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user[3], password):
            return jsonify({"error": "Invalid password"}), 401

        token = create_access_token(identity=email)
        return jsonify({
            "message": "Login successful", 
            "token": token,
            "parentName": user[1]
        }), 200

    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = db.session.execute(
        text("SELECT username, email FROM users WHERE email = :email"), {"email": current_user}
    ).fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"username": user[0], "email": user[1]}), 200

@app.route("/users", methods=["GET", "OPTIONS"])
def get_users():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        result = db.session.execute(text("SELECT user_id, username, email FROM users"))
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in result]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_user/<int:user_id>", methods=["DELETE", "OPTIONS"])
def delete_user(user_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        db.session.execute(text("DELETE FROM children WHERE user_id = :uid"), {"uid": user_id})
        db.session.execute(text("DELETE FROM users WHERE user_id = :uid"), {"uid": user_id})
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ========== CHILD MANAGEMENT ROUTES ==========

@app.route("/add_child", methods=["POST", "OPTIONS"])
@jwt_required()
def add_child():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        name = data.get("name")
        birth_date = data.get("birth_date")
        gender = data.get("gender")

        if not name or not birth_date or not gender:
            return jsonify({"error": "All fields (name, birth_date, gender) are required"}), 400

        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        if not user:
            return jsonify({"error": "Parent not found"}), 404

        db.session.execute(
            text("INSERT INTO children (user_id, name, birth_date, gender) VALUES (:uid, :n, :bd, :g)"),
            {"uid": user[0], "n": name, "bd": birth_date, "g": gender}
        )
        db.session.commit()
        return jsonify({"message": f"Child {name} added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/children", methods=["GET", "OPTIONS"])
@jwt_required()
def list_children():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        if not user:
            return jsonify({"error": "Parent not found"}), 404

        rows = db.session.execute(
            text("SELECT child_id, name, birth_date, gender FROM children WHERE user_id = :uid"),
            {"uid": user[0]}
        ).fetchall()

        children = [{"child_id": r[0], "name": r[1], "birth_date": str(r[2]), "gender": r[3]} for r in rows]
        return jsonify(children), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/child/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_child_details(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        child = db.session.execute(
            text("SELECT child_id, name, birth_date, gender FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        health_records = db.session.execute(
            text("SELECT record_id, record_date, height_cm, weight_kg, notes FROM health_records WHERE child_id = :cid ORDER BY record_date DESC"),
            {"cid": child_id}
        ).fetchall()

        goals = db.session.execute(
            text("SELECT goal_id, description, target_date, is_completed FROM goal WHERE user_id = :uid ORDER BY target_date DESC LIMIT 5"),
            {"uid": user[0]}
        ).fetchall()

        records = [{"record_id": r[0], "date": str(r[1]), "height": r[2], "weight": r[3], "notes": r[4]} for r in health_records]
        parent_goals = [{"goal_id": r[0], "description": r[1], "target_date": str(r[2]), "is_completed": bool(r[3])} for r in goals]

        return jsonify({
            "child_id": child[0],
            "name": child[1],
            "birth_date": str(child[2]),
            "gender": child[3],
            "health_records": records,
            "goals": parent_goals
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/child/<int:child_id>/health", methods=["POST", "OPTIONS"])
@jwt_required()
def add_health_record(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        record_date = data.get("record_date")
        height_cm = data.get("height_cm")
        weight_kg = data.get("weight_kg")
        notes = data.get("notes", "")

        if not record_date or not height_cm or not weight_kg:
            return jsonify({"error": "Date, height, and weight are required"}), 400

        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        db.session.execute(
            text("INSERT INTO health_records (child_id, record_date, height_cm, weight_kg, notes) VALUES (:cid, :rd, :h, :w, :n)"),
            {"cid": child_id, "rd": record_date, "h": height_cm, "w": weight_kg, "n": notes}
        )
        db.session.commit()
        return jsonify({"message": "Health record added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/delete_child/<int:child_id>", methods=["DELETE", "OPTIONS"])
def delete_child(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
        
    try:
        db.session.execute(text("DELETE FROM children WHERE child_id = :cid"), {"cid": child_id})
        db.session.commit()
        return jsonify({"message": "Child deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ========== GOALS MODULE ENDPOINTS ==========
@app.route("/child/<int:child_id>/goals", methods=["POST", "OPTIONS"])
@jwt_required()
def add_goal(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        description = data.get("description")
        target_date = data.get("target_date")
        if not description or not target_date:
            return jsonify({"error": "Description and target date required"}), 400
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        if not child:
            return jsonify({"error": "Child not found"}), 404
        db.session.execute(
            text("INSERT INTO goal (user_id, description, target_date, is_completed) VALUES (:uid, :desc, :td, 0)"),
            {"uid": user[0], "desc": description, "td": target_date}
        )
        db.session.commit()
        return jsonify({"message": "Goal added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/child/<int:child_id>/goals/<int:goal_id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def toggle_goal(child_id, goal_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Only allow toggling if the goal belongs to the user and child
        goal = db.session.execute(
            text("SELECT goal_id, is_completed FROM goal WHERE goal_id = :gid AND user_id = :uid"),
            {"gid": goal_id, "uid": user[0]}
        ).fetchone()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        new_status = 0 if goal[1] else 1
        db.session.execute(
            text("UPDATE goal SET is_completed = :status WHERE goal_id = :gid"),
            {"status": new_status, "gid": goal_id}
        )
        db.session.commit()
        return jsonify({"message": "Goal status updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/child/<int:child_id>/goals/<int:goal_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def delete_goal(child_id, goal_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Only allow deleting if the goal belongs to the user and child
        goal = db.session.execute(
            text("SELECT goal_id FROM goal WHERE goal_id = :gid AND user_id = :uid"),
            {"gid": goal_id, "uid": user[0]}
        ).fetchone()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        db.session.execute(
            text("DELETE FROM goal WHERE goal_id = :gid"), {"gid": goal_id}
        )
        db.session.commit()
        return jsonify({"message": "Goal deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ========== AI BEHAVIOR TRACKING MODULE - NEW COMPLETE MODULE ==========
# ========== HELPER FUNCTIONS FOR AI ANALYSIS ==========
# ========== AI BEHAVIOR TRACKING MODULE - NEW COMPLETE MODULE ==========
# ========== HELPER FUNCTIONS FOR AI ANALYSIS ==========

def load_behavior_model():
    """Load the pre-trained ML model (you'll train this separately)"""
    try:
        model = joblib.load('behavior_predictor.pkl')
        return model
    except:
        # Fallback simple rule-based model if ML model not found
        return None


def extract_behavior_features(child_id, days=30):
    """Extract features from last N days of behavior logs"""
    try:
        thirty_days_ago = datetime.utcnow() - timedelta(days=days)

        logs = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours 
                FROM behavior_logs 
                WHERE child_id = :cid AND log_date > :date 
                ORDER BY log_date DESC
            """), {"cid": child_id, "date": thirty_days_ago}
        ).fetchall()

        if len(logs) < 3:  # Need some history
            return None

        df = pd.DataFrame(logs, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours'])

        features = {
            'avg_mood': df['mood'].mean(),
            'mood_std': df['mood'].std(),
            'avg_focus': df['focus'].mean(),
            'avg_social': df['social'].mean(),
            'avg_tantrums': df['tantrums'].mean(),
            'max_tantrums': df['tantrums'].max(),
            'avg_sleep': df['sleep_hours'].mean(),
            'short_sleep_ratio': (df['sleep_hours'] < 7).mean(),
            'tantrum_days_ratio': (df['tantrums'] > 0).mean(),
            'mood_trend': (df['mood'].iloc[-1] - df['mood'].iloc[0]) / max(len(df) - 1, 1),
            'total_logs': len(df)
        }

        return features
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return None


def get_risk_emoji(risk_level):
    """Get emoji for risk level"""
    emojis = {
        'low': '[OK]',
        'medium': '[WARN]',
        'high': '[ALERT]',
        'NO_DATA': '[PENDING]'
    }
    return emojis.get((risk_level or '').lower(), '[INFO]')


def predict_behavior_risk(features):
    """Simple ML prediction or rule-based fallback"""
    model = load_behavior_model()

    if model and features:
        feature_vector = np.array([[
            features['avg_mood'],
            features['avg_focus'],
            features['avg_social'],
            features['avg_tantrums'],
            features['avg_sleep'],
            features['tantrum_days_ratio']
        ]])
        prediction = model.predict(feature_vector)[0]
        cluster_idx = model.predict_proba(feature_vector)[0].argmax()
        clusters = ['balanced', 'high_impulse', 'anxious', 'low_energy']
        return prediction, clusters[cluster_idx]

    # Fallback rule-based
    tantrums = features.get('avg_tantrums', 0)
    sleep = features.get('avg_sleep', 8)
    mood = features.get('avg_mood', 3)

    if tantrums > 2 or sleep < 7:
        risk = 'high'
        cluster = 'high_impulse'
    elif mood < 2.5 or tantrums > 1:
        risk = 'medium'
        cluster = 'anxious'
    else:
        risk = 'low'
        cluster = 'balanced'

    return risk, cluster


def build_psyche_profile(features):
    """Multi-axis child profile: emotional, impulse, social, self-regulation"""
    profile = {}

    # Emotional stability
    mood_std = features.get('mood_std') or 0
    if mood_std < 0.6:
        profile['emotional_stability'] = 'stable'
    elif mood_std < 1.2:
        profile['emotional_stability'] = 'somewhat_variable'
    else:
        profile['emotional_stability'] = 'highly_variable'

    # Impulse / frustration control
    avg_tantrums = features.get('avg_tantrums', 0)
    tantrum_days_ratio = features.get('tantrum_days_ratio', 0)
    if avg_tantrums == 0 and tantrum_days_ratio < 0.15:
        profile['impulse_control'] = 'good'
    elif avg_tantrums <= 1:
        profile['impulse_control'] = 'moderate'
    else:
        profile['impulse_control'] = 'challenged'

    # Social engagement
    avg_social = features.get('avg_social', 3)
    if avg_social >= 4:
        profile['social_engagement'] = 'high'
    elif avg_social >= 3:
        profile['social_engagement'] = 'balanced'
    else:
        profile['social_engagement'] = 'low'

    # Self-regulation (sleep + focus)
    avg_sleep = features.get('avg_sleep', 8)
    avg_focus = features.get('avg_focus', 3)
    if avg_sleep >= 8 and avg_focus >= 3:
        profile['self_regulation'] = 'strong'
    elif avg_sleep >= 7:
        profile['self_regulation'] = 'developing'
    else:
        profile['self_regulation'] = 'weak'

    return profile


def build_parent_report(features, profile):
    """Build multi-sentence, parent-friendly report text"""
    sections = []

    # Emotional overview
    emo = profile.get('emotional_stability')
    if emo == 'stable':
        sections.append(
            "Emotional state appears generally stable, with mood mostly in the positive or neutral range over recent days."
        )
    elif emo == 'somewhat_variable':
        sections.append(
            "Emotional state shows moderate ups and downs, which is common, but worth watching if the same triggers keep repeating."
        )
    else:
        sections.append(
            "Emotional state is highly variable, with frequent shifts between low and high moods."
        )

    # Impulse control
    ic = profile.get('impulse_control')
    if ic == 'good':
        sections.append(
            "Tantrums and outbursts are infrequent, suggesting good frustration tolerance for this age."
        )
    elif ic == 'moderate':
        sections.append(
            "Tantrums are occasional; consistent routines and calm responses can support further self‑control."
        )
    else:
        sections.append(
            "Tantrums occur more often than typical; predictable routines and clear limits may help reduce overload moments."
        )

    # Social engagement
    se = profile.get('social_engagement')
    if se == 'high':
        sections.append(
            "Social engagement is high; the child seems comfortable connecting and interacting with others."
        )
    elif se == 'balanced':
        sections.append(
            "Social engagement is balanced; the child participates but may need some warm‑up time in groups."
        )
    else:
        sections.append(
            "Social engagement appears lower; gentle, low-pressure opportunities to interact with familiar people may be helpful."
        )

    # Self-regulation
    sr = profile.get('self_regulation')
    if sr == 'strong':
        sections.append(
            "Sleep and focus patterns suggest strong self‑regulation, which supports learning and daily behavior."
        )
    elif sr == 'developing':
        sections.append(
            "Self‑regulation is developing; small adjustments to bedtime, screens, and transitions could improve focus."
        )
    else:
        sections.append(
            "Sleep and focus patterns point to weaker self‑regulation; consistent routines and wind‑down time before bed are especially important."
        )

    # Short, concrete recommendations
    recs = []
    if features.get('short_sleep_ratio', 0) > 0.3:
        recs.append("Work toward a consistent bedtime and a calming pre‑sleep routine.")
    if features.get('tantrum_days_ratio', 0) > 0.3:
        recs.append("Use a calm‑down space and name feelings early, before they explode.")
    if features.get('avg_social', 3) < 3:
        recs.append("Schedule short, structured play with one familiar peer instead of big groups.")
    if features.get('avg_mood', 3) < 3:
        recs.append("Notice and praise even small moments of effort and kindness during the day.")

    return sections, recs


# ========== BEHAVIOR LOGGING ROUTES ==========

@app.route("/behavior/<int:child_id>/log", methods=["POST", "OPTIONS"])
@jwt_required()
def log_behavior(child_id):
    """Log behavior entry for a child and trigger AI analysis"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        print(f"[LOG_BEHAVIOR] User: {current_user}, Child: {child_id}")

        # Verify parent owns this child
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": f"Child {child_id} not found or not owned by user"}), 404

        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate and extract fields
        mood = int(data.get("mood", 3))
        focus = int(data.get("focus", 3))
        social = int(data.get("social", 3))
        tantrums = int(data.get("tantrums", 0))
        sleep_hours = float(data.get("sleep_hours", 8.0))
        notes = str(data.get("notes", ""))

        print(f"[LOG_BEHAVIOR] Inserting: mood={mood}, focus={focus}, social={social}, tantrums={tantrums}, sleep={sleep_hours}")

        # Insert behavior log
        db.session.execute(
            text("""
                INSERT INTO behavior_logs (child_id, mood, focus, social, tantrums, sleep_hours, notes, log_date)
                VALUES (:cid, :mood, :focus, :social, :tantrums, :sleep, :notes, NOW())
            """),
            {
                "cid": child_id,
                "mood": mood,
                "focus": focus,
                "social": social,
                "tantrums": tantrums,
                "sleep": sleep_hours,
                "notes": notes
            }
        )
        db.session.commit()
        print(f"[LOG_BEHAVIOR] Successfully inserted behavior log")

        # Run AI analysis
        try:
            generate_ai_insights(child_id)
            print(f"[LOG_BEHAVIOR] AI analysis completed")
        except Exception as ai_err:
            print(f"[LOG_BEHAVIOR] AI analysis warning: {str(ai_err)}")
            # Don't fail the request if AI analysis fails

        return jsonify({
            "status": "success",
            "message": "Behavior logged and AI analysis completed",
            "child_id": child_id
        }), 201

    except Exception as e:
        print(f"[LOG_BEHAVIOR] Error: {str(e)}")
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": f"Failed to log behavior: {str(e)}"
        }), 500


@app.route("/behavior/<int:child_id>/insights", methods=["GET", "OPTIONS"])
@jwt_required()
def get_behavior_insights(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()

        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        # Ensure latest analysis
        generate_ai_insights(child_id)

        latest_insight = db.session.execute(
            text("""
                SELECT ai_risk_level, ai_cluster, ai_recommendations, log_date
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 1
            """), {"cid": child_id}
        ).fetchone()

        recent_logs = db.session.execute(
            text("""
                SELECT log_date, mood, focus, social, tantrums, sleep_hours
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 7
            """), {"cid": child_id}
        ).fetchall()

        if not latest_insight:
            return jsonify({
                "risk_level": "NO_DATA",
                "risk_emoji": "⏳",
                "behavior_type": "Need more logs",
                "recommendations": ["Log 2–3 moods daily for AI insights!"],
                "recent_logs": []
            }), 200

        logs_data = [{
            "date": str(r[0]),
            "mood": r[1],
            "focus": r[2],
            "social": r[3],
            "tantrums": r[4],
            "sleep": r[5],
        } for r in recent_logs]

        risk_level = latest_insight[0] or 'NO_DATA'
        cluster = latest_insight[1] or 'profile'
        full_text = latest_insight[2] or ""
        # Split long text into logical chunks for bullets
        rec_lines = [s.strip() for s in full_text.split("Recommendations:") if s.strip()]

        return jsonify({
            "risk_level": risk_level,
            "risk_emoji": get_risk_emoji(risk_level),
            "behavior_type": cluster,
            "recommendations": rec_lines,
            "last_updated": str(latest_insight[3]) if latest_insight[3] else 'never',
            "recent_logs": logs_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_ai_insights(child_id):
    """Background AI analysis function - NOW WITH ADVANCED ML"""
    try:
        # Fetch recent behavior logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours, log_date 
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        if len(logs_data) < 3:
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(logs_data, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours', 'log_date'])
        
        # Run advanced AI analysis
        analysis = ai_model.predict(df)
        
        if analysis['status'] != 'success':
            return
        
        profile = analysis['profile']
        recommendations = analysis['recommendations']
        
        # Build comprehensive report
        full_text = create_summary_report(analysis)
        
        # Store in database
        db.session.execute(
            text("""
                UPDATE behavior_logs 
                SET ai_risk_level = :risk, ai_cluster = :cluster, ai_recommendations = :recs
                WHERE child_id = :cid AND log_date = (
                    SELECT MAX(log_date) FROM behavior_logs WHERE child_id = :cid2
                )
            """),
            {
                "risk": profile['risk_assessment']['risk_level'],
                "cluster": profile['cluster'],
                "recs": full_text,
                "cid": child_id,
                "cid2": child_id
            }
        )
        db.session.commit()
        
    except Exception as e:
        print(f"AI analysis error: {e}")
        db.session.rollback()


@app.route("/behavior/<int:child_id>/history", methods=["GET", "OPTIONS"])
@jwt_required()
def get_behavior_history(child_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        logs = db.session.execute(
            text("""
                SELECT log_date, mood, focus, social, tantrums, sleep_hours, 
                       ai_risk_level, ai_recommendations, notes
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()

        history = [{
            "date": str(l[0]),
            "mood": l[1],
            "focus": l[2],
            "social": l[3],
            "tantrums": l[4],
            "sleep": l[5],
            "risk_level": l[6],
            "recommendations": l[7],
            "notes": l[8]
        } for l in logs]

        return jsonify(history), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== NEW ADVANCED AI ENDPOINTS ==========

@app.route("/behavior/<int:child_id>/psyche-profile", methods=["GET", "OPTIONS"])
@jwt_required()
def get_psyche_profile(child_id):
    """Get detailed psyche profile with dimensions and interventions"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        # Fetch recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours, log_date 
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()

        if len(logs_data) < 3:
            return jsonify({
                "status": "insufficient_data",
                "message": "Need at least 3 days of behavior logs",
                "logs_count": len(logs_data)
            }), 200

        # Run advanced analysis
        df = pd.DataFrame(logs_data, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours', 'log_date'])
        analysis = ai_model.predict(df)

        if analysis['status'] != 'success':
            return jsonify(analysis), 200

        profile = analysis['profile']
        recommendations = analysis['recommendations']

        return jsonify({
            "status": "success",
            "psyche_cluster": profile['cluster'],
            "profile_name": profile['profile']['name'],
            "profile_description": profile['profile']['description'],
            "profile_emoji": profile['profile']['emoji'],
            "confidence": profile['confidence'],
            "dimensions": profile['dimensions'],
            "risk_assessment": profile['risk_assessment'],
            "strengths": recommendations['strengths_to_build_on'],
            "growth_areas": recommendations['growth_areas'],
            "parenting_style": recommendations['parenting_approaches']['style'],
            "key_principles": recommendations['parenting_approaches']['key_principles'],
            "intervention_confidence": f"{profile['confidence']*100:.0f}%"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/behavior/<int:child_id>/recommendations", methods=["GET", "OPTIONS"])
@jwt_required()
def get_behavior_recommendations(child_id):
    """Get personalized intervention recommendations"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        # Fetch recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours, log_date 
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()

        if len(logs_data) < 3:
            return jsonify({
                "status": "insufficient_data",
                "message": "Need at least 3 days of behavior logs for recommendations"
            }), 200

        df = pd.DataFrame(logs_data, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours', 'log_date'])
        analysis = ai_model.predict(df)

        if analysis['status'] != 'success':
            return jsonify(analysis), 200

        recommendations = analysis['recommendations']

        return jsonify({
            "status": "success",
            "cluster": recommendations['cluster'],
            "profile_name": recommendations['profile_name'],
            "immediate_actions": recommendations['immediate_actions'],
            "weekly_strategies": recommendations['weekly_strategies'],
            "long_term_goals": recommendations['long_term_goals'],
            "success_indicators": recommendations['success_indicators'],
            "professional_resources": recommendations['professional_resources'],
            "follow_up_days": recommendations['follow_up_period_days']
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/behavior/<int:child_id>/behavior-patterns", methods=["GET", "OPTIONS"])
@jwt_required()
def get_behavior_patterns(child_id):
    """Get detailed behavior pattern analysis"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        logs_data = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours, log_date 
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()

        if len(logs_data) < 3:
            return jsonify({"status": "insufficient_data"}), 200

        df = pd.DataFrame(logs_data, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours', 'log_date'])
        analyzer = BehaviorPatternAnalyzer()
        features = analyzer.extract_advanced_features(df)

        if not features:
            return jsonify({"status": "insufficient_data"}), 200

        return jsonify({
            "status": "success",
            "patterns": {
                "emotional": {
                    "average_mood": float(features.get('avg_mood', 3)),
                    "mood_consistency": float(features.get('mood_std', 0)),
                    "mood_trend": "improving" if features.get('mood_trend', 0) > 0.1 else "declining" if features.get('mood_trend', 0) < -0.1 else "stable",
                    "volatility_score": float(features.get('mood_volatility', 0))
                },
                "impulse_control": {
                    "average_tantrums": float(features.get('avg_tantrums', 0)),
                    "tantrum_frequency": float(features.get('tantrum_frequency_ratio', 0)),
                    "escalation_trend": float(features.get('tantrum_escalation', 0))
                },
                "sleep": {
                    "average_hours": float(features.get('avg_sleep', 8)),
                    "consistency": float(features.get('sleep_consistency', 0)),
                    "insufficient_nights": int(features.get('insufficient_sleep_days', 0))
                },
                "social": {
                    "engagement_level": features.get('social_engagement_level', 'moderate'),
                    "average_score": float(features.get('avg_social', 3))
                },
                "overall_stability": float(features.get('overall_stability_score', 50))
            },
            "trend": features.get('trend_direction', 'stable')
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/behavior/<int:child_id>/risk-report", methods=["GET", "OPTIONS"])
@jwt_required()
def get_risk_report(child_id):
    """Generate comprehensive risk assessment report"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()

        child = db.session.execute(
            text("SELECT child_id FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()

        if not child:
            return jsonify({"error": "Child not found"}), 404

        logs_data = db.session.execute(
            text("""
                SELECT mood, focus, social, tantrums, sleep_hours, log_date 
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()

        if len(logs_data) < 3:
            return jsonify({"status": "insufficient_data"}), 200

        df = pd.DataFrame(logs_data, columns=['mood', 'focus', 'social', 'tantrums', 'sleep_hours', 'log_date'])
        analysis = ai_model.predict(df)

        if analysis['status'] != 'success':
            return jsonify(analysis), 200

        risk = analysis['profile']['risk_assessment']

        return jsonify({
            "status": "success",
            "risk_level": risk['risk_level'],
            "risk_score": risk['risk_score'],
            "trend": risk['trend'],
            "concerns": risk['concerns'],
            "professional_evaluation_recommended": risk['professional_evaluation_recommended'],
            "urgent_actions": [c for c in risk['concerns'] if 'high' in c.lower() or 'declining' in c.lower()]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================================

# ================================================================

# ================================================================

# ========== TEAM MEMBER AUTHENTICATION ROUTES ==========

@app.route("/team/register", methods=["POST", "OPTIONS"])
def team_register():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        role = data.get("role", "volunteer")
        
        if not all([username, email, password, full_name]):
            return jsonify({"error": "All fields required"}), 400
        
        existing = db.session.execute(text("SELECT * FROM team_members WHERE email = :email OR username = :username"), 
            {"email": email, "username": username}).fetchone()
        
        if existing:
            return jsonify({"error": "Email or username already exists"}), 400
        
        hashed_password = generate_password_hash(password)
        db.session.execute(text("INSERT INTO team_members (username, email, password_hash, full_name, role) VALUES (:u, :e, :p, :fn, :r)"),
            {"u": username, "e": email, "p": hashed_password, "fn": full_name, "r": role})
        db.session.commit()
        
        print(f"Team member {full_name} registered successfully")
        return jsonify({"message": "Team member registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Team registration error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/team/login", methods=["POST", "OPTIONS"])
def team_login():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400
        
        team_member = db.session.execute(text("SELECT team_member_id, username, email, password_hash, full_name, role FROM team_members WHERE email = :email"),
            {"email": email}).fetchone()
        
        if not team_member:
            return jsonify({"error": "Team member not found"}), 404
        
        if not check_password_hash(team_member[3], password):
            return jsonify({"error": "Invalid password"}), 401
        
        token = create_access_token(identity=f"team_{team_member[0]}")
        
        print(f"Team member {team_member[4]} logged in successfully")
        return jsonify({
            "message": "Login successful",
            "token": token,
            "team_member_id": team_member[0],
            "username": team_member[1],
            "full_name": team_member[4],
            "role": team_member[5]
        }), 200
    except Exception as e:
        print(f"Team login error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/add", methods=["POST", "OPTIONS"])
@jwt_required()
def add_inventory_item():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        identity = get_jwt_identity()
        if not identity.startswith("team_"):
            return jsonify({"error": "Unauthorized"}), 403
        
        team_id = int(identity.split("_")[1])
        data = request.get_json()
        item_name = data.get("item_name")
        item_type = data.get("item_type")
        quantity = data.get("quantity")
        unit = data.get("unit", "pcs")
        description = data.get("description")
        
        if not all([item_name, item_type, quantity]):
            return jsonify({"error": "Missing fields"}), 400
        
        db.session.execute(text("INSERT INTO inventory (item_name, item_type, quantity, unit, description, created_by) VALUES (:n, :t, :q, :u, :d, :cb)"),
            {"n": item_name, "t": item_type, "q": quantity, "u": unit, "d": description, "cb": team_id})
        db.session.commit()
        return jsonify({"message": "Item added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/inventory", methods=["GET", "OPTIONS"])
@jwt_required()
def get_inventory():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        items = db.session.execute(text("SELECT inventory_id, item_name, item_type, quantity, unit, description FROM inventory")).fetchall()
        inventory = [{"inventory_id": i[0], "item_name": i[1], "item_type": i[2], "quantity": i[3], "unit": i[4], "description": i[5]} for i in items]
        return jsonify(inventory), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/<int:inventory_id>/distribute", methods=["POST", "OPTIONS"])
@jwt_required()
def distribute_item(inventory_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    try:
        identity = get_jwt_identity()
        if not identity.startswith("team_"):
            return jsonify({"error": "Unauthorized"}), 403
        team_id = int(identity.split("_")[1])
        data = request.get_json()
        quantity = data.get("quantity")
        distributed_to = data.get("distributed_to")
        notes = data.get("notes")
        
        item = db.session.execute(text("SELECT quantity FROM inventory WHERE inventory_id = :id"), {"id": inventory_id}).fetchone()
        if not item or item[0] < quantity:
            return jsonify({"error": "Insufficient stock"}), 400
        
        db.session.execute(text("UPDATE inventory SET quantity = quantity - :q WHERE inventory_id = :id"), {"q": quantity, "id": inventory_id})
        db.session.execute(text("INSERT INTO distribution_log (inventory_id, quantity_distributed, distributed_to, distributed_by, notes) VALUES (:id, :q, :to, :by, :n)"),
            {"id": inventory_id, "q": quantity, "to": distributed_to, "by": team_id, "n": notes})
        db.session.commit()
        return jsonify({"message": "Distribution successful"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/funds", methods=["GET", "OPTIONS"])
@jwt_required()
def get_funds():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        fund = db.session.execute(text("SELECT total_available, total_allocated, total_distributed FROM funds LIMIT 1")).fetchone()
        if not fund: return jsonify({"total_available": 0, "total_allocated": 0, "total_distributed": 0}), 200
        return jsonify({"total_available": float(fund[0]), "total_allocated": float(fund[1]), "total_distributed": float(fund[2])}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/funds/add", methods=["POST", "OPTIONS"])
@jwt_required()
def add_funds():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        data = request.get_json()
        amount = data.get("amount")
        db.session.execute(text("UPDATE funds SET total_available = total_available + :a"), {"a": amount})
        db.session.commit()
        return jsonify({"message": "Funds added"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/fund-allocations", methods=["GET", "OPTIONS"])
@jwt_required()
def get_allocations():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        rows = db.session.execute(text("SELECT allocation_id, parent_id, amount, status, allocation_date, notes FROM fund_allocations")).fetchall()
        allocs = [{"allocation_id": r[0], "parent_id": r[1], "amount": float(r[2]), "status": r[3], "date": str(r[4]), "notes": r[5]} for r in rows]
        return jsonify(allocs), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/distribution/history", methods=["GET", "OPTIONS"])
@jwt_required()
def get_distrib_history():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        rows = db.session.execute(text("SELECT log_id, inventory_id, quantity_distributed, distributed_to, distribution_date FROM distribution_log")).fetchall()
        hist = [{"log_id": r[0], "inventory_id": r[1], "quantity": r[2], "to": r[3], "date": str(r[4])} for r in rows]
        return jsonify(hist), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/team-members", methods=["GET", "OPTIONS"])
@jwt_required()
def get_team_members():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        rows = db.session.execute(text("SELECT team_member_id, username, full_name, role, status FROM team_members")).fetchall()
        members = [{"id": r[0], "username": r[1], "name": r[2], "role": r[3], "status": r[4]} for r in rows]
        return jsonify(members), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/cases", methods=["GET", "OPTIONS"])
@jwt_required()
def get_cases():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        rows = db.session.execute(text("SELECT case_id, photo_url, location_name, priority_level, category, child_name, status FROM case_reports")).fetchall()
        cases = [{"id": r[0], "photo_url": r[1], "location": r[2], "priority": r[3], "category": r[4], "child_name": r[5], "status": r[6]} for r in rows]
        return jsonify(cases), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/cases/add", methods=["POST", "OPTIONS"])
@jwt_required()
def add_case():
    if request.method == "OPTIONS": return jsonify({"message": "OK"}), 200
    try:
        identity = get_jwt_identity()
        team_id = int(identity.split("_")[1])
        data = request.get_json()
        db.session.execute(text("INSERT INTO case_reports (team_member_id, photo_url, location_name, priority_level, category, child_name, child_age, description, status) VALUES (:by, :p, :l, :pl, :c, :cn, :ca, :d, 'New')"),
            {"by": team_id, "p": data.get("photo_url"), "l": data.get("location_name"), "pl": data.get("priority_level"), "c": data.get("category"), "cn": data.get("child_name"), "ca": data.get("child_age"), "d": data.get("description")})
        db.session.commit()
        return jsonify({"message": "Case reported"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ========== ADVANCED ML PIPELINE API ENDPOINTS ==========

# ===== 1. TIME-SERIES PREDICTION ENDPOINTS =====
@app.route("/api/ml/timeseries/train/<int:child_id>", methods=["POST", "OPTIONS"])
@jwt_required()
def train_timeseries_model(child_id):
    """Train time-series model on child's behavior logs"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        # Verify child ownership
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Child not found or access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level, log_date
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date ASC LIMIT 90
            """), {"cid": child_id}
        ).fetchall()
        
        if len(logs_data) < 14:
            return jsonify({
                "error": "Insufficient data",
                "message": f"Need at least 14 logs, have {len(logs_data)}"
            }), 400
        
        # Convert to list of dicts
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Train model
        result = ts_predictor.train(logs_list)
        
        return jsonify({
            "status": "success",
            "training_result": result
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/timeseries/predict/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def predict_next_day_mood(child_id):
    """Predict next-day mood and risk"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level, log_date
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 14
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Make prediction
        prediction = ts_predictor.predict_next_day(logs_list)
        
        # Get explanation
        explanation = explainer.explain_mood_prediction(prediction)
        
        return jsonify({
            "status": "success",
            "prediction": prediction,
            "explanation": explanation
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/timeseries/trend/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_mood_trend(child_id):
    """Get 7-day mood trend forecast"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level, log_date
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 14
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Get trend
        trend_result = ts_predictor.predict_trend(logs_list, days_ahead=7)
        
        return jsonify({
            "status": "success",
            "trend": trend_result
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== 2. ANOMALY DETECTION ENDPOINTS =====
@app.route("/api/ml/anomaly/train/<int:child_id>", methods=["POST", "OPTIONS"])
@jwt_required()
def train_anomaly_model(child_id):
    """Train anomaly detection model"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 60
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        result = anomaly_detector.train(logs_list)
        
        return jsonify({
            "status": "success",
            "training_result": result
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/anomaly/detect/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def detect_anomaly(child_id):
    """Detect anomalies in recent behavior"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Detect anomalies
        anomalies = anomaly_detector.detect_anomalies(logs_list)
        
        # Get explanation
        anomaly_explanation = explainer.explain_anomaly(anomalies)
        
        return jsonify({
            "status": "success",
            "anomalies": anomalies,
            "explanation": anomaly_explanation
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== 3. RISK CLASSIFICATION ENDPOINTS =====
@app.route("/api/ml/risk/train", methods=["POST", "OPTIONS"])
@jwt_required()
def train_risk_model():
    """Train risk classification model (requires sample data)"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        data = request.get_json()
        
        # This would require structured training data
        # For demo, return info
        return jsonify({
            "status": "info",
            "message": "Risk model training requires multi-child dataset. Use production data.",
            "instructions": "Send POST with training_data containing low/medium/high risk samples"
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/risk/classify/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def classify_risk(child_id):
    """Classify behavior risk level"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Classify risk
        risk_prediction = risk_classifier.predict(logs_list)
        
        # Get explanation
        risk_explanation = explainer.explain_risk_prediction(
            risk_prediction,
            risk_classifier.get_feature_importance()
        )
        
        return jsonify({
            "status": "success",
            "risk_prediction": risk_prediction,
            "explanation": risk_explanation
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== 4. NLP ANALYSIS ENDPOINTS =====
@app.route("/api/ml/nlp/analyze", methods=["POST", "OPTIONS"])
@jwt_required()
def analyze_parent_note():
    """Analyze parent note for sentiment and emotion"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        data = request.get_json()
        text_content = data.get("text", "")
        
        if not text_content:
            return jsonify({"error": "No text provided"}), 400
        
        # Analyze note
        analysis = nlp_analyzer.analyze_note(text_content)
        
        return jsonify({
            "status": "success",
            "analysis": analysis
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/nlp/patterns/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def detect_nlp_patterns(child_id):
    """Detect patterns in parent notes"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get notes
        logs_with_notes = db.session.execute(
            text("""
                SELECT notes FROM behavior_logs 
                WHERE child_id = :cid AND notes IS NOT NULL
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        notes_list = [row[0] for row in logs_with_notes if row[0]]
        
        if not notes_list:
            return jsonify({
                "status": "info",
                "message": "No parent notes available"
            }), 200
        
        # Detect patterns
        patterns = nlp_analyzer.detect_concerning_patterns(notes_list)
        
        return jsonify({
            "status": "success",
            "patterns": patterns
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== 5. RECOMMENDATION ENGINE ENDPOINTS =====
@app.route("/api/ml/recommendations/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_ml_recommendations(child_id):
    """Get AI-powered personalized recommendations"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child_data = db.session.execute(
            text("SELECT child_id, name, birth_date FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child_data:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, social as activity_level, ai_risk_level, ai_cluster
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        logs_list = [
            {
                'mood': row[0],
                'sleep_hours': row[1],
                'tantrums': row[2],
                'focus': row[3],
                'activity_level': row[4]
            }
            for row in logs_data
        ]
        
        # Calculate age
        from datetime import date
        today = date.today()
        birth_date = child_data[2]
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Get recommendations
        recommendations = recommendation_engine.generate_recommendations({
            'risk_level': logs_data[0][5] if logs_data else 'medium',
            'psyche_cluster': logs_data[0][6] if logs_data else 'balanced',
            'age': age,
            'recent_logs': logs_list
        })
        
        return jsonify({
            "status": "success",
            "recommendations": recommendations
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/recommendations/contextual/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_contextual_recommendations(child_id):
    """Get context-aware suggestions (morning/afternoon/evening/school/weekend)"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        context = request.args.get("context", "default")
        
        suggestions = recommendation_engine.get_contextual_suggestions({}, context)
        
        return jsonify({
            "status": "success",
            "context": context,
            "suggestions": suggestions
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== 6. EXPLAINABILITY ENDPOINTS =====
@app.route("/api/ml/explain/summary/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_simple_summary(child_id):
    """Get a simple one-line summary of child's status"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child = db.session.execute(
            text("SELECT * FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child:
            return jsonify({"error": "Access denied"}), 403
        
        # Get current predictions (from recent logs)
        latest_log = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, ai_risk_level
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 1
            """), {"cid": child_id}
        ).fetchone()
        
        if not latest_log:
            return jsonify({
                "status": "info",
                "summary": "No behavior logs yet. Start tracking to get insights."
            }), 200
        
        all_predictions = {
            'mood': {'predicted_mood': latest_log[0]},
            'risk': {'risk_level': latest_log[4]},
            'anomaly': {'is_anomaly': False}
        }
        
        summary = explainer.create_simple_summary(all_predictions)
        
        return jsonify({
            "status": "success",
            "summary": summary
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml/explain/report/<int:child_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_parent_report(child_id):
    """Get comprehensive parent-friendly report"""
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200
    
    try:
        current_user = get_jwt_identity()
        user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email"), {"email": current_user}
        ).fetchone()
        
        child_data = db.session.execute(
            text("SELECT child_id, name, birth_date FROM children WHERE child_id = :cid AND user_id = :uid"),
            {"cid": child_id, "uid": user[0]}
        ).fetchone()
        
        if not child_data:
            return jsonify({"error": "Access denied"}), 403
        
        # Get recent logs
        logs_data = db.session.execute(
            text("""
                SELECT mood, sleep_hours, tantrums, focus, ai_risk_level
                FROM behavior_logs 
                WHERE child_id = :cid 
                ORDER BY log_date DESC LIMIT 30
            """), {"cid": child_id}
        ).fetchall()
        
        if not logs_data:
            return jsonify({
                "status": "info",
                "message": "Insufficient data for report. Add more behavior logs."
            }), 200
        
        all_predictions = {
            'risk': {'risk_level': logs_data[0][4]},
            'mood': {'predicted_mood_category': 'Neutral'},
            'anomaly': {'is_anomaly': False},
            'recommendations': []
        }
        
        report = explainer.generate_parent_report(
            {'name': child_data[1]},
            all_predictions
        )
        
        return jsonify({
            "status": "success",
            "report": report
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== END OF ML PIPELINE ENDPOINTS ==========


if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            print("[OK] Database connected successfully!")
            print("[OK] AI Behavior module tables created!")
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
    
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"[INFO] Flask server starting on port {port}")
    print("[NEW] Behavior tracking: POST /behavior/log/<child_id>")
    print("[NEW] AI Insights: GET /behavior/<child_id>/insights")
    print("[INFO] Inventory: /inventory")
    print("[INFO] Funds: /funds")
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
