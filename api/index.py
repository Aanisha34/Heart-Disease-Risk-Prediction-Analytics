import os
import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Load saved pipeline model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "../model/heart_disease_pipeline.pkl"
)
model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        # Parse inputs matching training features order
        features = np.array([list(data.values())])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        return jsonify(
            {
                "status": "success",
                "prediction": int(prediction),
                "risk_probability": round(float(probability) * 100, 2),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# Export app for Vercel WSGI
if __name__ == "__main__":
    app.run(debug=True)