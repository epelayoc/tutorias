import streamlit as st
import pandas as pd

# Cargar el archivo Excel
DATA_FILE = "opciones.xlsx"
df = pd.read_excel(DATA_FILE)
def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# Cargar las opciones desde el archivo
df = load_data()

st.title("Formulario de Inscripción a Reuniones")
st.write("Selecciona una fecha para tu reunión. Las opciones tienen un límite de 5 inscripciones por fecha.")

# Obtener las preguntas y sus opciones
preguntas = df["pregunta"].unique()

# Crear un formulario interactivo
with st.form("Formulario de registro"):
    nombre = st.text_input("Tu nombre", "")
    pregunta_seleccionada = st.selectbox("Pregunta", preguntas)
    opciones_disponibles = df[df["pregunta"] == pregunta_seleccionada]

    opciones_habilitadas = opciones_disponibles[opciones_disponibles["respuestas"] < 5]
    if opciones_habilitadas.empty:
        st.error("No hay fechas disponibles para esta pregunta.")
    else:
        opcion = st.selectbox("Opciones disponibles", opciones_habilitadas["opción"])
        enviar = st.form_submit_button("Registrar")

        if enviar:
            # Actualizar el conteo de respuestas
            idx = (df["pregunta"] == pregunta_seleccionada) & (df["opcion"] == opcion)
            if opciones_habilitadas.loc[opciones_habilitadas["opcion"] == opcion, "respuestas"].values[0] < 5:
                df.loc[idx, "num_respuestas"] += 1
                save_data(df)
                st.success(f"¡Te has registrado en la opción '{opcion}' con éxito!")
            else:
                st.error("Esta opción ya ha alcanzado el límite de inscripciones.")

# Mostrar el estado actual de las inscripciones
st.subheader("Estado actual de las inscripciones")
st.dataframe(df)
