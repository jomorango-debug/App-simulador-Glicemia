import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador de Enfermagem v2", page_icon="🩺", layout="wide")

# --- 2. BARRA LATERAL: CONFIGURAÇÃO ---
with st.sidebar:
    st.header("🔑 Configuração")
    
    api_key_input = st.text_input(
        "Introduza a sua Google API Key:", 
        type="password", 
        placeholder="AIzaSy...",
        help="A chave é apagada ao fechar o navegador."
    )

    if api_key_input:
        try:
            # Configuração forçada para evitar erros de versão
            genai.configure(api_key=api_key_input)
            st.success("✅ Sistema Pronto")
        except Exception as e:
            st.error(f"Erro: {e}")

# --- 3. MOTOR DE IA (VERSÃO PRO) ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if api_key_input and st.session_state.chat_session is None:
    try:
        # Mudamos para o 1.5-pro, que é mais robusto para diagnósticos
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction="És um Professor de Enfermagem em Portugal. Avalia as decisões dos alunos sobre insulina com rigor pedagógico."
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error("Erro ao carregar o Professor. Tente uma nova chave API.")

# --- 4. INTERFACE E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica")

cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": "Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. O que faz?",
    "🏥 Sr. Alberto (Jejum)": "Cenário: Sr. Alberto em jejum para cateterismo. Glicémia: 135 mg/dL. Deve administrar a NPH?",
    "👵 D. Maria (Visão)": "Cenário: D. Maria, baixa visão. Glicémia: 310 mg/dL. Como orientar a preparação segura?"
}

col1, col2, col3 = st.columns(3)
for i, (nome, prompt) in enumerate(cenarios.items()):
    with [col1, col2, col3][i]:
        if st.button(nome, use_container_width=True):
            if st.session_state.chat_session:
                try:
                    res = st.session_state.chat_session.send_message(prompt)
                    st.session_state.historico = res.text
                except Exception:
                    st.error("Sem quota. Tente novamente em 60 segundos.")
            else:
                st.warning("Insira a chave na barra lateral.")

# --- 5. EXIBIÇÃO ---
if "historico" in st.session_state:
    st.info(st.session_state.historico)

user_input = st.chat_input("Sua decisão...")
if user_input and st.session_state.chat_session:
    try:
        res = st.session_state.chat_session.send_message(user_input)
        st.session_state.historico = res.text
        st.rerun()
    except:
        st.error("Erro de quota.")
