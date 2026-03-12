import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# 1. Configuração de Página
st.set_page_config(page_title="Simulador Enfermagem", layout="centered")

# 2. Barra Lateral: Chave API
with st.sidebar:
    st.header("🔑 Acesso ao Professor")
    api_key = st.text_input("Introduza a sua Google API Key:", type="password")
    st.info("Obtenha a chave em: aistudio.google.com")

# 3. Bloqueio de Segurança
if not api_key:
    st.title("🩺 Simulador de Insulinoterapia")
    st.warning("⚠️ O simulador está à espera da sua API Key na barra lateral.")
    st.stop()

# 4. Configuração da IA (Ajuste Crítico para evitar erro 404)
try:
    # Forçamos a API a usar a rota estável v1
    options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com")
    genai.configure(api_key=api_key, client_options=options)
    
    # Criamos o modelo garantindo que não usamos v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        # Mensagem invisível para definir o comportamento
        st.session_state.chat.send_message("Age como um Professor de Enfermagem em Portugal. Sê pedagógico.")
    
    st.sidebar.success("✅ Professor Conectado")
except Exception as e:
    st.error(f"Erro de Configuração: {e}")
    st.stop()

# 5. Interface e Cenários
st.title("🩺 Casos Clínicos: Insulinoterapia")

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Caso 1: Glicémia 265 mg/dL", use_container_width=True):
        try:
            res = st.session_state.chat.send_message("Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. Comece a simulação.")
            st.session_state.last_res = res.text
        except Exception as e:
            st.error(f"Erro ao iniciar cenário: {e}")

with col2:
    if st.button("🏥 Caso 2: Doente em Jejum", use_container_width=True):
        try:
            res = st.session_state.chat.send_message("Cenário: Doente em jejum para cateterismo, glicémia 135 mg/dL. Deve administrar a NPH? Comece a simulação.")
            st.session_state.last_res = res.text
        except Exception as e:
            st.error(f"Erro ao iniciar cenário: {e}")

# Mostrar Feedback
if "last_res" in st.session_state:
    st.markdown("---")
    st.info(st.session_state.last_res)

# Interação
aluno_input = st.chat_input("Responda ao professor...")
if aluno_input:
    try:
        res = st.session_state.chat.send_message(aluno_input)
        st.session_state.last_res = res.text
        st.rerun()
    except Exception:
        st.error("Erro na resposta. Aguarde 60 segundos (Limite de Quota).")
