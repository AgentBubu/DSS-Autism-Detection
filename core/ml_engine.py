import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

MODEL_FILE = os.path.join('models', 'random_forest.pkl')

def get_model():
    if os.path.exists(MODEL_FILE):
        try: return joblib.load(MODEL_FILE)
        except: pass 

    # Re-train logic (Same as before)
    print("Training new Random Forest Model...")
    X = np.random.rand(1000, 5)
    y = []
    for row in X:
        max_idx = np.argmax(row)
        if np.mean(row) < 0.25: label = "Pendampingan Reguler"
        elif max_idx == 0: label = "Terapi Integrasi Sensorik"
        elif max_idx == 1: label = "Pelatihan Keterampilan Sosial"
        elif max_idx == 2: label = "Terapi Wicara Pragmatik"
        elif max_idx == 3: label = "DIR (Floortime)"
        else: label = "Metode TEACCH"
        y.append(label)
        
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    if not os.path.exists('models'): os.makedirs('models')
    joblib.dump(clf, MODEL_FILE)
    return clf

def predict_with_details(features):
    clf = get_model()
    
    # Input Vector
    input_vector = [[
        features.get('C1', 0),
        features.get('C2', 0),
        features.get('C3', 0),
        features.get('C4', 0),
        features.get('C5', 0)
    ]]
    
    # 1. Get the Winner
    prediction = clf.predict(input_vector)[0]
    
    # 2. Get Probabilities (The "Calculation" part)
    # This returns an array like [0.1, 0.8, 0.05, ...]
    probs = clf.predict_proba(input_vector)[0]
    class_labels = clf.classes_
    
    # Zip them together and sort by highest probability
    detailed_probs = []
    for label, prob in zip(class_labels, probs):
        detailed_probs.append({
            "label": label,
            "probability": round(prob * 100, 1) # Convert to percentage
        })
    
    # Sort: Highest confidence first
    detailed_probs.sort(key=lambda x: x['probability'], reverse=True)
    
    return prediction, detailed_probs