import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE SEGURANÇA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Configuração Necessária: A API Key não foi encontrada nos Secrets do Streamlit.")
    st.stop()

# --- 2. CONFIGURAÇÃO DO MODELO ---
generation_config = {"temperature": 0.7, "top_p": 0.95, "max_output_tokens": 2048}
system_instruction = """
Tu és um Professor de Enfermagem (2º ano). O teu tom é clínico e pedagógico.
REGRAS: 1. Rápida = Abdómen. 2. Lenta/NPH = Coxas/Nádegas. 
3. Jejum: Se mantiver NPH total, simula hipoglicémia. 
4. Baixa Visão: Exige 'Técnica dos Cliques'.
Usa Português de Portugal.
"""

model = genai.GenerativeModel(
    model_name="gemini-3-flash", # Nome oficial para 2026
    generation_config=generation_config,
    system_instruction=system_instruction,
)

# --- 3. FUNÇÃO PDF ---
def generate_pdf(history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatorio de Simulacao Clinica - Enfermagem", ln=True, align="C")
    pdf.ln(10)
    for message in history:
        role = "ALUNO" if message.role == "user" else "PROFESSOR"
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"{role}:", ln=True)
        pdf.set_font("Arial", "", 11)
        clean_text = message.parts[0].text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 8, clean_text)
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. INTERFACE ---
st.set_page_config(page_title="Simulador Enfermagem", page_icon="🩺", layout="wide")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

with st.sidebar:
    st.header("Cenários")
    if st.button("📍 Sr. Alberto (EAM)"):
        st.session_state.prompt_input = "Inicie: Sr. Alberto, Pós-EAM. Glicémia: 265 mg/dL. NPH 18UI e Aspart SOS."
    if st.button("🏥 Sr. Alberto (Jejum)"):
        st.session_state.prompt_input = "Inicie: Sr. Alberto, Jejum (NPO). Glicémia: 135 mg/dL."
    if st.button("👵 D. Maria (Visão)"):
        st.session_state.prompt_input = "Inicie: D. Maria, baixa visão. Glicémia: 310 mg/dL."
    
    if len(st.session_state.chat_session.history) > 0:
        pdf_data = generate_pdf(st.session_state.chat_session.history)
        st.download_button("📥 Baixar Relatório PDF", pdf_data, "relatorio.pdf", "application/pdf")

for message in st.session_state.chat_session.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Sua decisão...")
if "prompt_input" in st.session_state:
    user_input = st.session_state.prompt_input
    del st.session_state.prompt_input

if user_input:
    with st.chat_message("user"): st.markdown(user_input)
    response = st.session_state.chat_session.send_message(user_input)
    with st.chat_message("assistant"): st.markdown(response.text)
