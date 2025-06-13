from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # يسحب المفتاح من Environment Variables

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    signal = f"""
📡 Webhook Signal:
Symbol: {data.get('symbol')}
Action: {data.get('action')}
Qty: {data.get('qty')}
Price: {data.get('price')}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد تداول ذكي. حلل الإشارة وحدد ما إذا كانت فرصة للشراء أو البيع أو الانتظار. ثم أعطِ: Strike مناسب، سعر الدخول، وقف الخسارة، الهدف، وسبب التوصية بشكل مختصر."},
                {"role": "user", "content": signal}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"recommendation": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
