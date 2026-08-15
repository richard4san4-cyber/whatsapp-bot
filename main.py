from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# PUT YOUR GREEN API KEYS HERE LATER
ID_INSTANCE = "YOUR_ID_INSTANCE"
API_TOKEN_INSTANCE = "YOUR_API_TOKEN_INSTANCE"
GREEN_API_URL = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data) # this shows messages in Render logs

    if data and data.get('typeWebhook') == 'incomingMessageReceived':
        chat_id = data['senderData']['chatId']
        message = data['messageData']['textMessageData']['textMessage']
        
        reply = f"You said: {message}"
        
        payload = {
            "chatId": chat_id,
            "message": reply
        }
        requests.post(GREEN_API_URL, json=payload)
        
    return jsonify({"status": "ok"})

@app.route('/', methods=['GET'])
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
