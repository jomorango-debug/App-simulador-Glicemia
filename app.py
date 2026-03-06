import streamlit as st
import google.generativeai as genai

# 1. Configuração de Segurança
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")
    st.stop()

st.title("🩺 Simulador de Enfermagem")

# 2. Motor "Detetive" de Modelos
if "chat" not in st.session_state:
    # Lista de nomes possíveis em 2026 (do mais novo para o mais estável)
    nomes_para_testar = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    
    model_found = False
    for nome in nomes_para_testar:
        try:
            model = genai.GenerativeModel(nome)
            # Teste rápido de conexão
            st.session_state.chat = model.start_chat(history=[])
            st.sidebar.success(f"✅ Ligado: {nome}")
            model_found = True
            break
        except:
            continue
            
    if not model_found:
        st.error("❌ Não foi possível encontrar nenhum modelo disponível. Verifique se a sua API Key no Google AI Studio está ativa.")

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
                response = st.session_state.chat.send_message(comando)
                st.session_state.last_response = response.text
            except Exception as e:
                st.error(f"Erro ao carregar cenário: {e}")

# 4. Exibição
if "last_response" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state.last_response)

prompt = st.chat_input("Decisão clínica...")
if prompt and "chat" in st.session_state:
    try:
        res = st.session_state.chat.send_message(prompt)
        st.session_state.last_response = res.text
        st.rerun()
    except:
        st.error("Erro na resposta.")
