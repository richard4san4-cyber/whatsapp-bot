from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GREEN_API_ID = os.environ.get("GREEN_API_ID")
GREEN_API_TOKEN = os.environ.get("GREEN_API_TOKEN")

@app.route('/')
def home():
    return "Bot is running", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("GOT WEBHOOK!", data) # This is key - shows in Render Logs
    
    if data and data.get('typeWebhook') == 'incomingMessageReceived':
        try:
            message = data['messageData']['textMessageData']['textMessage']
            chat_id = data['senderData']['chatId']
            
            url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
            payload = {"chatId": chat_id, "message": f"You said: {message}"}
            requests.post(url, json=payload)
            print(f"Replied to {chat_id}")
        except Exception as e:
            print("Error:", e)
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
