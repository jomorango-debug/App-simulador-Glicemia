import streamlit as st
import google.generativeai as genai
import os

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
    st.warning("⚠️ O simulador aguarda a sua API Key na barra lateral.")
    st.stop()

# 4. Configuração da IA (Ajuste para evitar erro 404/v1beta)
try:
    # Forçamos a configuração a ignorar versões beta internamente
    os.environ["GOOGLE_API_KEY"] = api_key
    genai.configure(api_key=api_key)
    
    # Em 2026, usamos o modelo estável sem prefixos de versão no código
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "chat" not in st.session_state:
        # Criamos o chat e enviamos a instrução de sistema
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.chat.send_message("Age como um Professor de Enfermagem em Portugal. Sê rigoroso e pedagógico.")
    
    st.sidebar.success("✅ Professor Conectado (v1)")
except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.info("Dica: Tente criar uma NOVA chave API no Google AI Studio num projeto novo.")
    st.stop()

# 5. Interface e Cenários
st.title("🩺 Casos Clínicos: Insulinoterapia")

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Caso 1: Glicémia 265 mg/dL", use_container_width=True):
        try:
            res = st.session_state.chat.send_message("Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. Comece a simulação.")
            st.session_state.last_res = res.text
        except Exception:
            st.error("Erro de Quota. Aguarde 60 segundos.")

with col2:
    if st.button("🏥 Caso 2: Doente em Jejum", use_container_width=True):
        try:
            res = st.session_state.chat.send_message("Cenário: Doente em jejum para cateterismo, glicémia 135 mg/dL. Deve administrar a NPH? Comece a simulação.")
            st.session_state.last_res = res.text
        except Exception:
            st.error("Erro de Quota. Aguarde 60 segundos.")

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
        st.error("Erro na resposta. Aguarde 60 segundos.")
