from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurações do seu Servidor Evolution API (Local ou Nuvem)
EVOLUTION_SERVER = "http://localhost:8080" # Onde a API está a correr
API_KEY = "sua_global_api_key_aqui"         # Chave de segurança da API

def enviar_mensagem_cliente(instance_name, number, text):
    """Envia uma mensagem através da instância específica do lojista"""
    url = f"{EVOLUTION_SERVER}/message/sendText/{instance_name}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": number,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Mensagem enviada para o cliente [{instance_name}]:", response.status_code, response.text)

@app.route("/", methods=["GET"])
def home():
    print("Servidor SaaS Central ativo e operacional!")
    return "SaaS de Bots Multi-Cliente Ativo!", 200

# Webhook único que recebe mensagens de TODOS os clientes lojistas
@app.route("/webhook-saas", methods=["POST"])
def webhook_multi_cliente():
    data = request.get_json()
    print("Payload recebido de um lojista:", data)

    try:
        # A Evolution API identifica qual instância/lojista mandou a mensagem
        event = data.get("event")
        instance = data.get("instance") # Ex: "pizzaria_central"
        
        if event == "messages.upsert":
            message_data = data.get("data", {})
            
            # Evita responder mensagens enviadas pelo próprio bot
            if message_data.get("key", {}).get("fromMe", False):
                return jsonify({"status": "ignored_own_message"}), 200

            remetente = message_data.get("key", {}).get("remoteJid", "")
            texto_recebido = message_data.get("message", {}).get("conversation", "")
            
            if not texto_recebido:
                # Tenta capturar se for mensagem estendida
                texto_recebido = message_data.get("message", {}).get("extendedTextMessage", {}).get("text", "")

            print(f"Loja [{instance}] recebeu de {remetente}: {texto_recebido}")

            # Lógica comercial automatizada por nicho ou padrão
            resposta_personalizada = (
                f"Olá! Seja bem-vindo ao atendimento automatizado da loja. "
                f"Recebemos a sua mensagem: '{texto_recebido}'. "
                f"Como podemos ajudar o senhor(a) hoje?"
            )

            # Devolve a resposta usando a mesma instância do lojista
            enviar_mensagem_cliente(instance, remetente, resposta_personalizada)

    except Exception as e:
        print("Erro ao processar webhook multi-cliente:", str(e))

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
