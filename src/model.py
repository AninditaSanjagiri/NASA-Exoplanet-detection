import os
import pandas as pd
from xgboost import XGBClassifier

def train_or_load_model(dataset_path="data/tess_prototype_dataset.csv"):
    """
    Trains the XGBoost model on the prototype dataset.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at '{dataset_path}'. Please move your CSV into the 'data/' folder.")
    
    df = pd.read_csv(dataset_path)
    
    feature_cols = ['period_days', 'transit_count', 'signal_depth', 'snr', 'odd_even_diff']
    X = df[feature_cols]
    y = df['is_planet']
    
    model = XGBClassifier(eval_metric='logloss', random_state=42)
    model.fit(X, y)
    
    return model


def predict_candidate(model, features_dict):
    """
    Takes the extracted feature dictionary and outputs a prediction + confidence score.
    """
    feature_cols = ['period_days', 'transit_count', 'signal_depth', 'snr', 'odd_even_diff']
    input_df = pd.DataFrame([features_dict])[feature_cols]
    
    prob = model.predict_proba(input_df)[0]
    is_planet_pred = model.predict(input_df)[0]
    
    # Probability of being a planet
    planet_confidence = prob[1] * 100.0
    
    return int(is_planet_pred), round(planet_confidence, 2)