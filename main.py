import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de Verificação do Webhook que definimos na Meta
VERIFY_TOKEN = "meu_token_secreto_123"

# Credenciais da API do WhatsApp da Meta (pegue o seu Token de Acesso e o ID do Telefone na tela da Meta)
WHATSAPP_TOKEN = "EAAPpBIUhFYEBSsObZB8ZBe1JJI1fB6zE1FgNEBLdyXMOOg32TkEyHUMrRjMex7xs5QxHTZBYXN5dfTTXkvTGfZCVXRMPDATOvMEbSZCdkoZCXzGouWmiQHqZAIXBIxXkaLZAfdA8fhDWi8iZAaj51O0ZC4kYNf23ZANXa0FAbpXZAt9Y36N9xoUwhC3NhZCRli28ZAu2p1Q5afhm6ByiLrZCwLjRDylZAJbuRSztPK7nIQKcrZACQJmy9waFw7kGH27GRwFIDJZCxSnujxoF6ioYu3D8IUblPq"
PHONE_NUMBER_ID = "137506042357384" # ID do número de teste que aparece na Meta

@app.route("/", methods=["GET"])
def home():
    return "Bot de WhatsApp rodando na nuvem com sucesso!"

# Rota obrigatória para a Meta verificar o Webhook
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED com sucesso!")
            return challenge, 200
        else:
            return "Erro de verificação", 403
    return "Parâmetros inválidos", 400

# Rota que recebe as mensagens enviadas pelo WhatsApp
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Dados recebidos:", data)

    try:
        # Extrai a mensagem enviada pelo usuário
        if "entry" in data and data["entry"]:
            changes = data["entry"][0].get("changes", [])
            if changes:
                value = changes[0].get("value", {})
                messages = value.get("messages", [])
                
                if messages:
                    msg = messages[0]
                    from_number = msg["from"] # Número de quem mandou a mensagem
                    msg_body = msg["text"]["body"] # Texto da mensagem
                    
                    print(f"de {from_number}: {msg_body}")

                    # Envia uma resposta automática de volta
                    enviar_resposta(from_number, f"Recebi a sua mensagem: '{msg_body}'. Bot em Python online!")

    except Exception as e:
        print("Erro ao processar mensagem:", e)

    return jsonify({"status": "success"}), 200

def enviar_resposta(to_number, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Resposta enviada para a Meta:", response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
