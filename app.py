{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import google.generativeai as genai\
from fpdf import FPDF\
from datetime import datetime\
\
# --- 1. CONFIGURA\'c7\'c3O DE SEGURAN\'c7A ---\
# No Streamlit Cloud, configura a chave em Settings > Secrets como: GOOGLE_API_KEY = "sua_chave"\
try:\
    API_KEY = st.secrets["GOOGLE_API_KEY"]\
    genai.configure(api_key=API_KEY)\
except Exception:\
    st.error("\uc0\u9888 \u65039  Configura\'e7\'e3o Necess\'e1ria: A API Key n\'e3o foi encontrada nos Secrets do Streamlit.")\
    st.stop()\
\
# --- 2. CONFIGURA\'c7\'c3O DO MODELO (PROFESSOR DE ENFERMAGEM) ---\
generation_config = \{\
    "temperature": 0.7,\
    "top_p": 0.95,\
    "max_output_tokens": 2048,\
\}\
\
system_instruction = """\
Tu \'e9s um Professor de Enfermagem de uma Licenciatura (2\'ba ano). O teu tom \'e9 cl\'ednico e pedag\'f3gico.\
REGRAS T\'c9CNICAS:\
1. Localiza\'e7\'e3o: Insulina R\'e1pida/Ultrarr\'e1pida = ABD\'d3MEN. Insulina Lenta/NPH = COXAS ou N\'c1DEGAS.\
2. Jejum (NPO): Se o aluno mantiver a dose total de NPH em jejum para exame, descreve complica\'e7\'f5es de hipoglic\'e9mia no cateterismo.\
3. Baixa Vis\'e3o: Exige que o aluno ensine a "T\'e9cnica dos Cliques" da caneta \'e0 D. Maria.\
4. Seguran\'e7a: Se o aluno errar dose ou local, interrompe com "\uc0\u9888 \u65039  ERRO DE SEGURAN\'c7A" e descreve sintomas (palpita\'e7\'f5es, confus\'e3o).\
5. Linguagem: Usa estritamente Portugu\'eas de Portugal.\
"""\
\
model = genai.GenerativeModel(\
    model_name="gemini-1.5-flash",\
    generation_config=generation_config,\
    system_instruction=system_instruction,\
)\
\
# --- 3. FUN\'c7\'c3O PARA GERAR RELAT\'d3RIO PDF ---\
def generate_pdf(history):\
    pdf = FPDF()\
    pdf.add_page()\
    pdf.set_font("Arial", "B", 16)\
    pdf.cell(200, 10, "Relatorio de Simulacao Clinica - Enfermagem", ln=True, align="C")\
    pdf.set_font("Arial", "", 10)\
    pdf.cell(200, 10, f"Data: \{datetime.now().strftime('%d/%m/%Y %H:%M')\}", ln=True, align="C")\
    pdf.ln(10)\
\
    for message in history:\
        role = "ALUNO" if message.role == "user" else "PROFESSOR"\
        pdf.set_font("Arial", "B", 11)\
        pdf.cell(0, 10, f"\{role\}:", ln=True)\
        pdf.set_font("Arial", "", 11)\
        # Limpar caracteres especiais para evitar erros no FPDF (latin-1)\
        clean_text = message.parts[0].text.encode('latin-1', 'ignore').decode('latin-1')\
        pdf.multi_cell(0, 8, clean_text)\
        pdf.ln(2)\
    \
    return pdf.output(dest='S').encode('latin-1')\
\
# --- 4. INTERFACE STREAMLIT ---\
st.set_page_config(page_title="Simulador Enfermagem", page_icon="\uc0\u55358 \u56954 ", layout="wide")\
\
# Estilo para os bot\'f5es e interface\
st.markdown("""\
    <style>\
    .stButton>button \{ width: 100%; border-radius: 5px; height: 3em; background-color: #f0f2f6; \}\
    .stDownloadButton>button \{ width: 100%; background-color: #2ecc71; color: white; \}\
    </style>\
    """, unsafe_allow_html=True)\
\
st.title("\uc0\u55358 \u56954  Simulador de Decis\'e3o: Insulinoterapia")\
st.caption("Suporte \'e0 tomada de decis\'e3o para estudantes do 2\'ba ano de Enfermagem")\
\
# Inicializar sess\'e3o de chat\
if "chat_session" not in st.session_state:\
    st.session_state.chat_session = model.start_chat(history=[])\
\
# --- BARRA LATERAL COM BOT\'d5ES ---\
with st.sidebar:\
    st.header("Escolha o Cen\'e1rio")\
    \
    if st.button("\uc0\u55357 \u56525  Cen\'e1rio 1: Sr. Alberto (EAM)"):\
        st.session_state.prompt_input = "Inicie o Cen\'e1rio 1: Sr. Alberto, 64 anos, P\'f3s-EAM. Glic\'e9mia: 265 mg/dL. Prescri\'e7\'e3o: NPH 18UI e Aspart SOS."\
    \
    if st.button("\uc0\u55356 \u57317  Cen\'e1rio 2: Sr. Alberto (Jejum)"):\
        st.session_state.prompt_input = "Inicie o Cen\'e1rio 2: Sr. Alberto, em jejum (NPO) para Cateterismo. Glic\'e9mia: 135 mg/dL. Qual a conduta?"\
    \
    if st.button("\uc0\u55357 \u56437  Cen\'e1rio 3: D. Maria (Baixa Vis\'e3o)"):\
        st.session_state.prompt_input = "Inicie o Cen\'e1rio 3: D. Maria, 70 anos, baixa vis\'e3o. Glic\'e9mia: 310 mg/dL. Como administrar e educar a doente?"\
\
    st.divider()\
    \
    if st.button("\uc0\u55357 \u56538  Tabela de Apoio T\'e9cnia"):\
        st.session_state.prompt_input = "Professor, pode mostrar a tabela de picos de a\'e7\'e3o e locais de elei\'e7\'e3o?"\
\
    # Op\'e7\'e3o de Download do PDF\
    if len(st.session_state.chat_session.history) > 0:\
        st.subheader("Finalizar Aula")\
        try:\
            pdf_data = generate_pdf(st.session_state.chat_session.history)\
            st.download_button(\
                label="\uc0\u55357 \u56549  Descarregar Relat\'f3rio PDF",\
                data=pdf_data,\
                file_name=f"relatorio_enfermagem_\{datetime.now().strftime('%Y%m%d_%H%M')\}.pdf",\
                mime="application/pdf"\
            )\
        except Exception as e:\
            st.error("Erro ao gerar PDF. Continue a simula\'e7\'e3o.")\
\
# --- JANELA DE CHAT PRINCIPAL ---\
for message in st.session_state.chat_session.history:\
    role = "user" if message.role == "user" else "assistant"\
    with st.chat_message(role):\
        st.markdown(message.parts[0].text)\
\
# Capturar input do chat ou dos bot\'f5es\
user_input = st.chat_input("Descreva a sua interven\'e7\'e3o de enfermagem...")\
\
# L\'f3gica para processar bot\'f5es da barra lateral\
if "prompt_input" in st.session_state:\
    user_input = st.session_state.prompt_input\
    del st.session_state.prompt_input\
\
if user_input:\
    with st.chat_message("user"):\
        st.markdown(user_input)\
    \
    response = st.session_state.chat_session.send_message(user_input)\
    \
    with st.chat_message("assistant"):\
        st.markdown(response.text)}