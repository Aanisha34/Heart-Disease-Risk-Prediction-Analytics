import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("data/heart.csv")
X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Bundle preprocessing and model into one pipeline
pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]
)

pipeline.fit(X_train, y_train)

# Save lightweight pipeline model
joblib.dump(pipeline, "model/heart_disease_pipeline.pkl", compress=3)