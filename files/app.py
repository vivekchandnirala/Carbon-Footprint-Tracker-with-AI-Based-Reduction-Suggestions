"""
Carbon Footprint Tracker — Flask Backend
==========================================
Endpoints:
  POST /api/predict      → CO2 prediction + recommendations
  GET  /api/health       → server status check
  POST /api/register     → user registration
  POST /api/login        → user login (JWT)
  GET  /api/history/<id> → user's past submissions

Run karo: python app.py
Port     : http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import sqlite3
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)   # React frontend allow karne ke liye

SECRET_KEY  = "carbon_tracker_secret_2025"
DB_FILE     = "carbon_tracker.db"
MODEL_FILE  = "carbon_model.pkl"
LE_FILE     = "label_encoders.pkl"
FEAT_FILE   = "feature_cols.pkl"

CATEGORICAL_COLS = [
    "body_type", "diet", "transport", "energy_source",
    "social_activity", "home_size", "recycles", "heating_cooling_usage"
]

# ── Load ML model ─────────────────────────────────────────────────────────────
def load_model():
    if not os.path.exists(MODEL_FILE):
        return None, None, None
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    with open(LE_FILE, "rb") as f:
        label_encoders = pickle.load(f)
    with open(FEAT_FILE, "rb") as f:
        feature_cols = pickle.load(f)
    return model, label_encoders, feature_cols

model, label_encoders, feature_cols = load_model()

# ── Database setup ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS emissions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER,
            co2_predicted REAL,
            level         TEXT,
            input_data    TEXT,
            created       TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── Helper functions ──────────────────────────────────────────────────────────
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def make_token(user_id, email):
    payload = {
        "user_id": user_id,
        "email":   email,
        "exp":     datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None

def get_recommendations(user_data, predicted_co2):
    tips = []
    INDIA_AVG = 1800

    if predicted_co2 > INDIA_AVG * 2:
        tips.append({"category": "Overall", "priority": "HIGH",
                     "tip": "Tera carbon footprint India average se 2x zyada hai!", "impact_kg": 0})

    if user_data.get("transport") == "private car":
        tips.append({"category": "Transport", "priority": "HIGH",
                     "tip": "Public transport ya carpooling use karo — 600 kg/year bach sakta hai.", "impact_kg": 600})

    if user_data.get("flights_per_year", 0) > 4:
        saving = (user_data["flights_per_year"] - 2) * 900
        tips.append({"category": "Transport", "priority": "HIGH",
                     "tip": f"Flights kam karo. {user_data['flights_per_year']} flights = ~{user_data['flights_per_year']*900} kg CO2/year.", "impact_kg": saving})

    if user_data.get("diet") == "omnivore":
        tips.append({"category": "Food", "priority": "MEDIUM",
                     "tip": "Meatless Monday try karo — ~400 kg/year bacha sakte ho.", "impact_kg": 400})

    if user_data.get("energy_source") in ["coal", "natural gas"]:
        tips.append({"category": "Energy", "priority": "HIGH",
                     "tip": "Renewable energy ya solar panels consider karo — ~1200 kg/year impact.", "impact_kg": 1200})

    if user_data.get("recycles") in ["never", "rarely"]:
        tips.append({"category": "Waste", "priority": "LOW",
                     "tip": "Recycling shuru karo — paper, plastic, glass segregate karo.", "impact_kg": 150})

    if not tips:
        tips.append({"category": "General", "priority": "LOW",
                     "tip": "Great job! Tera footprint accha hai. Tree plantation mein contribute karo.", "impact_kg": 0})

    return sorted(tips, key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["priority"]])

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status":       "ok",
        "model_loaded": model is not None,
        "message":      "Carbon Footprint Tracker API is running 🌱"
    })


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name  = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    pwd   = data.get("password", "")

    if not name or not email or not pwd:
        return jsonify({"error": "Sab fields required hain"}), 400
    if len(pwd) < 6:
        return jsonify({"error": "Password kam se kam 6 characters ka hona chahiye"}), 400

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",
                  (name, email, hash_password(pwd)))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        token = make_token(user_id, email)
        return jsonify({"message": "Registration successful!", "token": token, "name": name}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Yeh email already registered hai"}), 409


@app.route("/api/login", methods=["POST"])
def login():
    data  = request.get_json()
    email = data.get("email", "").strip().lower()
    pwd   = data.get("password", "")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name FROM users WHERE email=? AND password=?",
              (email, hash_password(pwd)))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Email ya password galat hai"}), 401

    token = make_token(user[0], email)
    return jsonify({"message": "Login successful!", "token": token, "name": user[1]}), 200


@app.route("/api/predict", methods=["POST"])
def predict():
    """Main endpoint: user data → CO2 prediction + recommendations."""
    if model is None:
        return jsonify({"error": "Model load nahi hua. Pehle ml_model.py run karo!"}), 500

    # Optional auth
    token_data = None
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token_data = verify_token(auth[7:])

    data = request.get_json()

    # Validate required fields
    required = ["diet", "transport", "energy_source", "flights_per_year",
                "recycles", "home_size", "new_clothes_monthly",
                "internet_hours_daily", "monthly_grocery_inr",
                "vehicle_monthly_km", "heating_cooling_usage",
                "body_type", "social_activity"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Field missing: {field}"}), 400

    try:
        row = {k: v for k, v in data.items()}
        for col in CATEGORICAL_COLS:
            if col in row:
                row[col] = label_encoders[col].transform([row[col]])[0]

        input_df = pd.DataFrame([row])[feature_cols]
        predicted = float(model.predict(input_df)[0])

        if predicted < 1800:
            level = "Low"
        elif predicted < 3500:
            level = "Medium"
        else:
            level = "High"

        recs = get_recommendations(data, predicted)

        # Save to DB if user is logged in
        if token_data:
            import json
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute(
                "INSERT INTO emissions (user_id, co2_predicted, level, input_data) VALUES (?,?,?,?)",
                (token_data["user_id"], predicted, level, json.dumps(data))
            )
            conn.commit()
            conn.close()

        return jsonify({
            "predicted_co2_kg_year": round(predicted, 2),
            "level":                 level,
            "india_average_kg":      1800,
            "recommendations":       recs,
            "saved":                 token_data is not None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history/<int:user_id>", methods=["GET"])
def history(user_id):
    auth = request.headers.get("Authorization", "")
    token_data = verify_token(auth[7:]) if auth.startswith("Bearer ") else None

    if not token_data or token_data["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT co2_predicted, level, created FROM emissions WHERE user_id=? ORDER BY created DESC LIMIT 20",
              (user_id,))
    rows = c.fetchall()
    conn.close()

    history_data = [{"co2": r[0], "level": r[1], "date": r[2]} for r in rows]
    return jsonify({"history": history_data})


if __name__ == "__main__":
    print("🌱 Carbon Footprint Tracker API starting...")
    print("📍 URL: http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /api/health")
    print("   POST /api/register")
    print("   POST /api/login")
    print("   POST /api/predict")
    print("   GET  /api/history/<user_id>")
    app.run(debug=True, port=8080)
