from flask import Flask, request
import requests
import os

app = Flask(__name__)

GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
API_URL = f"https://7107.api.greenapi.com"

def send_message(chatId, text):
    url = f"{API_URL}/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
    requests.post(url, json={"chatId": chatId, "message": text})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("GOT WEBHOOK!") # This will show in Render logs
    
    if data.get("typeWebhook") == "incomingMessageReceived":
        chatId = data["senderData"]["chatId"]
        senderId = data["senderData"]["sender"]

        if "@g.us" in chatId:
            md = data.get("messageData", {})
            text = md.get("textMessageData", {}).get("textMessage", "") or md.get("extendedTextMessageData", {}).get("text", "")
            
            if "chat.whatsapp.com" in text:
                name = senderId.split('@')[0]
                send_message(chatId, f"🚫 @ {name} No group links allowed!")
                
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
