# Updated FAHP Logic based on the new PDF Revision
# Weights are now Triangular Fuzzy Numbers (L, M, U) derived from Table 10 (Page 11)

TFN_WEIGHTS = {
    'C1': (0.275, 0.357, 0.672),  # Sensory
    'C2': (0.234, 0.337, 0.539),  # Social
    'C3': (0.090, 0.127, 0.191),  # Communication
    'C4': (0.047, 0.069, 0.116),  # Empathy
    'C5': (0.250, 0.374, 0.576)   # Interests
}

# Max possible score for each criteria (Used for Normalization)
# C1 has 3 questions, C2 has 3, C3 has 2, C4 has 1, C5 has 1
CRITERIA_MAX_SCORES = {
    'C1': 3,
    'C2': 3,
    'C3': 2,
    'C4': 1,
    'C5': 1
}

# Map HTML form names (q1...q10) to Criteria
Q_MAP = {
    'q1': 'C1', 'q2': 'C3', 'q3': 'C1', 'q4': 'C2', 'q5': 'C1',
    'q6': 'C2', 'q7': 'C3', 'q8': 'C4', 'q9': 'C2', 'q10': 'C5'
}

def calculate_fahp(form_data):
    # 1. Initialize Score Counters
    raw_scores = {k: 0 for k in TFN_WEIGHTS}
    
    # 2. Aggregate Raw Scores (Summing 1s and 0s)
    for key, val in form_data.items():
        if key in Q_MAP:
            crit = Q_MAP[key]
            raw_scores[crit] += int(val)

    # 3. Calculate Fuzzy Scores
    # We sum L, M, and U separately
    sum_l = 0.0
    sum_m = 0.0
    sum_u = 0.0
    
    normalized_features = {} # For ML Engine

    for crit, weight_tuple in TFN_WEIGHTS.items():
        # Normalization: Raw Score / Max Possible Score
        # Example C1: 1 / 3 = 0.333
        norm_score = raw_scores[crit] / CRITERIA_MAX_SCORES[crit]
        normalized_features[crit] = norm_score

        # Multiply Normalization Score * TFN Weight
        # (Score * L, Score * M, Score * U)
        val_l = norm_score * weight_tuple[0]
        val_m = norm_score * weight_tuple[1]
        val_u = norm_score * weight_tuple[2]

        # Add to totals
        sum_l += val_l
        sum_m += val_m
        sum_u += val_u

    # 4. Defuzzification (Page 12 formula)
    # (Total_L + Total_M + Total_U) / 3
    final_score = (sum_l + sum_m + sum_u) / 3

    # Rounding to match paper style (optional, but good for UI)
    final_score = round(final_score, 3)

    # 5. Determine Risk Level (Table 14)
    # Low: 0.0 - 0.33
    # Medium: 0.34 - 0.66
    # High: 0.67 - 1.0
    if final_score <= 0.33:
        risk = "Low"
    elif final_score <= 0.66:
        risk = "Medium"
    else:
        risk = "High"

    return final_score, risk, normalized_features