import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador de Enfermagem v2", page_icon="🩺", layout="wide")

# --- 2. BARRA LATERAL: SEGURANÇA E CONFIGURAÇÃO DA CHAVE API ---
with st.sidebar:
    st.header("🔑 Configuração de Segurança")
    
    # Instruções para o utilizador obter a sua própria chave
    with st.expander("Como obter a sua chave API?"):
        st.markdown("""
        1. Vai ao [Google AI Studio](https://aistudio.google.com/).
        2. Clica em **'Get API key'**.
        3. Seleciona **'Create API key in new project'**.
        4. Copia a chave e cola no campo abaixo.
        """)
    
    # Campo de entrada com máscara (tipo password) para locais públicos
    api_key_input = st.text_input(
        "Introduza a sua Google API Key:", 
        type="password", 
        placeholder="AIzaSy...",
        help="A chave é mantida apenas na memória desta sessão e NÃO é gravada no servidor."
    )

    if api_key_input:
        try:
            genai.configure(api_key=api_key_input)
            st.success("✅ Professor de IA Ativado!")
        except Exception as e:
            st.error(f"Erro na chave: {e}")
    else:
        st.warning("⚠️ O Professor está offline. Insira a chave para começar.")

# --- 3. INICIALIZAÇÃO DO MOTOR DE IA ---
# Criamos a sessão de chat apenas se a chave estiver presente
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if api_key_input and st.session_state.chat_session is None:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Tu és um Professor de Enfermagem especialista em Diabetes em Portugal. "
                "O teu objetivo é avaliar decisões clínicas de alunos de 2º ano. "
                "Sê rigoroso mas pedagógico. Usa Português de Portugal. "
                "Foca-te na segurança do doente, na farmacocinética das insulinas e na técnica correta."
            )
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Erro ao inicializar o Professor: {e}")

# --- 4. INTERFACE PRINCIPAL E CENÁRIOS ---
st.title("🩺 Simulador de Decisão Clínica: Insulinoterapia")
st.markdown("---")

st.sidebar.header("Cenários Clínicos")
cenarios = {
    "📍 Sr. Alberto (Pós-EAM)": "Cenário: Sr. Alberto, 65 anos, admitido após Enfarte (EAM). Glicémia: 265 mg/dL. Prescrição: NPH 18UI e Aspart SOS. O que faz primeiro?",
    "🏥 Sr. Alberto (Jejum)": "Cenário: Sr. Alberto está em jejum para cateterismo às 10h. Glicémia: 135 mg/dL. Deve administrar a NPH das 8h?",
    "👵 D. Maria (Baixa Visão)": "Cenário: D. Maria, 70 anos, baixa visão grave. Glicémia: 310 mg/dL. Como garante que ela prepara a dose correta sozinha?"
}

# Botões de cenário na barra lateral
for nome, prompt_cenario in cenarios.items():
    if st.sidebar.button(nome, use_container_width=True):
        if st.session_state.chat_session:
            try:
                response = st.session_state.chat_session.send_message(prompt_cenario)
                st.session_state.historico = response.text
            except Exception as e:
                st.error("Erro na comunicação. Verifique se a chave tem quota disponível ou se é válida.")
        else:
            st.error("Por favor, insira a chave API na barra lateral primeiro.")

# --- 5. ÁREA DE DIÁLOGO E FEEDBACK ---
if "historico" in st.session_state:
    with st.container():
        st.info("### 👨‍🏫 Resposta do Professor")
        st.markdown(st.session_state.historico)

st.markdown("---")

# Campo de Resposta do Aluno
user_input = st.chat_input("Escreva aqui a sua decisão clínica ou resposta...")

if user_input:
    if st.session_state.chat_session:
        try:
            response = st.session_state.chat_session.send_message(user_input)
            st.session_state.historico = response.text
            st.rerun() # Atualiza para mostrar a resposta imediata
        except Exception as e:
            st.error("Erro ao processar resposta. Tente novamente em 60 segundos.")
    else:
        st.error("Insira a chave API para interagir com o Professor.")
