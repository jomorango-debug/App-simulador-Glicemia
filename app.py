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

# 2. Inicialização do Modelo e Chat
if "chat" not in st.session_state:
    try:
        # Tentamos o nome mais compatível para evitar o erro 'NotFound'
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        st.sidebar.error(f"Falha na conexão: {e}")

# 3. Interface da Barra Lateral
st.sidebar.header("Cenários Clínicos")
opcoes = {
    "📍 Sr. Alberto (EAM)": "Inicie o cenário: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS.",
    "🏥 Sr. Alberto (Jejum)": "Inicie o cenário: Sr. Alberto, Jejum para Cateterismo, Glicémia 135 mg/dL.",
    "👵 D. Maria (Visão)": "Inicie o cenário: D. Maria, 70 anos, baixa visão, glicémia 310 mg/dL."
}

for nome, comando in opcoes.items():
    if st.sidebar.button(nome):
        try:
            response = st.session_state.chat.send_message(comando)
            st.session_state.last_response = response.text
        except Exception as e:
            st.error(f"Erro ao enviar mensagem: {e}")

# 4. Exibição das Respostas
if "last_response" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state.last_response)

# 5. Caixa de Chat Livre
st.markdown("---")
prompt = st.chat_input("Escreva a sua decisão de enfermagem...")
if prompt:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.last_response = res.text
        st.rerun() # Atualiza a página para mostrar a resposta
    except Exception as e:
        st.error(f"Erro no chat: {e}")
