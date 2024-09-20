from flask import Flask, request, jsonify

app = Flask(__name__)

# Função para reconhecer o gesto baseado na descrição
def reconhecer_gesto(descricao):
    # Lógica simples de reconhecimento
    if "polegar" in descricao and "indicador" in descricao:
        return "Este gesto significa 'Olá'"
    elif "mínimo" in descricao:
        return "Este gesto significa 'Adeus'"
    else:
        return "Gesto desconhecido"

@app.route('/gesto', methods=['POST'])
def gesto():
    data = request.json
    descricao = data.get("descricao")
    
    # Reconhece o gesto baseado na descrição
    significado = reconhecer_gesto(descricao)
    
    return jsonify({"significado": significado})

if __name__ == '__main__':
    app.run(debug=True)
