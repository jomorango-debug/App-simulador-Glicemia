from flask import Flask, render_template, request, jsonify
from google import genai
import os
import re

app = Flask(__name__)

# Inicialização do cliente Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CENARIOS = {
    "pos_eam": {
        "titulo": "Sr. Alberto (Pós-EAM)",
        "texto": (
            "Sr. Alberto, 65 anos, admitido após enfarte agudo do miocárdio. "
            "Glicemia capilar: 265 mg/dL. "
            "Prescrição: NPH 18 UI e Aspart SOS. "
            "O que faz em primeiro lugar?"
        )
    },
    "jejum": {
        "titulo": "Sr. Alberto (Jejum para cateterismo)",
        "texto": (
            "Sr. Alberto em jejum para cateterismo às 10h00. "
            "Glicemia capilar: 135 mg/dL. "
            "Deve administrar a NPH das 08h00?"
        )
    },
    "baixa_visao": {
        "titulo": "D. Maria (Baixa visão)",
        "texto": (
            "D. Maria, 70 anos, com baixa visão grave. "
            "Glicemia capilar: 310 mg/dL. "
            "Como garante que ela prepara a dose correta de insulina em segurança?"
        )
    }
}

SYSTEM_PROMPT = """
Tu és um Professor de Enfermagem especialista em Diabetes em Portugal.
Avalias decisões clínicas de estudantes de enfermagem de forma pedagógica, rigorosa e objetiva.
Responde sempre em português de Portugal.
Não uses português do Brasil.

Foca-te em:
- segurança da pessoa
- farmacocinética das insulinas
- técnica correta de preparação e administração
- prevenção de hipoglicemia
- adequação da decisão ao contexto clínico
- necessidade de confirmação da prescrição e dos protocolos institucionais, quando aplicável

Regras:
- Não inventes prescrições.
- Não alteres doses sem explicitar que isso depende de prescrição, protocolo institucional ou validação clínica.
- Se houver risco clínico, identifica-o com clareza.
- Dá feedback útil para contexto de sala de aula.
- Mantém a resposta relativamente curta, mas suficientemente explicativa.
- Termina obrigatoriamente com uma pontuação de 0 a 10.

Estrutura obrigatória da resposta:
1. Avaliação geral
2. Aspetos adequados
3. Riscos ou erros de segurança
4. Conduta mais adequada
5. Pontuação: X/10
"""

def extrair_score(texto: str):
    match = re.search(r'Pontuação:\s*(\d+(?:[.,]\d+)?)\s*/\s*10', texto, re.IGNORECASE)
    if match:
        return match.group(1).replace(",", ".")
    return None

@app.route("/")
def index():
    return render_template("index.html", cenarios=CENARIOS)

@app.route("/avaliar", methods=["POST"])
def avaliar():
    try:
        data = request.get_json()
        cenario_id = data.get("cenario_id", "")
        resposta_aluno = data.get("resposta", "").strip()

        if cenario_id not in CENARIOS:
            return jsonify({"erro": "Cenário inválido."}), 400

        if not resposta_aluno:
            return jsonify({"erro": "A resposta está vazia."}), 400

        cenario = CENARIOS[cenario_id]

        prompt = f"""
Cenário clínico:
{cenario['texto']}

Resposta do estudante:
{resposta_aluno}

Avalia esta resposta de acordo com as instruções fornecidas.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )

        feedback = response.text if hasattr(response, "text") else "Não foi possível obter resposta do modelo."
        score = extrair_score(feedback)

        return jsonify({
            "titulo": cenario["titulo"],
            "cenario": cenario["texto"],
            "feedback": feedback,
            "score": score
        })

    except Exception as e:
        return jsonify({"erro": f"Erro ao avaliar a resposta: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
