import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

# Import logic
from core.fahp import calculate_fahp
from core.ml_engine import predict_recommendation
# Import the new data file
from core.program_data import PROGRAM_DETAILS, CRITERIA_NAMES

app = Flask(__name__)
DATA_FILE = os.path.join('data', 'history.json')

def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return []

def save_data(record):
    if not os.path.exists('data'): os.makedirs('data')
    history = load_data()
    record['id'] = len(history) + 1
    record['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    history.insert(0, record)
    with open(DATA_FILE, 'w') as f: json.dump(history, f, indent=4)
    return record

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    form_data = request.form.to_dict()
    student_name = form_data.pop('student_name')
    
    # 1. Calculate Score
    score, risk, features = calculate_fahp(form_data)
    
    # 2. Get AI Recommendation (Name only)
    program_name = predict_recommendation(features)
    
    # 3. Get Full Program Details from Dictionary
    program_info = PROGRAM_DETAILS.get(program_name, {})
    
    # 4. Identify Prominent Criteria (Highest Score)
    # features is {'C1': 0.3, 'C2': 0.8...}
    max_criteria_code = max(features, key=features.get)
    max_criteria_name = CRITERIA_NAMES.get(max_criteria_code, max_criteria_code)
    max_criteria_val = features[max_criteria_code]

    result_record = {
        "name": student_name,
        "score": score,
        "risk": risk,
        "program_name": program_name,
        "program_details": program_info, # Passing the dictionary of details
        "prominent_criteria": {
            "code": max_criteria_code,
            "name": max_criteria_name,
            "value": round(max_criteria_val, 2)
        },
        "features": features
    }
    
    final_record = save_data(result_record)
    return render_template('result.html', result=final_record)

@app.route('/history')
def history():
    data = load_data()
    return render_template('history.html', history=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)