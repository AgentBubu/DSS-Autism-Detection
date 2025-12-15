# core/fahp.py

TFN_WEIGHTS = {
    'C1': (0.275, 0.357, 0.672),
    'C2': (0.234, 0.337, 0.539),
    'C3': (0.090, 0.127, 0.191),
    'C4': (0.047, 0.069, 0.116),
    'C5': (0.250, 0.374, 0.576)
}

CRITERIA_MAX_SCORES = {'C1': 3, 'C2': 3, 'C3': 2, 'C4': 1, 'C5': 1}

Q_MAP = {
    'q1': 'C1', 'q2': 'C3', 'q3': 'C1', 'q4': 'C2', 'q5': 'C1',
    'q6': 'C2', 'q7': 'C3', 'q8': 'C4', 'q9': 'C2', 'q10': 'C5'
}

def calculate_fahp(form_data):
    raw_scores = {k: 0 for k in TFN_WEIGHTS}
    
    for key, val in form_data.items():
        if key in Q_MAP:
            crit = Q_MAP[key]
            raw_scores[crit] += int(val)

    sum_l, sum_m, sum_u = 0.0, 0.0, 0.0
    normalized_features = {}
    
    # NEW: List to store detailed steps for the UI
    calculation_details = []

    for crit, weight_tuple in TFN_WEIGHTS.items():
        norm_score = raw_scores[crit] / CRITERIA_MAX_SCORES[crit]
        normalized_features[crit] = norm_score

        val_l = norm_score * weight_tuple[0]
        val_m = norm_score * weight_tuple[1]
        val_u = norm_score * weight_tuple[2]

        sum_l += val_l
        sum_m += val_m
        sum_u += val_u
        
        # Store step-by-step data
        calculation_details.append({
            'criteria': crit,
            'raw': raw_scores[crit],
            'max': CRITERIA_MAX_SCORES[crit],
            'norm': round(norm_score, 3),
            'weight_l': weight_tuple[0],
            'weight_m': weight_tuple[1],
            'weight_u': weight_tuple[2],
            'res_l': round(val_l, 4),
            'res_m': round(val_m, 4),
            'res_u': round(val_u, 4)
        })

    final_score = (sum_l + sum_m + sum_u) / 3
    final_score = round(final_score, 3)

    if final_score <= 0.33: risk = "Low"
    elif final_score <= 0.66: risk = "Medium"
    else: risk = "High"

    # NEW: Return totals dictionary for the UI
    totals = {
        'sum_l': round(sum_l, 4),
        'sum_m': round(sum_m, 4),
        'sum_u': round(sum_u, 4)
    }

    # Return 4 items now instead of 3
    return final_score, risk, normalized_features, calculation_details, totals

def reconstruct_details(features):
    """
    Re-generates the detailed calculation steps from saved normalized features.
    Used for the /calculation_view route.
    """
    calculation_details = []
    sum_l, sum_m, sum_u = 0.0, 0.0, 0.0
    
    # We iterate through TFN_WEIGHTS to ensure order
    for crit, weight_tuple in TFN_WEIGHTS.items():
        # Get normalized score from saved record (default 0 if missing)
        norm_score = features.get(crit, 0)
        
        # Reverse calculate raw score for display (Norm * Max)
        raw_score = int(round(norm_score * CRITERIA_MAX_SCORES[crit]))
        
        # Calculate Fuzzy Multiplication
        val_l = norm_score * weight_tuple[0]
        val_m = norm_score * weight_tuple[1]
        val_u = norm_score * weight_tuple[2]
        
        sum_l += val_l
        sum_m += val_m
        sum_u += val_u
        
        calculation_details.append({
            'criteria': crit,
            'raw': raw_score,
            'max': CRITERIA_MAX_SCORES[crit],
            'norm': round(norm_score, 3),
            'weight_l': weight_tuple[0],
            'weight_m': weight_tuple[1],
            'weight_u': weight_tuple[2],
            'res_l': round(val_l, 4),
            'res_m': round(val_m, 4),
            'res_u': round(val_u, 4)
        })
        
    totals = {
        'sum_l': round(sum_l, 4),
        'sum_m': round(sum_m, 4),
        'sum_u': round(sum_u, 4)
    }
    
    return calculation_details, totals