import streamlit as st
import google.generativeai as genai

# 1. Tentar ler a Chave dos Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")
    st.stop()

st.title("🩺 Simulador de Enfermagem")

# 2. Testar conexão e definir modelo
# Em 2026, o nome padrão é gemini-2.0-flash ou gemini-1.5-flash para estabilidade
MODELO = "gemini-1.5-flash" 

if "chat" not in st.session_state:
    try:
       # 2. Testar conexão e definir modelo com nomes universais
MODELO_NOME = "models/gemini-1.5-flash" # Prefixo 'models/' é obrigatório em certas versões

if "chat" not in st.session_state:
    try:
        # Tenta inicializar com o nome completo
        model = genai.GenerativeModel(MODELO_NOME)
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        # Se falhar, tenta o nome curto
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            st.session_state.chat = model.start_chat(history=[])
            st.sidebar.success("✅ Professor Online (v2)")
        except:
            st.sidebar.error(f"Erro de Conexão: {e}")

# 3. Interface Simples
st.sidebar.header("Cenários")
opcoes = {
    "Sr. Alberto (EAM)": "Inicie cenário: Sr. Alberto, Pós-EAM, Glicémia 265.",
    "Sr. Alberto (Jejum)": "Inicie cenário: Sr. Alberto, Jejum, Glicémia 135.",
    "D. Maria (Visão)": "Inicie cenário: D. Maria, Baixa visão, Glicémia 310."
}

for nome, comando in opcoes.items():
    if st.sidebar.button(nome):
        response = st.session_state.chat.send_message(comando)
        st.session_state.last_response = response.text

if "last_response" in st.session_state:
    st.markdown(st.session_state.last_response)

# Caixa de texto livre
prompt = st.chat_input("Escreva a sua decisão clínica...")
if prompt:
    res = st.session_state.chat.send_message(prompt)
    st.markdown(res.text)
