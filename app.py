import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador de Enfermagem", page_icon="🩺", layout="wide")

# --- 2. CONFIGURAÇÃO DA IA ---
# Tenta ler a chave dos secrets do Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Erro: GOOGLE_API_KEY não encontrada nos Secrets do Streamlit.")
    st.stop()

# Inicialização do Modelo (Usando o Gemini 1.5 Flash para maior estabilidade de quota)
if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Tu és um Professor de Enfermagem especialista em Diabetes. "
                "O teu objetivo é avaliar as decisões clínicas dos alunos de 2º ano. "
                "Sê rigoroso mas pedagógico. Usa Português de Portugal. "
                "Se o aluno cometer um erro grave (ex: dose errada ou local de absorção inadequado), "
                "explica as consequências fisiológicas (ex: risco de hipoglicémia ou lipodistrofia)."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Erro ao iniciar o motor de IA: {e}")

# --- 3. INTERFACE E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica: Insulinoterapia")
st.markdown("---")

st.sidebar.header("Cenários Clínicos")
st.sidebar.markdown("Escolha um caso para iniciar a simulação:")

cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": (
        "Cenário: Sr. Alberto, 65 anos, admitido após Enfarte Agudo do Miocárdio. "
        "Glicémia atual: 265 mg/dL
