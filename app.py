import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar el archivo Excel
DATA_FILE = "opciones.xlsx"
LIMIT = 1

def load_data():
    try:
      return pd.read_excel(DATA_FILE)
    except FileNotFoundError:
      return pd.DataFrame({"pregunta":[], "opcion":[], "respuestas":[]})

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# Cargar las opciones desde el archivo
df = load_data()

# Check if the DataFrame has the necessary columns
if not all(col in df.columns for col in ["pregunta", "opcion", "respuestas"]):
    st.error("The Excel file must contain the columns 'pregunta', 'opcion', and 'respuestas'.")
    st.stop()

st.title("Formulario de Inscripción a Reuniones")
st.write("Selecciona una fecha para tu reunión. Las opciones tienen un límite de 5 inscripciones por fecha.")

# Obtener las preguntas y sus opciones
preguntas = df["pregunta"].unique()

# Crear un formulario interactivo
with st.form("Formulario de registro"):
    nombre = st.text_input("Tu nombre", "")
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

                    # Load existing registration data or create empty DataFrame if it does not exist
                    try:
                        registration_df = pd.read_excel('registrations.xlsx')
                    except FileNotFoundError:
                        registration_df = pd.DataFrame(columns = ["pregunta", "opcion", "nombre", "fecha_inscripción"])

                    # Create the new entry DataFrame
                    new_entry = {
                        "pregunta": pregunta_seleccionada,
                        "opcion": opcion,
                        "nombre": nombre,
                        "fecha_inscripción": fecha_inscripcion,
                    }

                    new_data = pd.DataFrame([new_entry])

                    # Concatenate the old registration data with the new data
                    registration_df = pd.concat([registration_df,new_data], ignore_index=True)

                    # Save the data to a new excel file
                    registration_df.to_excel("registrations.xlsx", index = False)

                    # Save the updated data to the original excel file
                    save_data(df)
                    st.success(f"¡Te has registrado en la opción '{opcion}' con éxito!")

                else:
                    st.error("Esta opción ya ha alcanzado el límite de inscripciones.")


# Mostrar el estado actual de las inscripciones
st.subheader("Estado actual de las inscripciones")
st.dataframe(df)
