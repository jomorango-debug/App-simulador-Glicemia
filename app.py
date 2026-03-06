import streamlit as st
import google.generativeai as genai

# 1. Configurar a Chave
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Configure a GOOGLE_API_KEY nos Secrets do Streamlit.")
    st.stop()

# FORÇAR A VERSÃO V1 PARA EVITAR O ERRO 404
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')

st.title("🩺 Simulador de Enfermagem v3")

# 2. Inicialização do Chat (Usando o modelo estável v1)
if "chat" not in st.session_state:
    try:
        # Em 2026, este nome é o padrão de produção
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Conectado (v1)")
    except Exception as e:
        st.sidebar.error(f"Erro de Conexão: {e}")

# 3. Interface e Botões
st.sidebar.header("Cenários Clínicos")
cenarios = {
    "📍 Sr. Alberto (EAM)": "Inicie o cenário: Sr. Alberto, Pós-EAM, Glicémia 265 mg/dL. NPH 18UI e Aspart SOS.",
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
                st.error(f"Erro: {e}")

# 4. Mostrar o diálogo
if "texto" in st.session_state:
    st.divider()
    st.markdown(st.session_state.texto)

# Chat livre no fundo
prompt = st.chat_input("O que vai fazer?")
if prompt and "chat" in st.session_state:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.texto = res.text
        st.rerun()
    except Exception as e:
        st.error(f"Erro no chat: {e}")
