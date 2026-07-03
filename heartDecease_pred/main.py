from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Load Model

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))


# Home Page

@app.route("/")
def home():
    return render_template("index.html")


# Prediction

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    age = float(data["age"])
    sex = int(data["sex"])
    cp = int(data["cp"])
    trestbps = float(data["trestbps"])
    chol = float(data["chol"])
    fbs = int(data["fbs"])
    restecg = int(data["restecg"])
    thalach = float(data["thalach"])
    exang = int(data["exang"])
    oldpeak = float(data["oldpeak"])
    slope = int(data["slope"])
    ca = int(data["ca"])
    thal = int(data["thal"])

    # Create dataframe with original features

    input_df = pd.DataFrame([{
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }])

    # Apply the same preprocessing as training

    input_df = pd.get_dummies(
        input_df,
        columns=["cp", "restecg", "slope", "thal", "ca"],
        drop_first=True
    )

    # Match training columns

    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Scale

    input_scaled = scaler.transform(input_df)

    # Predict

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    confidence = round(max(probability) * 100, 2)

    if prediction == 1:

        return jsonify({
            "prediction": "High Risk",
            "confidence": confidence,
            "color": "red",
            "emoji": "❤️",
            "message": "Please consult a healthcare professional for further evaluation."
        })

    else:

        return jsonify({
            "prediction": "Low Risk",
            "confidence": confidence,
            "color": "green",
            "emoji": "💚",
            "message": "No significant signs of heart disease were detected."
        })

if __name__ == "__main__":
    app.run(debug=True)