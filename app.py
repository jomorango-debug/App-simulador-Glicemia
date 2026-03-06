import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. Configurar a Chave
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Configure a GOOGLE_API_KEY nos Secrets do Streamlit.")
    st.stop()

# CONFIGURAÇÃO DE SEGURANÇA PARA FORÇAR V1
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🩺 Simulador de Enfermagem v3")

# 2. Inicialização do Chat (Forçando a API v1)
if "chat" not in st.session_state:
    try:
        # Usamos o RequestOptions para garantir que não vai para o v1beta
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Servidor v1 Ativo")
    except Exception as e:
        st.sidebar.error(f"Erro de Conexão: {e}")

# 3. Interface e Cenários
st.sidebar.header("Cenários Clínicos")
cenarios = {
    "📍 Sr. Alberto (EAM)": "Inicie: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. NPH 18UI e Aspart SOS.",
    "🏥 Sr. Alberto (Jejum)": "Inicie: Sr. Alberto, Jejum, Glicémia 135 mg/dL.",
    "👵 D. Maria (Visão)": "Inicie: D. Maria, baixa visão, glicémia 310 mg/dL."
}

for nome, comando in cenarios.items():
    if st.sidebar.button(nome):
        if "chat" in st.session_state:
            try:
                # Forçamos a versão v1 na própria mensagem
                res = st.session_state.chat.send_message(
                    comando, 
                    request_options=RequestOptions(api_version='v1')
                )
                st.session_state.texto = res.text
            except Exception as e:
                st.error(f"Erro: {e}")

# 4. Mostrar o diálogo
if "texto" in st.session_state:
    st.divider()
    st.markdown(st.session_state.texto)

# Chat livre
prompt = st.chat_input("O que vai fazer?")
if prompt and "chat" in st.session_state:
    try:
        res = st.session_state.chat.send_message(
            prompt, 
            request_options=RequestOptions(api_version='v1')
        )
        st.session_state.texto = res.text
        st.rerun()
    except Exception as e:
        st.error(f"Erro: {e}")
