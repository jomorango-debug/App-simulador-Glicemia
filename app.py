import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador de Enfermagem", page_icon="🩺", layout="wide")

# --- 2. CONFIGURAÇÃO DA IA ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Erro: GOOGLE_API_KEY não encontrada nos Secrets do Streamlit.")
    st.stop()

# Inicialização do Modelo e da Sessão de Chat
if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=(
                "Tu és um Professor de Enfermagem especialista em Diabetes em Portugal. "
                "Avalia decisões de alunos de 2º ano. Sê rigoroso e pedagógico. "
                "Usa Português de Portugal. Foca na segurança e farmacocinética."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        st.sidebar.error(f"Erro ao iniciar IA: {e}")

# --- 3. INTERFACE E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica: Insulinoterapia")
st.markdown("---")

st.sidebar.header("Cenários Clínicos")
st.sidebar.markdown("Selecione um caso:")

# Definindo cenários de forma linear para evitar erros de aspas triplas
cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": "Cenário: Sr. Alberto, 65 anos, admitido após Enfarte. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. Peça ao aluno para decidir a conduta.",
    "🏥 Sr. Alberto (Jejum)": "Cenário: Sr. Alberto em jejum para cateterismo. Glicémia: 135 mg/dL. Deve administrar a NPH da manhã? Peça justificativa.",
    "👵 D. Maria (Visão)": "Cenário: D. Maria, 70 anos, baixa visão grave. Glicémia: 310 mg/dL. Como orientar a preparação segura da dose? Avalie a técnica dos cliques."
}

# Botões na barra lateral
for nome, prompt_cenario in cenarios.items():
    if st.sidebar.button(nome, use_container_width=True):
        try:
            response = st.session_state.chat_session.send_message(prompt_cenario)
            st.session_state.historico = response.text
        except Exception as e:
            st.error("Limite de quota atingido ou erro. Aguarde 60 segundos.")

# --- 4. ÁREA DE DIÁLOGO ---
if "historico" in st.session_state:
    with st.container():
        st.info("### 👨‍🏫 Orientação do Professor")
        st.markdown(st.session_state.historico)

st.markdown("---")

user_input = st.chat_input("Escreva aqui a sua decisão ou resposta...")

if user_input:
    if "chat_session" in st.session_state:
        try:
            response = st.session_state.chat_session.send_message(user_input)
            st.session_state.historico = response.text
            st.rerun()
        except Exception as e:
            st.error("Erro na comunicação. Tente novamente em 1 minuto.")
