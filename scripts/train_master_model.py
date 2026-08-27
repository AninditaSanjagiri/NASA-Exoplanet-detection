import os
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("🚀 Loading REAL NASA Kepler Dataset (cumulative.csv)...")

# 1. Load the dataset
df = pd.read_csv('data/cumulative.csv')

# 2. Filter labels: Keep only definitive CONFIRMED and FALSE POSITIVE
# (We drop 'CANDIDATE' because those are unverified/unlabeled)
df = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()
df['label'] = df['koi_disposition'].apply(lambda x: 1 if x == 'CONFIRMED' else 0)

# 3. Select the core physical features matching our Lightkurve pipeline
# - koi_period: Orbital period in days
# - koi_depth: Transit depth (converted from ppm to fractional depth)
# - koi_duration: Transit duration in hours
# - koi_model_snr: Signal-to-Noise Ratio
# - koi_prad: Planetary radius (Earth radii)

df['fractional_depth'] = df['koi_depth'] / 1e6  # Convert ppm to relative fraction

feature_cols = ['koi_period', 'fractional_depth', 'koi_duration', 'koi_model_snr']

# Drop any rows with missing feature values
df_clean = df.dropna(subset=feature_cols + ['label']).copy()

X = df_clean[feature_cols]
y = df_clean['label']

print(f"📊 Filtered down to {len(df_clean)} verified NASA observations.")
print(f"   - Confirmed Planets: {sum(y == 1)}")
print(f"   - False Positives:   {sum(y == 0)}")

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Train XGBoost Classifier
print("\n🧠 Training XGBoost Classifier on NASA telemetry...")
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss'
)

model.fit(X_train, y_train)

# 6. Model Evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("-" * 45)
print(f"✅ Accuracy on Real NASA Test Data: {acc * 100:.2f}%")
print("-" * 45)
print(classification_report(y_test, y_pred, target_names=["False Positive", "Confirmed Planet"]))

# 7. Export Model Artifact
os.makedirs("models", exist_ok=True)
export_path = "models/xgboost_nasa_model.pkl"
joblib.dump(model, export_path)

print(f"💾 Model successfully saved to: {export_path}")