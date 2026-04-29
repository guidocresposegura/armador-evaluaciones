import os
from flask import Flask, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)

@app.route('/refinar', methods=['POST'])
def refinar_evaluacion():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key no configurada'}), 500
    
    client = Anthropic(api_key=api_key)
    datos = request.json
    texto_evaluacion = datos.get('texto', '')
    
    if not texto_evaluacion:
        return jsonify({'error': 'No se envio texto'}), 400
    
    mensaje = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Refina esta evaluacion:\n\n{texto_evaluacion}"
            }
        ]
    )
    respuesta = mensaje.content[0].text
    return jsonify({'resultado': respuesta})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
