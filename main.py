from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configurações do WhatsApp
VERIFY_TOKEN = "meu_token_secreto_123"
PHONE_NUMBER_ID = "1375060542357384"
# Cole abaixo o token de acesso gerado na Meta
WHATSAPP_TOKEN = "EAAPpBIUhFYEBSsc4v5qtfdW89ddSiXyEOTqsotfjZCMbiZCY8OU1AHHFA7ucpdZAREvhuGsn50Hz68x4IHP1uHA1YYgmyXlZCb1ZAJvae7O3hnLy6sU8xMm3eZCiPcVGHPTYWS2OchYPxCIpMYJneLCyUoZB5F4qzveZAs2PJdlO0VAU7lsmQQ3mdaaoKgHVQpanMpSEFxPPafVAjoZB5UjMmYREFVSvgIi9xbKrRkWNjLz7AtNhyi1FsIeZABELLzTHy2DaHU5BUWkp4BEl4FRS4c"

def enviar_resposta(to_number, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Resposta enviada para a Meta:", response.status_code, response.text)

@app.route("/", methods=["GET"])
def home():
    return "Bot de WhatsApp ativo no Render!", 200

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado com sucesso!")
        return challenge, 200
    return "Token de verificação inválido", 403

@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    data = request.get_json()
    print("Payload recebido no Webhook:", data)

    try:
        if "object" in data:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            remetente = message["from"]
                            texto_recebido = message.get("text", {}).get("body", "")
                            print(f"Mensagem de {remetente}: {texto_recebido}")
                            
                            # Envia a resposta automática de volta
                            enviar_resposta(remetente, f"Olá! Recebi sua mensagem: '{texto_recebido}'. O bot está funcionando perfeitamente!")
    except Exception as e:
        print("Erro ao processar mensagem:", str(e))

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
