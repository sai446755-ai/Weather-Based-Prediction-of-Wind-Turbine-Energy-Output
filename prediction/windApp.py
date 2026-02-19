# -------------------- IMPORTS --------------------
import os
import joblib
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# load environment variables (.env file)
load_dotenv()

# -------------------- APP SETUP --------------------
app = Flask(__name__)

# Load trained ML model
model = joblib.load("model.pkl")


# ===================== ROUTES =====================

# Home Page (Intro Page)
@app.route("/")
def home():
    return render_template("index.html")


# Prediction Page
@app.route("/predict")
def predict_page():
    return render_template("predict.html")


# ---------------- WEATHER API ----------------
@app.route("/windapi", methods=["POST"])
def windapi():

    city = request.form.get("city")

    # API key from .env
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return render_template("predict.html",
                               error="API key missing! Add OPENWEATHER_API_KEY in .env file")

    # API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url).json()

    # If city not found
    if response.get("cod") != 200:
        return render_template("predict.html",
                               error=response.get("message", "City not found"))

    # Extract values
    temp = round(response["main"]["temp"] - 273.15, 2)
    humidity = response["main"]["humidity"]
    pressure = response["main"]["pressure"]
    wind_speed = response["wind"]["speed"]

    return render_template("predict.html",
                           temp=f"{temp} °C",
                           humid=f"{humidity} %",
                           pressure=f"{pressure} mmHG",
                           speed=f"{wind_speed} m/s")


# ---------------- ML PREDICTION ----------------
@app.route("/y_predict", methods=["POST"])
def y_predict():

    try:
        windspeed = float(request.form["windspeed"])
        torque = float(request.form["torque"])

        # Model prediction
        prediction = model.predict([[windspeed, torque]])
        output = round(prediction[0], 2)

        return render_template("predict.html",
                               prediction_text=f"Predicted Energy Output: {output} KWh")

    except Exception as e:
        return render_template("predict.html", error=str(e))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
