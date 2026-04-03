# 🌱 Carbon Footprint Tracker with AI-Based Reduction Suggestions

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange?style=for-the-badge&logo=scikit-learn)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Auth-red?style=for-the-badge)

**A smart web application that tracks your carbon emissions using AI and gives personalized suggestions to reduce your environmental impact.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [How It Works](#-how-it-works) • [Setup Guide](#-setup-guide) • [API Docs](#-api-endpoints) • [Team](#-team)

</div>

---

## 📌 What is this project?

Carbon Footprint Tracker is a full-stack web application built as a Capstone Project for **CSE-339 at Lovely Professional University (2025)**.

The system collects data about a user's daily lifestyle — such as diet, transportation, energy usage, and shopping habits — and uses a **Random Forest Machine Learning model** to calculate how much CO₂ (in kg/year) that person is producing. Based on this score, an **AI-powered Recommendation Engine** provides personalized, actionable tips to help reduce their carbon footprint.

---

## ✨ Features

- 🔐 **User Authentication** — Register & Login with JWT-secured sessions
- 📋 **Smart Input Form** — 13 lifestyle parameters across 5 categories
- 🤖 **ML Prediction** — Random Forest Regressor with 92.6% accuracy
- 📊 **Visual Dashboard** — Gauge chart, progress bar, comparison with India average
- 💡 **Personalized Tips** — Rule-based recommendation engine with CO₂ impact estimates
- 📈 **History Tracking** — Past results saved per user in database
- 🌍 **India Average Comparison** — See how you compare to the 1,800 kg/year national average

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React.js | UI components, routing, state management |
| Styling | CSS3 | Custom green-themed design system |
| HTTP Client | Axios | API calls from frontend to backend |
| Backend | Flask (Python) | REST API server |
| ML Model | scikit-learn | Random Forest Regressor for CO₂ prediction |
| Database | SQLite | User accounts and emission history storage |
| Authentication | JWT (PyJWT) | Secure token-based login sessions |
| Data Processing | Pandas, NumPy | Dataset generation and preprocessing |

---

## 🏗 Project Structure

```
Carbon-Footprint-Tracker/
│
├── files/                               ← Backend (Python + ML)
│   ├── carbon_dataset_generator.py      Step 1: Generates training dataset (1000 rows)
│   ├── ml_model.py                      Step 2: Trains the Random Forest model
│   ├── app.py                           Step 3: Flask REST API server
│   ├── requirements.txt                 Python dependencies
│   ├── carbon_footprint_dataset.csv     Generated training data
│   ├── carbon_model.pkl                 Saved trained ML model
│   ├── label_encoders.pkl               Saved label encoders
│   └── carbon_tracker.db               SQLite database (auto-created on first run)
│
└── frontend/                            ← Frontend (React)
    └── src/
        ├── App.js                       Main router
        ├── index.css                    Global styles
        ├── pages/
        │   ├── Login.js                 Login page
        │   ├── Register.js              Registration page
        │   ├── Dashboard.js             Carbon footprint input form
        │   └── Result.js                CO₂ score + recommendations
        └── components/
            ├── Navbar.js                Top navigation bar
            └── RecommendationCard.js    Individual tip card component
```

---

## 🔄 How It Works

### Step 1 — Data Collection
The user fills out a form with 13 lifestyle parameters:

| Category | Parameters |
|----------|-----------|
| Personal | Body type, home size |
| Food | Diet type, monthly grocery spend |
| Transport | Main transport mode, monthly km driven, flights per year |
| Energy | Energy source type, AC/heater usage frequency |
| Lifestyle | Recycling habits, social activity, clothes bought/month, internet hours/day |

### Step 2 — ML Prediction
The form data is sent via HTTP POST to the Flask backend. The **Random Forest Regressor** (100 decision trees) predicts the user's annual CO₂ footprint in kg/year.

```
User Data → Label Encoding → Random Forest (100 trees) → Average of all trees → CO₂ Score
```

**Model Performance:**
- R² Score: **0.9264** (92.6% accuracy)
- Mean Absolute Error: 648 kg CO₂/year
- Most important feature: `flights_per_year` (78.7% importance)

### Step 3 — Recommendations
A **rule-based engine** inside `app.py` reads the user's inputs and generates prioritized suggestions:

```
if transport == "private car"  →  suggest carpooling        →  saves ~600 kg/year
if flights_per_year > 4        →  suggest reducing flights   →  saves ~2700 kg/year
if energy_source == "coal"     →  suggest renewable energy   →  saves ~1200 kg/year
if diet == "omnivore"          →  suggest Meatless Monday    →  saves ~400 kg/year
if recycles == "never"         →  suggest start recycling    →  saves ~150 kg/year
```

Each tip shows: category, priority level (HIGH / MEDIUM / LOW), the suggestion text, and estimated annual CO₂ saved.

### Step 4 — Result Display
The React frontend renders:
- A **gauge chart** showing the CO₂ level visually
- A **level badge**: Low 🟢 / Medium 🟡 / High 🔴
- **Comparison bar** against India's average (1,800 kg/year)
- Daily and monthly CO₂ breakdown stats
- All personalized recommendation cards with impact estimates
- Total potential saving if all tips are followed

---

## 🔐 Authentication Flow

This project uses **JWT (JSON Web Token)** — industry-standard secure token-based authentication.

```
1. User registers  →  password hashed with SHA-256  →  stored in SQLite
2. User logs in    →  credentials verified  →  JWT token generated (valid 7 days)
3. Token stored    →  saved in browser localStorage
4. API calls       →  token sent in Authorization header: "Bearer <token>"
5. Backend         →  verifies token signature  →  allows or denies the request
```

**Security measures implemented:**
- Passwords hashed with `SHA-256` before storing — never saved as plain text
- JWT tokens signed with a `SECRET_KEY` — tamper-proof
- Token expiry enforced at 7 days — automatic logout after expiry
- Flask-CORS configured — controls which origins can access the API

---

## 🔗 How Frontend and Backend Are Connected

The frontend (React on **port 3000**) talks to the backend (Flask on **port 8080**) using **Axios** HTTP requests.

```javascript
// Example: Dashboard.js sends form data to Flask backend
const response = await axios.post('http://localhost:8080/api/predict', formData, {
  headers: { Authorization: `Bearer ${token}` }
});

// Flask returns JSON → React renders it on the Result page
```

This is a clean **separation of concerns** — React handles all UI rendering, Flask handles all business logic and database operations. They communicate only through well-defined API endpoints.

---

## 🗃 Database Design

**SQLite** is used — a lightweight, file-based database. No separate database server is needed. The `carbon_tracker.db` file is automatically created when `app.py` runs for the first time.

```sql
-- Stores registered users
CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    email     TEXT UNIQUE NOT NULL,
    password  TEXT NOT NULL,            -- SHA-256 hashed, never plain text
    created   TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Stores each carbon footprint calculation per user
CREATE TABLE emissions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,              -- Foreign key linking to users table
    co2_predicted REAL,                 -- Predicted CO₂ value in kg/year
    level         TEXT,                 -- "Low", "Medium", or "High"
    input_data    TEXT,                 -- Full JSON of all form inputs
    created       TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm

### Backend Setup

```bash
# Step 1: Navigate to backend folder
cd files

# Step 2: Install all Python dependencies
pip3 install -r requirements.txt

# Step 3: Generate the training dataset
python3 carbon_dataset_generator.py
# Output: carbon_footprint_dataset.csv (1000 rows)

# Step 4: Train the ML model
python3 ml_model.py
# Output: carbon_model.pkl (saved trained model)

# Step 5: Start the Flask API server
python3 app.py
# Server starts at: http://localhost:8080
```

### Frontend Setup

```bash
# Step 1: Navigate to frontend folder
cd frontend

# Step 2: Install Node.js dependencies
npm install axios recharts react-router-dom

# Step 3: Start the React development server
npm start
# App opens at: http://localhost:3000
```

> **Important:** Both servers must be running at the same time. Use two separate terminal windows — one for Flask, one for React.

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:-------------:|
| GET | `/api/health` | Server status check | No |
| POST | `/api/register` | Create a new user account | No |
| POST | `/api/login` | Login and receive JWT token | No |
| POST | `/api/predict` | Predict CO₂ score and get recommendations | Optional |
| GET | `/api/history/<user_id>` | Fetch user's past calculations | Yes |

### Sample Request — `/api/predict`

```json
POST http://localhost:8080/api/predict
Content-Type: application/json

{
  "body_type": "normal",
  "diet": "omnivore",
  "transport": "private car",
  "vehicle_monthly_km": 30,
  "energy_source": "coal",
  "monthly_grocery_inr": 4000,
  "social_activity": "sometimes",
  "flights_per_year": 5,
  "home_size": "medium",
  "recycles": "rarely",
  "heating_cooling_usage": "often",
  "new_clothes_monthly": 6,
  "internet_hours_daily": 7
}
```

### Sample Response

```json
{
  "predicted_co2_kg_year": 11033.05,
  "level": "High",
  "india_average_kg": 1800,
  "recommendations": [
    {
      "category": "Transport",
      "priority": "HIGH",
      "tip": "Switch to public transport or carpooling — saves ~600 kg CO₂/year",
      "impact_kg": 600
    },
    {
      "category": "Energy",
      "priority": "HIGH",
      "tip": "Switch to renewable energy or solar panels — saves ~1200 kg CO₂/year",
      "impact_kg": 1200
    }
  ]
}
```

---

## 📊 Dataset Information

The training dataset was synthetically generated using real-world carbon emission factors from environmental research papers and India-specific data.

- **Total records:** 1,000
- **Input features:** 13 columns
- **Target column:** `carbon_footprint_kg_year` (continuous — this is a regression problem)
- **CO₂ value range:** ~1,500 to ~16,000 kg/year

**Emission factors used (based on research):**

| Emission Source | CO₂ per Year |
|----------------|-------------|
| Vegan diet | ~500 kg |
| Vegetarian diet | ~900 kg |
| Omnivore diet | ~2,000 kg |
| Walking / cycling | 0 kg |
| Public transport | ~600 kg |
| Private car | ~2,500 kg base |
| One flight | ~900 kg |
| Renewable energy | ~200 kg |
| Coal / grid energy | ~2,200 kg |

---

## 👥 Team

| Name | Roll Number | Email |
|------|------------|-------|
| Vivek Chand Nirala | 12216577 | vivekchandnirala28@gmail.com |
| Priyanka Kumari | 12219581 | priyanka722004@gmail.com |

**Project Guide:** Dr. Manjot Kaur, Assistant Professor
**Institution:** Lovely Professional University, Punjab, India
**Course:** CSE-339 Capstone Project (August – November 2025)

---

## 📄 License

This project was developed for academic purposes at Lovely Professional University. All rights reserved by the contributors.

---

<div align="center">

Made with 💚 to help the planet — one carbon footprint at a time.

⭐ Star this repo if you found it helpful!

</div>
