import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de Verificação: Você inventa uma palavra-passe aqui para a Meta validar sua URL
VERIFY_TOKEN = "meu_token_secreto_123"

@app.route("/", methods=["GET"])
def home():
    return "Bot do WhatsApp rodando na nuvem com sucesso!", 200

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

# Rota que recebe as mensagens enviadas pelos clientes
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print("Mensagem recebida da Meta:", data)

    try:
        # Aqui é onde o bot vai processar a mensagem no futuro
        # Por enquanto, apenas confirmamos o recebimento para a Meta
        return jsonify({"status": "recebido"}), 200
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        return jsonify({"status": "erro"}), 500

if __name__ == "__main__":
    # A nuvem define a porta automaticamente através de variáveis de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)