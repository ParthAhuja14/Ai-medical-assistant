"""
Trains a RandomForest classifier on the public symptom-disease dataset
(132 binary symptom features -> 41 disease labels) and saves the model
plus the ordered symptom-feature list + label encoder to disk.

Run once during setup / image build:
    python -m app.ml.train_model

Dataset source (public, Kaggle "Disease Prediction Using Machine Learning"
by kaushil268, mirrored on GitHub): backend/data/Training.csv, Testing.csv
"""
import os
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    train_df = pd.read_csv(os.path.join(DATA_DIR, "Training.csv"))
    test_df = pd.read_csv(os.path.join(DATA_DIR, "Testing.csv"))

    feature_columns = [c for c in train_df.columns if c != "prognosis"]

    X_train, y_train_raw = train_df[feature_columns], train_df["prognosis"]
    X_test, y_test_raw = test_df[feature_columns], test_df["prognosis"]

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train_raw)
    y_test = encoder.transform(y_test_raw)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    test_preds = model.predict(X_test)
    test_acc = accuracy_score(y_test, test_preds)

    print(f"5-fold CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"Held-out test accuracy: {test_acc:.4f}")

    joblib.dump(model, os.path.join(MODEL_DIR, "disease_model.joblib"))
    joblib.dump(encoder, os.path.join(MODEL_DIR, "label_encoder.joblib"))
    with open(os.path.join(MODEL_DIR, "feature_columns.json"), "w") as f:
        json.dump(feature_columns, f, indent=2)

    print(f"Saved model artifacts to {MODEL_DIR}")


if __name__ == "__main__":
    main()
