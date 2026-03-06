import streamlit as st
import google.generativeai as genai

# 1. Configurar a Chave
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Configure a GOOGLE_API_KEY nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🩺 Simulador de Enfermagem v3")

# 2. Inicialização do Chat (Forçando o modelo estável)
if "chat" not in st.session_state:
    try:
        # Este é o modelo 'Pro' original, o mais estável para APIs gratuitas
        model = genai.GenerativeModel("gemini-1.0-pro")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Sistema Online")
    except Exception as e:
        st.sidebar.error(f"Erro: {e}")

# 3. Interface e Botões
st.sidebar.header("Escolha o Caso")
cenarios = {
    "📍 Sr. Alberto (EAM)": "Cenário: Sr. Alberto, Pós-EAM, Glicémia 265. NPH 18UI e Aspart SOS. Comece.",
    "🏥 Sr. Alberto (Jejum)": "Cenário: Sr. Alberto, Jejum, Glicémia 135. Comece.",
    "👵 D. Maria (Visão)": "Cenário: D. Maria, baixa visão, glicémia 310. Comece."
}

for nome, comando in cenarios.items():
    if st.sidebar.button(nome):
        if "chat" in st.session_state:
            try:
                res = st.session_state.chat.send_message(comando)
                st.session_state.texto = res.text
            except Exception as e:
                st.error(f"Erro de Conexão: {e}")

# 4. Mostrar o diálogo
if "texto" in st.session_state:
    st.divider()
    st.markdown(st.session_state.texto)

# Chat livre no fundo
prompt = st.chat_input("O que vai fazer?")
if prompt and "chat" in st.session_state:
    res = st.session_state.chat.send_message(prompt)
    st.session_state.texto = res.text
    st.rerun()
