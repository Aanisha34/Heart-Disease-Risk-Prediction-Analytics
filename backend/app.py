import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# Dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'heart.csv')

model = None
df_global = None

def load_and_train():
    global model, df_global
    
    # Try finding heart.csv or heart data set.csv in dataset folder
    possible_paths = [
        DATASET_PATH,
        os.path.join(BASE_DIR, 'dataset', 'heart data set.csv'),
        os.path.join(BASE_DIR, 'heart.csv'),
        os.path.join(BASE_DIR, 'heart data set.csv')
    ]
    
    target_path = None
    for path in possible_paths:
        if os.path.exists(path):
            target_path = path
            break
            
    if not target_path:
        print(f"Error: Dataset file not found in {possible_paths}")
        return

    try:
        print(f"Loading dataset from: {target_path}")
        df = pd.read_csv(target_path)
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        # Convert numeric values
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.fillna(df.median(), inplace=True)
        
        df_global = df.copy()

        # Split features and target
        X = df.drop(columns=['target'])
        y = df['target']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        
        model = rf
        print("✅ Model trained successfully!")
        
    except Exception as e:
        print(f"❌ Training Failed: {str(e)}")

# Train model when app starts
load_and_train()

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model is not trained'}), 500
    try:
        data = request.json
        features = [
            float(data.get('age', 52)),
            float(data.get('sex', 1)),
            float(data.get('cp', 0)),
            float(data.get('trestbps', 125)),
            float(data.get('chol', 212)),
            float(data.get('fbs', 0)),
            float(data.get('restecg', 1)),
            float(data.get('thalach', 168)),
            float(data.get('exang', 0)),
            float(data.get('oldpeak', 1.0)),
            float(data.get('slope', 2)),
            float(data.get('ca', 2)),
            float(data.get('thal', 3))
        ]

        pred = model.predict([features])[0]
        prob = model.predict_proba([features])[0][1] if hasattr(model, "predict_proba") else 0.5

        return jsonify({
            'prediction': int(pred),
            'risk_percentage': round(float(prob) * 100, 2),
            'message': 'High risk of Heart Disease detected' if pred == 1 else 'Low risk of Heart Disease detected'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analytics', methods=['GET'])
def analytics():
    if df_global is None:
        return jsonify({'error': 'Dataset unavailable'}), 500

    avg_age = float(df_global['age'].mean()) if 'age' in df_global.columns else 0
    disease_cases = int(df_global['target'].value_counts().get(1, 0)) if 'target' in df_global.columns else 0
    healthy_cases = int(df_global['target'].value_counts().get(0, 0)) if 'target' in df_global.columns else 0

    df_copy = df_global.copy()
    if 'age' in df_copy.columns:
        df_copy['age_group'] = pd.cut(df_copy['age'], bins=[0, 40, 55, 70, 100], labels=['<40', '40-55', '55-70', '70+'])
        age_dist = df_copy['age_group'].value_counts().to_dict()
    else:
        age_dist = {}

    return jsonify({
        'total_records': len(df_global),
        'avg_age': round(avg_age, 1),
        'disease_cases': disease_cases,
        'healthy_cases': healthy_cases,
        'age_distribution': {str(k): int(v) for k, v in age_dist.items()}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)