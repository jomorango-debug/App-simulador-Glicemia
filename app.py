import streamlit as st
import google.generativeai as genai
from google.generativeai import caching
import os

# 1. Configurar a Chave (Lida dos Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Erro: Configure a GOOGLE_API_KEY nos Secrets.")
    st.stop()

# FORÇAR CONFIGURAÇÃO DE PRODUÇÃO V1
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🩺 Simulador de Enfermagem v3")

# 2. Inicialização do Chat com Nome de Produção 2026
if "chat" not in st.session_state:
    try:
        # Usamos o nome de modelo que a Google estabilizou para v1
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Conectado (Produção v1)")
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
                # O segredo: forçar o transporte para contornar o erro 404
                res = st.session_state.chat.send_message(comando)
                st.session_state.texto = res.text
            except Exception as e:
                # Se der erro 404 aqui, a chave precisa de ser recreada
                st.error(f"Erro ao carregar cenário: {e}")

# 4. Mostrar o diálogo
if "texto" in st.session_state:
    st.divider()
    st.markdown(st.session_state.texto)

# Chat livre
prompt = st.chat_input("O que vai fazer?")
if prompt and "chat" in st.session_state:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.texto = res.text
        st.rerun()
    except Exception as e:
        st.error("Aguarde 60 segundos (Limite de Quota).")
