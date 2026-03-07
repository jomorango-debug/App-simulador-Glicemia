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
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Tu és um Professor de Enfermagem especialista em Diabetes. "
                "O teu objetivo é avaliar as decisões clínicas dos alunos de 2º ano em Portugal. "
                "Sê rigoroso mas pedagógico. Usa Português de Portugal. "
                "Foca-te na segurança do doente, farmacocinética das insulinas e técnica correta."
            )
        )
        # Inicializa a sessão com histórico vazio corretamente formatado
        st.session_state.chat_session = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        st.sidebar.error(f"Erro ao iniciar IA: {e}")

# --- 3. INTERFACE E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica: Insulinoterapia")
st.markdown("---")

st.sidebar.header("Cenários Clínicos")
st.sidebar.markdown("Selecione um caso para iniciar:")

# Dicionário de cenários com aspas triplas para segurança de sintaxe
cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": """Cenário: Sr. Alberto, 65 anos, admitido após Enfarte. 
    Glicémia atual: 265 mg/dL. Prescrição: Insulina NPH 18UI (SC) + Insulina Aspart SOS. 
    Apresenta-te como professor e pede ao aluno para decidir a conduta imediata.""",
    
    "🏥 Sr. Alberto (Jejum)": """Cenário: Sr. Alberto tem cateterismo marcado para as 10h e está em jejum. 
    Glicémia: 135 mg/dL. Ele questiona se deve administrar a NPH da manhã. 
    Pede ao aluno para justificar a decisão de administrar ou suspender.""",
    
    "👵 D. Maria (Baixa Visão)": """Cenário: D. Maria, 70 anos, vive sozinha e tem baixa visão grave. 
    Glicémia:
