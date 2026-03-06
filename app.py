import streamlit as st
import google.generativeai as genai

# 1. Configuração de Segurança (Secrets)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")
    st.stop()

st.title("🩺 Simulador de Enfermagem")

# 2. Inicialização do Modelo (Fechando o bloco try corretamente)
if "chat" not in st.session_state:
    try:
        # Usamos gemini-1.5-flash-latest por ser o mais estável na API v1
        model = genai.GenerativeModel("gemini-2.0-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Conectado")
    except Exception as e:
        st.sidebar.error("⚠️ Erro de Ligação")
        st.session_state.chat = None

# 3. Interface da Barra Lateral
st.sidebar.header("Cenários Clínicos")
cenarios = {
    "📍 Sr. Alberto (EAM)": "Inicie o cenário: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. NPH 18UI e Aspart SOS.",
    "🏥 Sr. Alberto (Jejum)": "Inicie o cenário: Sr. Alberto, Jejum para Cateterismo, Glicémia 135 mg/dL.",
    "👵 D. Maria (Visão)": "Inicie o cenário: D. Maria, 70 anos, baixa visão, glicémia 310 mg/dL."
}

for nome, comando in cenarios.items():
    if st.sidebar.button(nome):
        if st.session_state.chat:
            try:
                response = st.session_state.chat.send_message(comando)
                st.session_state.last_response = response.text
            except Exception as e:
                st.error(f"Erro ao carregar: {e}")
        else:
            st.error("O motor de IA não está ativo. Verifique a API Key.")

# 4. Exibição das Respostas e Chat
if "last_response" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state.last_response)

st.markdown("---")
prompt = st.chat_input("Escreva a sua decisão clínica...")
if prompt and st.session_state.chat:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.last_response = res.text
        st.rerun()
    except Exception as e:
        st.error(f"Erro no chat: {e}")
