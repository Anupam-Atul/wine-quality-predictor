import os
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Order MUST match the columns you trained on in Colab (X.columns).
FEATURES = [
    "fixed acidity", "volatile acidity", "citric acid", "residual sugar",
    "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density",
    "pH", "sulphates", "alcohol",
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "Model", "wine_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "Model", "scaler.pkl")  # optional

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None

# If the model remembers its column names, trust those over FEATURES.
FEATURES = list(getattr(model, "feature_names_in_", FEATURES))


@app.route("/")
def index():
    return render_template("index.html", features=FEATURES)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    try:
        row = [float(data[f]) for f in FEATURES]
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Please fill every field with a valid number."), 400

    X = pd.DataFrame([row], columns=FEATURES)
    if scaler is not None:
        X = scaler.transform(X)

    pred = model.predict(X)[0]
    result = {"prediction": int(pred) if float(pred).is_integer() else round(float(pred), 2)}

    if hasattr(model, "predict_proba"):
        result["confidence"] = round(float(max(model.predict_proba(X)[0])) * 100, 1)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=int(os.environ.get("PORT", 5000)))
