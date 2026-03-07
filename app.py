import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador de Enfermagem", page_icon="🩺", layout="wide")

# --- 2. CONFIGURAÇÃO DA IA ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Erro: GOOGLE_API_KEY não encontrada nos Secrets.")
    st.stop()

# Inicialização do Modelo
if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Tu és um Professor de Enfermagem especialista em Diabetes. "
                "Avalia as decisões dos alunos de 2º ano em Portugal. "
                "Sê rigoroso mas pedagógico. Usa Português de Portugal."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[)
    except Exception as e:
        st.error(f"Erro ao iniciar IA: {e}")

# --- 3. INTERFACE E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica: Insulinoterapia")

st.sidebar.header("Cenários Clínicos")

# Usamos aspas triplas para evitar o erro de 'unterminated string literal'
cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": """Cenário: Sr. Alberto, 65 anos, admitido após Enfarte. 
    Glicémia atual: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. 
    Apresenta-te e pede ao aluno para decidir a conduta.""",
    
    "🏥 Sr. Alberto (Jejum)": """Cenário: Sr. Alberto em jejum para cateterismo às 10h. 
    Glicémia: 135 mg/dL. Deve administrar a NPH da manhã? Pede a opinião ao aluno.""",
    
    "👵 D. Maria (Baixa Visão)": """Cenário: D. Maria, 70 anos, baixa visão. 
    Glicémia: 310 mg/dL. Como preparar a dose de forma segura? Pede ao aluno para explicar."""
}

for nome, prompt_cenario in cenarios.items():
    if st.sidebar.button(nome, use_container_width=True):
        try:
            response = st.session_state.chat_session.send_message(prompt_cenario)
            st.session_state.historico = response.text
        except Exception as e:
            st.error("Erro ou limite de quota. Aguarde 60 segundos.")

# --- 4. ÁREA DE DIÁLOGO ---
if "historico" in st.session_state:
    st.info("### 👨‍🏫 Orientação do Professor")
    st.markdown(st.session_state.historico)

user_input = st.chat_input("Escreva aqui a sua decisão clínica...")

if user_input:
    try:
        response = st.session_state.chat_session.send_message(user_input)
        st.session_state.historico = response.text
        st.rerun()
    except Exception as e:
        st.error("Erro na resposta da IA. Tente novamente em breve.")
