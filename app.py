from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FRANKFURTER_API = "https://api.frankfurter.app/latest"

def convert_currency(amount, source, target):
    try:
        url = f"{FRANKFURTER_API}?amount={amount}&from={source}&to={target}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"][target]
    except Exception as e:
        print("Error during conversion:", e)
        return None

# Add this GET route
@app.route("/", methods=["GET"])
def home():
    return "Currency Converter Bot is running! Use POST requests to communicate with DialogFlow."

@app.route("/", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    
    try:
        params = req["queryResult"]["parameters"]
        source_currency = params["unit-currency"]["currency"].upper()
        amount = params["unit-currency"]["amount"]
        target_currency = params["currency-name"].upper()
    except KeyError:
        return jsonify({"fulfillmentText": "Sorry, I couldn't understand the currencies."})
    

    converted_amount = convert_currency(amount, source_currency, target_currency)
    
    if converted_amount is None:
        fulfillment_text = "Sorry, I couldn't fetch the conversion right now. Please try again later."
    else:
        fulfillment_text = f"💱 {amount} {source_currency} = {converted_amount} {target_currency}"
    

    return jsonify({"fulfillmentText": fulfillment_text})

if __name__ == "__main__":
    app.run(debug=True)