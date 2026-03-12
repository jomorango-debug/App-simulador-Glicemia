import streamlit as st
import google.generativeai as genai

# 1. Configuração de Página
st.set_page_config(page_title="Simulador Enfermagem", layout="centered")

# 2. Barra Lateral: Chave API
with st.sidebar:
    st.header("🔑 Acesso")
    api_key = st.text_input("Introduza a sua Google API Key:", type="password")
    st.info("Obtenha a chave em: aistudio.google.com")

# 3. Bloqueio de Segurança
if not api_key:
    st.title("🩺 Simulador de Insulinoterapia")
    st.warning("⚠️ Insira a sua API Key na barra lateral para ativar o simulador.")
    st.stop()

# 4. Configuração da IA (Forçando a versão estável)
try:
    genai.configure(api_key=api_key)
    # Em 2026, o nome 'gemini-1.5-flash' é o padrão estável
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    st.sidebar.success("✅ Professor Online")
except Exception as e:
    st.error(f"Erro na Chave: {e}")
    st.stop()

# 5. Interface e Cenários
st.title("🩺 Casos Clínicos: Insulinoterapia")

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Caso 1: Glicémia 265 mg/dL", use_container_width=True):
        res = st.session_state.chat.send_message("Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. Comece a simulação.")
        st.session_state.last_res = res.text

with col2:
    if st.button("🏥 Caso 2: Doente em Jejum", use_container_width=True):
        res = st.session_state.chat.send_message("Cenário: Doente em jejum para cateterismo, glicémia 135 mg/dL. Deve administrar a NPH? Comece a simulação.")
        st.session_state.last_res = res.text

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
    except Exception as e:
        st.error("Erro de comunicação. Tente novamente em 60 segundos.")
