# 🌱 Carbon Footprint Tracker — Setup Guide

## Project Structure

```
carbon-footprint-tracker/
│
├── carbon_dataset_generator.py   ← Step 1: Dataset banao
├── ml_model.py                   ← Step 2: ML Model train karo
├── app.py                        ← Step 3: Backend chalao
├── requirements.txt              ← Dependencies
└── (frontend/ folder alag se)    ← Step 4: React Dashboard
```

---

## ⚙️ Setup Steps (Ek Ek Karo)

### Step 0: Dependencies install karo

```bash
pip install -r requirements.txt
```

### Step 1: Dataset generate karo

```bash
python carbon_dataset_generator.py
```

✅ Output: `carbon_footprint_dataset.csv` (1000 rows)

### Step 2: ML Model train karo

```bash
python ml_model.py
```

✅ Output: `carbon_model.pkl`, `label_encoders.pkl`
📊 Model performance aur sample predictions dikhega

### Step 3: Backend server start karo

```bash
python app.py
```

✅ Server: http://localhost:5000

---

## 🔌 API Test karo (Postman ya curl se)

### Health check

```
GET http://localhost:5000/api/health
```

### Register

```json
POST http://localhost:5000/api/register
{
  "name": "Vikash",
  "email": "vikash@example.com",
  "password": "password123"
}
```

### Predict CO2

```json
POST http://localhost:5000/api/predict
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

---

## 🤖 Algorithm Explanation (Report ke liye)

**Random Forest Regressor** use kiya kyunki:

- Multiple decision trees → zyada accurate predictions
- Categorical + numerical dono types handle karta hai
- Feature importance deta hai (kaunsi cheez zyada CO2 deta hai)
- Overfitting kam hoti hai

**Rule-based Recommendation Engine:**

- If transport == car → carpooling suggest karo
- If flights > 4 → reduce flights suggest karo
- If energy == coal → renewable suggest karo
- Priority: HIGH > MEDIUM > LOW

---

## 📊 Dataset Columns

| Column                       | Type          | Description                           |
| ---------------------------- | ------------- | ------------------------------------- |
| body_type                    | Categorical   | underweight/normal/overweight/obese   |
| diet                         | Categorical   | vegan/vegetarian/pescatarian/omnivore |
| transport                    | Categorical   | walk/public transport/car/motorbike   |
| vehicle_monthly_km           | Numerical     | Monthly km in private vehicle         |
| energy_source                | Categorical   | renewable/gas/coal/mixed              |
| monthly_grocery_inr          | Numerical     | Monthly grocery spend (INR)           |
| social_activity              | Categorical   | rarely/sometimes/often/always         |
| flights_per_year             | Numerical     | Number of flights per year            |
| home_size                    | Categorical   | small/medium/large                    |
| recycles                     | Categorical   | never/rarely/sometimes/often/always   |
| heating_cooling_usage        | Categorical   | AC/heater usage frequency             |
| new_clothes_monthly          | Numerical     | Clothes bought per month              |
| internet_hours_daily         | Numerical     | Daily internet usage hours            |
| **carbon_footprint_kg_year** | **Numerical** | **TARGET: CO2 in kg/year**            |

---

## 👥 Team

- Amanjyot Kaur (12201523)
- Priyanka Kumari (12219581)
- Vikash Kumar Gupta (12215449)
- Vivek Chand Nirala (12216577)

**Guide:** Dr. Manjot Kaur | LPU CSE-339 Capstone (2025)
