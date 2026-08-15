from flask import Flask, request
import requests
import os

app = Flask(__name__)

GREEN_API_ID = os.getenv("GREEN_API_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
API_URL = f"https://7105.api.greenapi.com"

def send_message(chatId, text):
    url = f"{API_URL}/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
    data = {"chatId": chatId, "message": text}
    requests.post(url, json=data)

def delete_message(chatId, idMessage):
    url = f"{API_URL}/waInstance{GREEN_API_ID}/deleteMessages/{GREEN_API_TOKEN}"
    data = {"chatId": chatId, "idMessages": [idMessage]}
    requests.post(url, json=data)

def remove_participant(groupId, participant):
    url = f"{API_URL}/waInstance{GREEN_API_ID}/removeParticipant/{GREEN_API_TOKEN}"
    data = {"groupId": groupId, "participant": participant}
    requests.post(url, json=data)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if data.get("typeWebhook") == "incomingMessageReceived":
        messageData = data["messageData"]
        sender = data["senderData"]
        chatId = sender["chatId"]
        senderId = sender["sender"]
        idMessage = data["idMessage"]

        # Only work in groups
        if "@g.us" in chatId:
            text = messageData.get("textMessageData", {}).get("textMessage", "")
            
            # Check for WhatsApp group link
            if "chat.whatsapp.com" in text:
                # 1. Delete the link message
                delete_message(chatId, idMessage)
                
                # 2. Kick the sender
                remove_participant(chatId, senderId)
                
                # 3. Send warning to group
                name = senderId.split('@')[0]
                send_message(chatId, f"🚫 Group links not allowed! @{name} has been removed.")
                
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
