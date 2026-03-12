import streamlit as st
import google.generativeai as genai

# 1. Configuração de Página (Deve ser a primeira linha de Streamlit)
st.set_page_config(page_title="Simulador Enfermagem", layout="centered")

st.title("🩺 Simulador de Insulinoterapia")

# 2. Área de Configuração na Sidebar
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Insira a sua Google API Key:", type="password")
    st.markdown("[Obter chave aqui](https://aistudio.google.com/)")

# 3. Lógica Principal
if not api_key:
    st.warning("⚠️ Por favor, insira a sua API Key na barra lateral para começar.")
    st.stop() # Isto para o loop aqui até haver uma chave

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Inicializar chat se não existir
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.sidebar.success("✅ Professor Online")

    # Botões de Cenário
    st.subheader("Selecione um Cenário Clínico")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📍 Sr. Alberto (Glicémia 265)"):
            response = st.session_state.chat.send_message("Cenário: Sr. Alberto, 65 anos, Pós-EAM. Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. Comece a simulação.")
            st.session_state.resposta = response.text
            
    with col2:
        if st.button("🏥 Jejum para Cateterismo"):
            response = st.session_state.chat.send_message("Cenário: Doente em jejum, glicémia 135 mg/dL. Deve administrar a NPH? Comece a simulação.")
            st.session_state.resposta = response.text

    # Exibição do Diálogo
    if "resposta" in st.session_state:
        st.info(st.session_state.resposta)

    # Chat de interação
    user_input = st.chat_input("Responda ao professor...")
    if user_input:
        response = st.session_state.chat.send_message(user_input)
        st.session_state.resposta = response.text
        st.rerun()

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
