import streamlit as st
import pandas as pd
import random
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


ARCHIVO_USADOS = "numeros_usados.txt"

st.set_page_config(page_title="PROSOLVIT TECH", layout="centered")


# Hoja de calculo
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


#CSS 
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

/* FONDO */
.stApp { 
    background: linear-gradient(225deg, #0AC4E0, #BDE8F5);
}

/* LOGO */
img { margin-top: -10px; }
.block-container { background: transparent; }
[data-testid="stImage"] { background-color: transparent; }

/* SUBTÍTULOS */
.subtitulo {
    font-family: 'Cinzel', serif !important;
    font-size: 45px;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 25px;
    background: linear-gradient(#0B2D72, #0D1A63, #0992C2 );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TEXTO DEL FORM */
.texto-form {
    font-family: 'Cinzel', serif !important;
    color: #F3F4F4;
    font-size: 18px;
    font-weight: 600;
    margin-top: 15px;
}

/* INPUTS */
input, textarea {
    background-color: #E9F1FF !important;
    color: #0A1A2F !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px !important;
    font-size: 16px !important;
}

/* INPUT FOCUS */
input:focus, textarea:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(11,45,114,0.35);
}

/* BOTONES */
button {
    font-family: 'Orbitron', sans-serif !important;
    background: linear-gradient(90deg, #0F5FFF, #0F5FFF) !important;
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
    box-shadow: 0 6px 18px rgba(0,194,255,0.35);
}

/* NUMERO ANIMADO */
.numero-ganador {
    text-align: center;
    font-size: 120px;
    font-family: 'Cinzel', serif !important;
    margin-top: 20px;
    background: linear-gradient(225deg, #1C0770, #261CC1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: aparecerNumero 0.9s ease-out,
               brilloNumero 2s ease-in-out infinite;
}

@keyframes aparecerNumero {
    0% { transform: scale(0.4); opacity: 0; }
    60% { transform: scale(1.15); }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes brilloNumero {
    0% { text-shadow: 0 0 0px rgba(0,194,255,0); }
    50% { text-shadow: 0 0 15px rgba(0,194,255,0.6); }
    100% { text-shadow: 0 0 0px rgba(0,194,255,0); }
}

</style>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.image("prosolvit.png", use_container_width=True)

st.markdown("<div class='subtitulo'>🎉 Sorteo</div>", unsafe_allow_html=True)


#  LEER HOJA DE CALCULO

data = sheet.get_all_records()

if not data:
    st.warning("No hay participantes registrados aún.")
    st.stop()

df = pd.DataFrame(data)


# NUMEROS USADOS 
if os.path.exists(ARCHIVO_USADOS):
    with open(ARCHIVO_USADOS, "r") as f:
        usados = [int(x.strip()) for x in f.readlines()]
else:
    usados = []

numeros_totales = df["numero"].tolist()
disponibles = list(set(numeros_totales) - set(usados))


# BOTON
c1, c2, c3 = st.columns([1,1,1])
with c2:
    sacar = st.button("Sacar Número")

if sacar:
    if disponibles:
        numero = random.choice(disponibles)

        with open(ARCHIVO_USADOS, "a") as f:
            f.write(f"{numero}\n")

        # Mostrar número animado
        st.markdown(
            f"<div class='numero-ganador'>{numero}</div>",
            unsafe_allow_html=True
        )

        # Buscar ganador
        ganador = df[df["numero"] == numero].iloc[0]

        # Mostrar nombre en negro debajo
        st.markdown(
            f"<div class='subtitulo' style='color:black; -webkit-text-fill-color:black; font-size:30px;'>{ganador['nombre']}</div>",
            unsafe_allow_html=True
        )

    else:
        st.warning("No hay números disponibles.")


# BOTON 2
c1, c2, c3 = st.columns([1,1,1])
with c2:
    reiniciar = st.button("Reiniciar Sorteo")

if reiniciar:
    if os.path.exists(ARCHIVO_USADOS):
        os.remove(ARCHIVO_USADOS)





