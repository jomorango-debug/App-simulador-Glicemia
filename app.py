import streamlit as st
import google.generativeai as genai

# 1. Configuração de Segurança
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")
    st.stop()

st.title("🩺 Simulador de Enfermagem")

# 2. Inicialização do Modelo (Ajustado para 2026)
if "chat" not in st.session_state:
    try:
        # Usando o modelo mais estável para evitar o erro 404
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        # Em 2026, este é o nome estável que substitui as versões v1beta
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 3. Interface da Barra Lateral
st.sidebar.header("Cenários Clínicos")

# Definimos os comandos para os botões
cenarios = {
    "📍 Sr. Alberto (EAM)": "Inicie o cenário: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. NPH 18UI e Aspart SOS.",
    "🏥 Sr. Alberto (Jejum)": "Inicie o cenário: Sr. Alberto, Jejum para Cateterismo, Glicémia 135 mg/dL.",
    "👵 D. Maria (Visão)": "Inicie o cenário: D. Maria, 70 anos, baixa visão, glicémia 310 mg/dL."
}

for nome, comando in cenarios.items():
    if st.sidebar.button(nome):
        try:
            response = st.session_state.chat.send_message(comando)
            st.session_state.last_response = response.text
        except Exception as e:
            st.error(f"Erro ao carregar cenário: {e}")

# 4. Exibição da Resposta do Professor
if "last_response" in st.session_state:
    st.markdown("---")
    st.info("💡 **Orientação do Professor:**")
    st.markdown(st.session_state.last_response)

# 5. Interação Livre
st.markdown("---")
prompt = st.chat_input("Descreva a sua intervenção de enfermagem aqui...")
if prompt:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.last_response = res.text
        st.rerun()
    except Exception as e:
        st.error(f"Erro na resposta: {e}")
