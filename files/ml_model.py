"""
Carbon Footprint ML Model
============================
Algorithm : Random Forest Regressor (prediction)
            Rule-based Engine (recommendations)

Run karo  : python ml_model.py
Outputs   : carbon_model.pkl, label_encoders.pkl
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# ── Step 1: Load dataset ──────────────────────────────────────────────────────
CSV_FILE = "carbon_footprint_dataset.csv"

if not os.path.exists(CSV_FILE):
    print("❌ Dataset nahi mili! Pehle run karo: python carbon_dataset_generator.py")
    exit()

df = pd.read_csv(CSV_FILE)
print(f"✅ Dataset load hui: {df.shape[0]} rows, {df.shape[1]} columns")

# ── Step 2: Preprocessing ────────────────────────────────────────────────────
CATEGORICAL_COLS = [
    "body_type", "diet", "transport", "energy_source",
    "social_activity", "home_size", "recycles",
    "heating_cooling_usage"
]
TARGET_COL = "carbon_footprint_kg_year"

# Label Encoding for categorical columns
label_encoders = {}
df_encoded = df.copy()

for col in CATEGORICAL_COLS:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le

FEATURE_COLS = [
    "body_type", "diet", "transport", "vehicle_monthly_km",
    "energy_source", "monthly_grocery_inr", "social_activity",
    "flights_per_year", "home_size", "recycles",
    "heating_cooling_usage", "new_clothes_monthly", "internet_hours_daily"
]

X = df_encoded[FEATURE_COLS]
y = df_encoded[TARGET_COL]

# ── Step 3: Train-Test Split ──────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n📊 Train size: {len(X_train)}, Test size: {len(X_test)}")

# ── Step 4: Train Random Forest ───────────────────────────────────────────────
print("\n🌲 Random Forest model train ho raha hai...")
model = RandomForestRegressor(
    n_estimators=100,   # 100 decision trees
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1           # use all CPU cores
)
model.fit(X_train, y_train)
print("✅ Model trained!")

# ── Step 5: Evaluate ──────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"\n📈 Model Performance:")
print(f"   MAE (Mean Absolute Error) : {mae:.2f} kg CO2/year")
print(f"   R² Score                  : {r2:.4f}  (1.0 = perfect)")

# Feature importance
feat_imp = pd.Series(model.feature_importances_, index=FEATURE_COLS)
feat_imp = feat_imp.sort_values(ascending=False)
print(f"\n🔍 Top 5 sabse important features:")
for feat, imp in feat_imp.head(5).items():
    print(f"   {feat:<30} {imp*100:.1f}%")

# ── Step 6: Save model ────────────────────────────────────────────────────────
with open("carbon_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)
with open("feature_cols.pkl", "wb") as f:
    pickle.dump(FEATURE_COLS, f)

print(f"\n💾 Model save ho gaya: carbon_model.pkl")

# ── Step 7: Recommendation Engine ────────────────────────────────────────────
def get_recommendations(user_data: dict, predicted_co2: float) -> list:
    """
    Rule-based recommendation engine.
    Input  : user_data dict + predicted CO2 score
    Output : list of personalized suggestions
    """
    tips = []

    # Average Indian per capita CO2 ~ 1800 kg/year
    INDIA_AVERAGE = 1800

    if predicted_co2 > INDIA_AVERAGE * 2:
        tips.append({
            "category": "Overall",
            "priority": "HIGH",
            "tip": "Tera carbon footprint bahut zyada hai! Turant kuch steps lene zaruri hain.",
            "impact_kg": None
        })

    # Transport
    if user_data.get("transport") == "private car":
        tips.append({
            "category": "Transport",
            "priority": "HIGH",
            "tip": "Private car ki jagah public transport ya carpooling use karo. "
                   "Week mein 3 din bhi karoge toh ~600 kg CO2/year bachega.",
            "impact_kg": 600
        })
    if user_data.get("flights_per_year", 0) > 4:
        tips.append({
            "category": "Transport",
            "priority": "HIGH",
            "tip": f"Tu {user_data['flights_per_year']} flights le raha hai. "
                   "Kum karo ya carbon offset karo. Ek flight ~900 kg CO2 deta hai.",
            "impact_kg": (user_data["flights_per_year"] - 2) * 900
        })

    # Diet
    if user_data.get("diet") == "omnivore":
        tips.append({
            "category": "Food",
            "priority": "MEDIUM",
            "tip": "Hafte mein 2-3 din meatless meals try karo (Meatless Monday). "
                   "~400 kg CO2/year bacha sakta hai.",
            "impact_kg": 400
        })

    # Energy
    if user_data.get("energy_source") in ["coal", "natural gas"]:
        tips.append({
            "category": "Energy",
            "priority": "HIGH",
            "tip": "Renewable energy (solar panels ya green energy provider) switch karo. "
                   "~1200 kg CO2/year tak bacha sakte ho.",
            "impact_kg": 1200
        })

    # Recycling
    if user_data.get("recycles") in ["never", "rarely"]:
        tips.append({
            "category": "Waste",
            "priority": "LOW",
            "tip": "Recycling shuru karo — paper, plastic, glass alag karo. "
                   "Ghar par compost banana try karo.",
            "impact_kg": 150
        })

    # Clothes
    if user_data.get("new_clothes_monthly", 0) > 5:
        tips.append({
            "category": "Lifestyle",
            "priority": "MEDIUM",
            "tip": "Fast fashion reduce karo. Thrifting ya kapde exchange programs try karo. "
                   "Ek kapda ~30 kg CO2 deta hai manufacturing mein.",
            "impact_kg": user_data["new_clothes_monthly"] * 25
        })

    # Grocery
    if user_data.get("monthly_grocery_inr", 0) > 5000:
        tips.append({
            "category": "Food",
            "priority": "LOW",
            "tip": "Local aur seasonal produce kharido. Food waste kum karo — "
                   "jo banana hai utna hi grocery lo.",
            "impact_kg": 100
        })

    if not tips:
        tips.append({
            "category": "General",
            "priority": "LOW",
            "tip": "Bahut accha! Tera footprint kaafi low hai. "
                   "Tree plantation aur community awareness mein contribute karo.",
            "impact_kg": 0
        })

    return sorted(tips, key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["priority"]])


# ── Step 8: Test with sample user ────────────────────────────────────────────
def predict_and_recommend(user_input: dict) -> dict:
    """Full pipeline: encode → predict → recommend."""
    with open("carbon_model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        loaded_le = pickle.load(f)
    with open("feature_cols.pkl", "rb") as f:
        loaded_features = pickle.load(f)

    row = user_input.copy()
    for col in CATEGORICAL_COLS:
        if col in row:
            row[col] = loaded_le[col].transform([row[col]])[0]

    input_df = pd.DataFrame([row])[loaded_features]
    predicted = loaded_model.predict(input_df)[0]

    level = "Low 🟢" if predicted < 1800 else ("Medium 🟡" if predicted < 3500 else "High 🔴")

    return {
        "predicted_co2_kg_year": round(predicted, 2),
        "level": level,
        "india_average_kg": 1800,
        "recommendations": get_recommendations(user_input, predicted)
    }


# ── Demo run ──────────────────────────────────────────────────────────────────
sample_user = {
    "body_type":             "normal",
    "diet":                  "omnivore",
    "transport":             "private car",
    "vehicle_monthly_km":    30,
    "energy_source":         "coal",
    "monthly_grocery_inr":   4000,
    "social_activity":       "sometimes",
    "flights_per_year":      5,
    "home_size":             "medium",
    "recycles":              "rarely",
    "heating_cooling_usage": "often",
    "new_clothes_monthly":   6,
    "internet_hours_daily":  7,
}

print("\n" + "="*55)
print("🧪 SAMPLE USER TEST")
print("="*55)
result = predict_and_recommend(sample_user)
print(f"📍 Predicted CO2 : {result['predicted_co2_kg_year']} kg/year")
print(f"📊 Level         : {result['level']}")
print(f"🇮🇳 India average : {result['india_average_kg']} kg/year")
print(f"\n💡 Recommendations ({len(result['recommendations'])} tips):")
for i, rec in enumerate(result["recommendations"], 1):
    print(f"\n  {i}. [{rec['priority']}] {rec['category']}")
    print(f"     {rec['tip']}")
    if rec["impact_kg"]:
        print(f"     💚 Impact: ~{rec['impact_kg']} kg CO2 bacha sakte ho/year")
print("\n✅ Model ready! Ab Flask app run karo: python app.py")
