import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar el archivo Excel
DATA_FILE = "opciones.xlsx"
OUT_FILE = "opciones1.xlsx"

LIMIT = 1
nombre_lista = ['Luis', 'Pedro', 'Juan', 'Ana', 'Maria', 'Carlos']

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
    #nombre = st.text_input("Tu nombre", "")
    nombre = st.selectbox("Tu nombre", nombre_lista)

    pregunta_seleccionada = st.selectbox("Pregunta", preguntas)
    opciones_disponibles = df[df["pregunta"] == pregunta_seleccionada]

    opciones_habilitadas = opciones_disponibles[opciones_disponibles["respuestas"] < LIMIT]
    if opciones_habilitadas.empty:
        st.error("No hay fechas disponibles para esta pregunta.")
    else:
        opcion = st.selectbox("Opciones disponibles", opciones_habilitadas["opcion"])
        enviar = st.form_submit_button("Registrar")

        if enviar:
            if not nombre:
                st.error("Por favor, introduce tu nombre.")
            else:
                # Actualizar el conteo de respuestas
                idx = (df["pregunta"] == pregunta_seleccionada) & (df["opcion"] == opcion)
                if opciones_habilitadas.loc[opciones_habilitadas["opcion"] == opcion, "respuestas"].values[0] < LIMIT:
                    df.loc[idx, "respuestas"] += 1
    
                    # Registrar nombre y fecha de inscripción
                    fecha_inscripcion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_entry = {
                        "pregunta": pregunta_seleccionada,
                        "opcion": opcion,
                        "nombre": nombre,
                        "fecha_inscripción": fecha_inscripcion,
                    }
    
                    # Crear un nuevo DataFrame para almacenar esta inscripción
                    new_data = pd.DataFrame([new_entry])
    
                    # Guardar los cambios: actualizar conteo y agregar registro
                    save_data(pd.concat([df, new_data], ignore_index=True))
                    st.success(f"¡Te has registrado en la opción '{opcion}' con éxito!")
                else:
                    st.error("Esta opción ya ha alcanzado el límite de inscripciones.")

# Mostrar el estado actual de las inscripciones
st.subheader("Estado actual de las inscripciones")
#df_actual = df[["pregunta","opcion","respuestas"]]
df_actual = df[["pregunta","opcion","respuestas"]].dropna(subset=['respuestas'])

st.dataframe(df_actual)
