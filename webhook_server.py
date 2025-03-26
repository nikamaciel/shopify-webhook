from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Credenciais do Shopify
SHOPIFY_STORE = "https://enigmafemme.myshopify.com"
API_KEY = "SUA_CHAVE_DA_API"
PASSWORD = "SUA_SENHA"

# Rota para receber o Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Dados recebidos do Shopify

    if not data:
        return jsonify({"message": "No data received"}), 400

    # Extrai informações do produto recebido
    produto = {
        "product": {
            "title": data.get("title", "Produto Sem Nome"),
            "body_html": data.get("body_html", ""),
            "vendor": "Kaisan",
            "product_type": data.get("product_type", ""),
            "variants": [
                {
                    "option1": "Padrão",
                    "price": data.get("variants", [{}])[0].get("price", "0.00"),
                    "sku": data.get("variants", [{}])[0].get("sku", "000000"),
                    "inventory_quantity": 10
                }
            ],
            "images": [
                {"src": data.get("images", [{}])[0].get("src", "")}
            ]
        }
    }

    # Envia o produto para Shopify
    response = requests.post(
        f"{SHOPIFY_STORE}/admin/api/2023-10/products.json",
        json=produto,
        auth=(API_KEY, PASSWORD),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 201:
        return jsonify({"message": "Produto importado com sucesso!"}), 201
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
