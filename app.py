import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

# Import logic
from core.fahp import calculate_fahp, reconstruct_details
from core.ml_engine import predict_with_details
from core.program_data import PROGRAM_DETAILS, CRITERIA_NAMES

app = Flask(__name__)
DATA_FILE = os.path.join('data', 'history.json')

# Mapping ID to Question Text (Matches your Index.html)
QUESTIONS_TEXT = {
    'q1': 'Apakah anak sering memperhatikan suara-suara kecil yang tidak didengar orang lain?',
    'q2': 'Apakah anak lebih fokus pada gambaran besar daripada detail kecil?',
    'q3': 'Bisakah anak melakukan beberapa tugas sekaligus dengan mudah?',
    'q4': 'Bisakah anak kembali beraktivitas dengan mudah setelah diinterupsi/diganggu?',
    'q5': 'Apakah anak mudah mengenali pola pada benda-benda?',
    'q6': 'Apakah anak tahu cara memulai dan mempertahankan percakapan?',
    'q7': 'Apakah anak memahami maksud atau niat karakter dalam cerita fiksi?',
    'q8': 'Apakah anak kesulitan membayangkan menjadi orang lain (bermain peran)?',
    'q9': 'Apakah anak menikmati acara/kumpul sosial?',
    'q10': 'Apakah anak terobsesi pada minat/topik tertentu secara berlebihan?'
}

# --- DATA MANAGEMENT ---

def load_data():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return []

def save_data(new_record):
    if not os.path.exists('data'): os.makedirs('data')
    history = load_data()
    
    # Check if child exists to keep ID consistent
    existing_id = None
    for record in history:
        if record.get('name') == new_record['name'] and record.get('dob') == new_record['dob']:
            existing_id = record.get('id')
            break
            
    if existing_id:
        new_record['id'] = existing_id
        # Remove old record to insert updated one at top
        history = [r for r in history if r.get('id') != existing_id]
    else:
        max_id = 0
        if history:
            max_id = max(r.get('id', 0) for r in history)
        new_record['id'] = max_id + 1

    history.insert(0, new_record)
    
    with open(DATA_FILE, 'w') as f: json.dump(history, f, indent=4)
    return new_record

# --- PAGE ROUTES ---

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/start')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    form_data = request.form.to_dict()
    
    # 1. Extract Bio Data (Remove them from form_data)
    student_name = form_data.pop('student_name')
    dob = form_data.pop('dob')
    gender = form_data.pop('gender')
    family_history = form_data.pop('family_history')
    
    # 2. Capture Raw Answers
    # At this point, form_data only contains q1, q2... q10
    raw_answers = form_data.copy() 
    
    # 3. FAHP Calc
    score, risk, features, calc_details, totals = calculate_fahp(form_data)
    
    # 4. ML Calc
    program_name, ml_probabilities = predict_with_details(features)
    
    program_info = PROGRAM_DETAILS.get(program_name, {})
    max_criteria_code = max(features, key=features.get)
    max_criteria_name = CRITERIA_NAMES.get(max_criteria_code, max_criteria_code)
    max_criteria_val = features[max_criteria_code]

    # 5. Create Record
    result_record = {
        "name": student_name,
        "dob": dob,
        "gender": gender,
        "family": family_history,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "risk": risk,
        "program_name": program_name,
        "program_details": program_info,
        "prominent_criteria": {
            "code": max_criteria_code,
            "name": max_criteria_name,
            "value": round(max_criteria_val, 2)
        },
        "features": features,
        "ml_confidence": ml_probabilities,
        "raw_answers": raw_answers  # <--- NEW: Storing the Q1-Q10 answers
    }
    
    saved_record = save_data(result_record)
    
    # 6. Redirect to FAHP Calculation Page
    return render_template('calculation.html', 
                           details=calc_details, 
                           totals=totals, 
                           final_score=score, 
                           record_id=saved_record['id'])

# --- FLOW ROUTES (Calculations & Results) ---

@app.route('/ml_view/<int:record_id>')
def ml_view(record_id):
    history = load_data()
    target_record = None
    for record in history:
        if record.get('id') == record_id:
            target_record = record
            break
    
    if not target_record: return "Data not found", 404
    
    return render_template('calculation_ml.html', result=target_record)

@app.route('/calculation_view/<int:record_id>')
def calculation_view(record_id):
    history = load_data()
    target_record = None
    for record in history:
        if record.get('id') == record_id:
            target_record = record
            break
    
    if not target_record: return "Data not found", 404
    
    # Reconstruct the math details from the saved features
    calc_details, totals = reconstruct_details(target_record['features'])
    
    return render_template('calculation.html', 
                           details=calc_details, 
                           totals=totals, 
                           final_score=target_record['score'], 
                           record_id=target_record['id'])

@app.route('/result_view/<int:record_id>')
def result_view(record_id):
    history = load_data()
    target_record = None
    for record in history:
        if record.get('id') == record_id:
            target_record = record
            break
            
    if not target_record: return "Data not found", 404
    
    return render_template('result.html', result=target_record)


# --- DATA VIEW ROUTES ---

@app.route('/history')
def history():
    data = load_data()
    return render_template('history.html', history=data)

@app.route('/programs')
def program_data():
    return render_template('program.html', programs=PROGRAM_DETAILS.values())

@app.route('/children')
def children_data():
    history = load_data()
    unique_children = {}
    for record in history:
        name = record.get('name', 'Unknown')
        dob = record.get('dob', 'Unknown')
        key = f"{name}_{dob}"
        if key not in unique_children:
            unique_children[key] = {
                "name": name, "dob": dob, "gender": record.get('gender', '-'),
                "family": record.get('family', '-'), "medical": record.get('medical', ''),
                "last_test": record.get('date', '-')
            }            
    return render_template('children.html', children=list(unique_children.values()))

@app.route('/test_detail/<int:record_id>')
def test_detail(record_id):
    history = load_data()
    target_record = None
    for record in history:
        if record.get('id') == record_id:
            target_record = record
            break
            
    if not target_record:
        return "Data not found", 404
        
    return render_template('test_detail.html', 
                           result=target_record, 
                           questions=QUESTIONS_TEXT)

# --- CRUD ROUTES ---

@app.route('/delete_child', methods=['POST'])
def delete_child():
    target_name = request.form.get('name')
    target_dob = request.form.get('dob')
    history = load_data()
    new_history = [r for r in history if not (r.get('name') == target_name and r.get('dob') == target_dob)]
    with open(DATA_FILE, 'w') as f: json.dump(new_history, f, indent=4)
    return redirect(url_for('children_data'))

@app.route('/edit_child', methods=['GET'])
def edit_child_form():
    name = request.args.get('name')
    dob = request.args.get('dob')
    history = load_data()
    child_data = None
    for record in history:
        if record.get('name') == name and record.get('dob') == dob:
            child_data = record
            break
    if not child_data: return "Data anak tidak ditemukan", 404
    return render_template('edit_child.html', child=child_data)

@app.route('/update_child_bio', methods=['POST'])
def update_child_bio():
    form_data = request.form.to_dict()
    orig_name = form_data.pop('original_name')
    orig_dob = form_data.pop('original_dob')
    
    history = load_data()
    updated_count = 0
    for record in history:
        if record.get('name') == orig_name and record.get('dob') == orig_dob:
            record['name'] = form_data.get('student_name')
            record['dob'] = form_data.get('dob')
            record['gender'] = form_data.get('gender')
            record['medical'] = form_data.get('medical_history')
            record['family'] = form_data.get('family_history')
            updated_count += 1
            
    if updated_count > 0:
        with open(DATA_FILE, 'w') as f: json.dump(history, f, indent=4)
        return redirect(url_for('children_data'))
    else: return "Gagal", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)