from flask import Flask, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route("/")
def home():
    return "Currency Converter API"

@app.route("/convert/<from_currency>/<to_currency>/<amount>")
def convert(from_currency, to_currency, amount):

    url = BASE_URL + from_currency.upper()

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid currency"}

    data = response.json()

    rates = data["rates"]

    if to_currency.upper() not in rates:
        return {"error": "Currency not found"}

    rate = rates[to_currency.upper()]

    converted = float(amount) * rate

    result = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": float(amount),
        "converted_amount": round(converted, 2)
    }

    return jsonify(result)

app.run(debug=True)