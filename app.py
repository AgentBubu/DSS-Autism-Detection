import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

# Import logic
from core.fahp import calculate_fahp
from core.ml_engine import predict_recommendation
from core.program_data import PROGRAM_DETAILS, CRITERIA_NAMES

app = Flask(__name__)
DATA_FILE = os.path.join('data', 'history.json')

# ... [Keep your existing load_data and save_data functions here] ...
def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return []

def save_data(new_record):
    if not os.path.exists('data'): os.makedirs('data')
    history = load_data()
    
    # LOGIC CHANGE: Check if child exists (Same Name + Same DOB)
    # If exists, REPLACE the record. If not, INSERT new.
    
    existing_index = -1
    for i, record in enumerate(history):
        if record.get('name') == new_record['name'] and record.get('dob') == new_record['dob']:
            existing_index = i
            break
            
    if existing_index != -1:
        # Update existing record (Retake Test logic)
        # We preserve the ID to keep it consistent, but update everything else
        new_record['id'] = history[existing_index].get('id')
        history[existing_index] = new_record
    else:
        # New Child
        new_record['id'] = len(history) + 1
        history.insert(0, new_record)
    
    with open(DATA_FILE, 'w') as f: json.dump(history, f, indent=4)
    return new_record

# --- UPDATED ROUTES ---

@app.route('/')
def landing():
    # This is the new Landing Page
    return render_template('landing.html')

@app.route('/start')
def index():
    # This is the Form page (previously index)
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    form_data = request.form.to_dict()
    
    # Extract Bio Data
    student_name = form_data.pop('student_name')
    dob = form_data.pop('dob')
    gender = form_data.pop('gender')
    family_history = form_data.pop('family_history')
    
    # Calculate Logic
    score, risk, features = calculate_fahp(form_data)
    program_name = predict_recommendation(features)
    program_info = PROGRAM_DETAILS.get(program_name, {})
    
    max_criteria_code = max(features, key=features.get)
    max_criteria_name = CRITERIA_NAMES.get(max_criteria_code, max_criteria_code)
    max_criteria_val = features[max_criteria_code]

    result_record = {
        "name": student_name,
        "dob": dob,                   # NEW
        "gender": gender,             # NEW
        "family": family_history,     # NEW
        "score": score,
        "risk": risk,
        "program_name": program_name,
        "program_details": program_info,
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

# --- NEW ROUTES ---
@app.route('/children')
def children_data():
    history = load_data()
    
    unique_children = {}
    
    for record in history:
        # Create a unique key using Name and Date of Birth
        # We use .get() to avoid errors if old data doesn't have these fields
        name = record.get('name', 'Unknown')
        dob = record.get('dob', 'Unknown')
        key = f"{name}_{dob}"
        
        if key not in unique_children:
            unique_children[key] = {
                "name": name,
                "dob": dob,
                "gender": record.get('gender', '-'),
                "family": record.get('family', '-'),
                "last_test": record.get('date', '-')
            }            
    children_list = list(unique_children.values())
    
    return render_template('children.html', children=children_list)

@app.route('/programs')
def program_data():
    return render_template('program.html', programs=PROGRAM_DETAILS.values())

# --- ADD THESE ROUTES TO app.py ---

@app.route('/delete_child', methods=['POST'])
def delete_child():
    # 1. Get the identifiers from the form
    target_name = request.form.get('name')
    target_dob = request.form.get('dob')
    
    # 2. Load existing data
    history = load_data()
    
    # 3. Filter out records that match BOTH Name and DOB
    # This deletes the child profile AND all their test history
    new_history = [
        record for record in history 
        if not (record.get('name') == target_name and record.get('dob') == target_dob)
    ]
    
    # 4. Save back to JSON
    with open(DATA_FILE, 'w') as f:
        json.dump(new_history, f, indent=4)
        
    return redirect(url_for('children_data'))

@app.route('/edit_child', methods=['GET'])
def edit_child_form():
    # Get identifiers from URL parameters
    name = request.args.get('name')
    dob = request.args.get('dob')
    
    history = load_data()
    child_data = None
    
    # Find the child
    for record in history:
        if record.get('name') == name and record.get('dob') == dob:
            child_data = record
            break
            
    if not child_data:
        return "Data anak tidak ditemukan", 404
        
    return render_template('edit_child.html', child=child_data)

@app.route('/update_child_bio', methods=['POST'])
def update_child_bio():
    form_data = request.form.to_dict()
    
    # Identifiers (Original) to find the record
    orig_name = form_data.pop('original_name')
    orig_dob = form_data.pop('original_dob')
    
    # New Data
    new_name = form_data.get('student_name')
    new_dob = form_data.get('dob')
    new_gender = form_data.get('gender')
    new_medical = form_data.get('medical_history')
    new_family = form_data.get('family_history')
    
    history = load_data()
    updated = False
    
    for record in history:
        # Find the record by ORIGINAL Name/DOB
        if record.get('name') == orig_name and record.get('dob') == orig_dob:
            # Update ONLY Biodata fields
            record['name'] = new_name
            record['dob'] = new_dob
            record['gender'] = new_gender
            record['medical'] = new_medical
            record['family'] = new_family
            updated = True
            break
            
    if updated:
        with open(DATA_FILE, 'w') as f:
            json.dump(history, f, indent=4)
        return redirect(url_for('children_data'))
    else:
        return "Gagal memperbarui data", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)