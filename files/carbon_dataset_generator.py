"""
Carbon Footprint Dataset Generator
====================================
Yeh script ek realistic dataset banati hai jisme individual
logon ki daily activities hain aur unka CO2 emission score hai.

Run karo: python carbon_dataset_generator.py
Output:   carbon_footprint_dataset.csv
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

NUM_RECORDS = 1000

# ── Options for categorical columns ──────────────────────────────────────────
body_types      = ["underweight", "normal", "overweight", "obese"]
diet_types      = ["vegan", "vegetarian", "pescatarian", "omnivore"]
transport_types = ["walk/cycle", "public transport", "private car", "motorbike"]
energy_sources  = ["renewable", "natural gas", "coal", "mixed"]
social_activity = ["rarely", "sometimes", "often", "always"]
home_sizes      = ["small", "medium", "large"]
frequency       = ["never", "rarely", "sometimes", "often", "always"]

# ── CO2 contribution weights (kg CO2 per unit or per category) ────────────────
diet_co2 = {
    "vegan":        500,
    "vegetarian":   900,
    "pescatarian": 1400,
    "omnivore":    2000,
}
transport_co2 = {
    "walk/cycle":         0,
    "public transport":  600,
    "motorbike":        1000,
    "private car":      2500,
}
energy_co2 = {
    "renewable":     200,
    "mixed":         800,
    "natural gas":  1400,
    "coal":         2200,
}

def generate_record(i):
    body      = random.choice(body_types)
    diet      = random.choice(diet_types)
    transport = random.choice(transport_types)
    vehicle_km = round(np.random.uniform(0, 50), 1) if transport in ["private car", "motorbike"] else 0
    energy    = random.choice(energy_sources)
    monthly_grocery = round(np.random.uniform(1000, 8000), 0)   # INR
    social    = random.choice(social_activity)
    flights_per_year = random.randint(0, 10)
    home      = random.choice(home_sizes)
    recycles  = random.choice(frequency)
    heating   = random.choice(frequency)          # heater/AC usage
    new_clothes_monthly = random.randint(0, 10)   # items bought
    internet_hours = round(np.random.uniform(1, 12), 1)

    # ── Calculate CO2 score (kg CO2 / year) ──────────────────────────────────
    co2  = diet_co2[diet]
    co2 += transport_co2[transport] + vehicle_km * 15   # 15g CO2 per km
    co2 += energy_co2[energy]
    co2 += flights_per_year * 900                       # ~900 kg per flight
    co2 += monthly_grocery * 0.05                       # food waste estimate
    co2 += new_clothes_monthly * 30                     # fast fashion impact
    co2 += internet_hours * 10                          # server energy
    co2 += {"small": 200, "medium": 500, "large": 900}[home]

    # Recycling reduces footprint
    recycle_discount = {"never": 0, "rarely": 0.02, "sometimes": 0.05,
                        "often": 0.08, "always": 0.12}
    co2 *= (1 - recycle_discount[recycles])

    # Add some noise to make data realistic
    co2 += np.random.normal(0, 150)
    co2 = max(300, round(co2, 2))   # minimum 300 kg/year

    return {
        "id":                    i + 1,
        "body_type":             body,
        "diet":                  diet,
        "transport":             transport,
        "vehicle_monthly_km":    vehicle_km,
        "energy_source":         energy,
        "monthly_grocery_inr":   monthly_grocery,
        "social_activity":       social,
        "flights_per_year":      flights_per_year,
        "home_size":             home,
        "recycles":              recycles,
        "heating_cooling_usage": heating,
        "new_clothes_monthly":   new_clothes_monthly,
        "internet_hours_daily":  internet_hours,
        "carbon_footprint_kg_year": co2,   # TARGET VARIABLE
    }

# ── Generate dataset ─────────────────────────────────────────────────────────
records = [generate_record(i) for i in range(NUM_RECORDS)]
df = pd.DataFrame(records)

df.to_csv("carbon_footprint_dataset.csv", index=False)
print(f"✅ Dataset banaya! Shape: {df.shape}")
print(f"\n📊 Carbon Footprint Stats:")
print(f"   Min  : {df['carbon_footprint_kg_year'].min():.0f} kg/year")
print(f"   Max  : {df['carbon_footprint_kg_year'].max():.0f} kg/year")
print(f"   Mean : {df['carbon_footprint_kg_year'].mean():.0f} kg/year")
print(f"\n📁 File saved: carbon_footprint_dataset.csv")
print(f"\nPehli 3 rows:")
print(df.head(3).to_string(index=False))
