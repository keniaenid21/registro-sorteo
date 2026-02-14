import streamlit as st
import pandas as pd
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.set_page_config(page_title="PROSOLVIT TECH", layout="centered")


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

cred = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)

client = gspread.authorize(cred)
sheet = client.open("registro_sorteo").sheet1


#  CSS 
st.markdown("""
<style>

/* Tipos de letra */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Inter:wght@400;600&family=Cinzel:wght@600&display=swap');

/* OCULTAR ENCABEZADO */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* QUITAR ESPACIO SUPERIOR */
.block-container { padding-top: 3rem !important; }

/* PARA EL DEGRADADO DEL FONDO */
.stApp { 
    background: linear-gradient(225deg, #0AC4E0, #BDE8F5);
}

/* LOGO MARGEN*/
img { margin-top: -10px; }

.block-container { background: transparent; }

[data-testid="stImage"] { background-color: transparent; }

/* SUBTITULOS */
.subtitulo {
    font-family: 'Cinzel', serif !important;
    font-size: 45px;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 15px;
    background: linear-gradient(#0B2D72, #0D1A63, #0992C2 );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TEXTO DEL REGISTRO */
.texto-form {
    font-family: 'Cinzel', serif !important;
    color: #F3F4F4;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: -60px;
}

/* INPUTS */
input, textarea {
    background-color: #E9F1FF !important;
    color: #0A1A2F !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px !important;
    font-size: 16px !important;
    margin-bottom: 6px;
}

/* cursor visible */
.stTextInput input:focus {
    border: 1px solid #000000 !important;
    caret-color: #000000 !important;
    box-shadow: none !important;
}

/* QUITA EL FONDO NEGRO CUANDO SE SELECCIONA ALGO POR PREDETERMIDANO */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill {
    -webkit-box-shadow: 0 0 0px 1000px #E9F1FF inset !important;
    -webkit-text-fill-color: #0A1A2F !important;
    caret-color: #0A1A2F !important;
}

/* INPUT */
input:focus, textarea:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(11,45,114,0.35);
}

/* BOTONES */
button {
    font-family: 'Orbitron', sans-serif !important;
    background: linear-gradient(90deg, #0F5FFF, #00C2FF) !important;
    color: white !important;
    border-radius: 12px !important;
    height: 50px !important;
    width: 260px !important;
    border: none !important;
    font-size: 20px;
    letter-spacing: 1px;
    transition: transform .15s ease, box-shadow .15s ease;
}

/* ANIMACIÓN DE LOS BOTONES */
button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(0,194,255,0.35),
                inset 0 0 3px rgba(255,255,255,0.2);
}

/* CONTENEDOR DEL REGISTRO */
div[data-testid="stForm"] {
    background-color: #0D1A63;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.image("prosolvit.png", use_container_width=True)


st.markdown("<div class='subtitulo'>Registro de Participantes</div>", unsafe_allow_html=True)



#REGISTRO DE PARTICIPANTES
with st.form("registro"):

    st.markdown("<div class='texto-form'>Nombre completo *</div>", unsafe_allow_html=True)
    nombre = st.text_input("", placeholder="Ingresa nombre completo")

    st.markdown("<div class='texto-form'>Correo electrónico *</div>", unsafe_allow_html=True)
    correo = st.text_input("", placeholder="Ingresa correo")

    st.markdown("<div class='texto-form'>Empresa *</div>", unsafe_allow_html=True)
    empresa = st.text_input("", placeholder="Empresa")

    st.markdown("<div class='texto-form'>Descripción</div>", unsafe_allow_html=True)
    descripcion = st.text_input("", placeholder="Opcional")

    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        submit = st.form_submit_button("Registrar")

    if submit:

        if not nombre or not correo or not empresa:
            st.warning("Completa todos los campos obligatorios.")

        elif not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$", nombre):
            st.warning("El nombre solo debe contener letras y espacios.")

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.warning("Ingresa un correo electrónico válido.")

        else:
            numero = len(sheet.col_values(1))

            sheet.append_row([
                numero,
                nombre,
                correo,
                empresa,
                descripcion
            ])

            st.success(f"Número asignado: {numero}")


