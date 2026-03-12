import streamlit as st
import google.generativeai as genai

# 1. Configuração Básica
st.set_page_config(page_title="Simulador Enfermagem", layout="wide")

# 2. Barra Lateral para a Chave
with st.sidebar:
    st.title("Configuração")
    api_key = st.text_input("Insere a tua Google API Key:", type="password")
    st.info("Obtém a chave em: aistudio.google.com")

# 3. Inicialização do Modelo (Só corre se houver chave)
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos o Flash que é mais rápido e evita que a app fique 'a pensar'
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            # Mensagem de sistema enviada silenciosamente para definir o papel do bot
            st.session_state.chat.send_message("Age como um Professor de Enfermagem em Portugal. Avalia as decisões dos alunos de forma rigorosa e pedagógica.")
        
        st.sidebar.success("✅ Professor Online")
    except Exception as e:
        st.sidebar.error(f"Erro de ligação: {e}")

# 4. Interface Principal
st.title("🩺 Simulador de Insulinoterapia")

# Cenários Rápidos
col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Caso: Sr. Alberto (Glicémia 265)"):
        st.session_state.prompt = "Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. O que fazes?"
with col2:
    if st.button("🏥 Caso: Jejum para Cateterismo"):
        st.session_state.prompt = "Cenário: Doente em jejum, glicémia 135 mg/dL. Deve administrar a NPH?"

# Processar o envio da mensagem
if "prompt" in st.session_state:
    try:
        response = st.session_state.chat.send_message(st.session_state.prompt)
        st.markdown("### 👨‍🏫 Feedback do Professor:")
        st.write(response.text)
        del st.session_state.prompt # Limpa para o próximo clique
    except Exception as e:
        st.error("A IA demorou muito a responder. Tenta novamente.")

# Chat livre
user_input = st.chat_input("Responde ao professor...")
if user_input and api_key:
    response = st.session_state.chat.send_message(user_input)
    st.markdown(f"**Professor:** {response.text}")
