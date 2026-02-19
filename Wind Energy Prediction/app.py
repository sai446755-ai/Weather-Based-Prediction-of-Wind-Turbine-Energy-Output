from flask import Flask, render_template, request
import requests
import numpy as np

app = Flask(__name__)

# 🔹 Replace with your OpenWeather API key
API_KEY = "3cb14b30ba409dd2ff94ab1883b99433"

@app.route('/')
def home():
    return render_template("intro.html")

@app.route('/windapi', methods=['GET', 'POST'])
def windapi():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form['city']

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # 🔹 Check if API returned success
        if data.get("cod") != 200:
            error = data.get("message", "Error fetching data")
            return render_template("predict.html", error=error)

        weather_data = {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "wind_speed": data['wind']['speed']
        }

    return render_template("predict.html", weather=weather_data, error=error)



@app.route('/predict', methods=['POST'])
def predict():

    theoretical_power = float(request.form['theoretical_power'])
    wind_speed = float(request.form['wind_speed'])

    # 🔹 Dummy ML Logic (Replace with trained model if needed)
    predicted_energy = round((0.5 * theoretical_power * (wind_speed ** 3)) / 1000, 2)

    return render_template("predict.html",
                           prediction_text=f"The energy predicted is {predicted_energy} KWh")


if __name__ == "__main__":
    app.run(debug=True)
