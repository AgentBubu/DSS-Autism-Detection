import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

MODEL_FILE = os.path.join('models', 'random_forest.pkl')

def get_model():
    # Attempt to load model
    if os.path.exists(MODEL_FILE):
        try:
            return joblib.load(MODEL_FILE)
        except:
            pass 

    print("Training new Random Forest Model...")
    
    # 1. Create dummy data [C1, C2, C3, C4, C5]
    X = np.random.rand(1000, 5)
    y = []
    
    # 2. Logic to map Symptoms -> Program Name
    # IMPORTANT: These strings must match keys in program_data.py EXACTLY
    for row in X:
        max_idx = np.argmax(row)
        
        # If scores are generally low, suggest regular support
        if np.mean(row) < 0.25:
            label = "Pendampingan Reguler"
        elif max_idx == 0: # C1 Highest
            label = "Terapi Integrasi Sensorik"
        elif max_idx == 1: # C2 Highest
            label = "Pelatihan Keterampilan Sosial"
        elif max_idx == 2: # C3 Highest
            label = "Terapi Wicara Pragmatik"
        elif max_idx == 3: # C4 Highest
            label = "DIR (Floortime)"
        else:              # C5 Highest
            label = "Metode TEACCH"
            
        y.append(label)
        
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(clf, MODEL_FILE)
    
    return clf

def predict_recommendation(features):
    clf = get_model()
    # Order: C1, C2, C3, C4, C5
    input_vector = [[
        features.get('C1', 0),
        features.get('C2', 0),
        features.get('C3', 0),
        features.get('C4', 0),
        features.get('C5', 0)
    ]]
    prediction = clf.predict(input_vector)
    return prediction[0]