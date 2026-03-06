import streamlit as st
import google.generativeai as genai

# 1. Configurar a Chave (Lida dos Secrets do Streamlit)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: GOOGLE_API_KEY não configurada nos Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🩺 Simulador de Enfermagem v3")

# 2. Inicialização do Modelo Estável
if "chat" not in st.session_state:
    try:
        # Em 2026, 'gemini-1.5-flash' no SDK v0.8.3+ já aponta para v1 automaticamente
        model = genai.GenerativeModel("gemini-pro")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        st.sidebar.error(f"Erro de Conexão: {e}")

# 3. Interface e Cenários
st.sidebar.header("Cenários Clínicos")
cenarios = {
    "📍 Sr. Alberto (EAM)": "Inicie o cenário: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS.",
    "🏥 Sr. Alberto (Jejum)": "Inicie o cenário: Sr. Alberto, Jejum para Cateterismo, Glicémia 135 mg/dL.",
    "👵 D. Maria (Visão)": "Inicie o cenário: D. Maria, 70 anos, baixa visão, glicémia 310 mg/dL."
}

for nome, comando in cenarios.items():
    if st.sidebar.button(nome):
        if "chat" in st.session_state:
            try:
                res = st.session_state.chat.send_message(comando)
                st.session_state.texto = res.text
            except Exception as e:
                st.error(f"Aguarde 60 segundos (Limite de Quota) ou Erro: {e}")

# 4. Mostrar o diálogo
if "texto" in st.session_state:
    st.divider()
    st.markdown(st.session_state.texto)

# Chat livre no fundo
prompt = st.chat_input("O que vai fazer agora?")
if prompt and "chat" in st.session_state:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.texto = res.text
        st.rerun()
    except Exception as e:
        st.error("Erro no chat. Tente novamente em 1 minuto.")
