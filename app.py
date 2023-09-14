import streamlit as st
import sqlite3
import pandas as pd
import time


st.set_page_config(page_title="Tarea 1", page_icon=":computer:", layout="wide")

st.title("Microprocesadores Tarea 1")

descripcion = """### Pseudocodigo
- Recibir mensaje NLP
- Generar codificación de conversión
- Convertir NLP al sistema de codificación
- Combinar los números en una cadena de texto
- Convertir sistema decimal a binario
- Imprimir dígitos binarios
"""
st.write("***Descripción de la tarea 1***")
st.markdown(descripcion)


# funcion para convertir NLP a ASCII
def convertirNLPaASCII(mensajeNLP):
    mensajeASCII = []
    for letra in mensajeNLP:
        mensajeASCII.append(ord(letra))
    return mensajeASCII


# funcion para convertir ASCII a binario
def convertirASCIIaBinario(mensajeASCII):
    mensajeBinario = []
    convertir_string_int = int("".join(map(str, mensajeASCII)))
    # print(convertir_string_int)
    # print(bin(convertir_string_int))
    for numero in mensajeASCII:
        mensajeBinario.append(bin(numero))
    return mensajeBinario


# ciclos de reloj
def tiempoEjecucion(palabra):
    return len(palabra) * 2 * 4


class NLP:
    def __init__(self, mensajeNLP, mensajeASCII, mensajeBinario, tiempoEjecucion):
        self.mensajeNLP = mensajeNLP
        self.mensajeASCII = mensajeASCII
        self.mensajeBinario = mensajeBinario
        self.tiempoEjecucion = tiempoEjecucion


def insertar_registro(nlp_obj):
    conn = sqlite3.connect("database/nlp_db.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO nlp_data (mensajeNLP, mensajeASCII, mensajeBinario, tiempoEjecucion)
        VALUES (?, ?, ?, ?)
    """,
        (
            nlp_obj.mensajeNLP,
            nlp_obj.mensajeASCII,
            nlp_obj.mensajeBinario,
            nlp_obj.tiempoEjecucion,
        ),
    )

    conn.commit()
    conn.close()


def listar_registro():
    conn = sqlite3.connect("database/nlp_db.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM nlp_data
    """
    )

    registros = cursor.fetchall()

    conn.commit()
    conn.close()

    # Crear un DataFrame con los nombres de las columnas
    df = pd.DataFrame(
        registros,
        columns=[
            "id",
            "Mensaje NLP",
            "Mensaje ASCII",
            "Mensaje binario",
            "Ciclos de reloj",
        ],
    )
    df = df.drop(columns=["id"])
    return df


mensajeNLP = st.text_input("Ingrese mensaje NLP")
if mensajeNLP:
    # generar los datos
    ascii = convertirNLPaASCII(mensajeNLP)
    binario = convertirASCIIaBinario(ascii)
    # convertir a string
    mensajeASCII = "".join(map(str, ascii))
    mensajeBinario = "".join(map(str, binario))
    # calcular ciclos de reloj
    tiempo = tiempoEjecucion(mensajeNLP)
    st.write("Mensaje en ASCII: ", mensajeASCII)
    st.write("Mensaje en binario : ", mensajeBinario)
    st.write("Tiempo de ejecución: ", tiempo)
    dato = NLP(mensajeNLP, mensajeASCII, mensajeBinario, tiempo)
    insertar_registro(dato)
    st.write("***Historial de conversiones***")
    registros = listar_registro()
    st.dataframe(registros, use_container_width=True)


st.title("Conversación entre Jairo y Axel")

# lista para almacenar la conversacion
conversacion = []

# muestra la conversacion del archivo csv
try:
    df = pd.read_csv("conversacion.csv")
    conversacion = df["Conversacion"].tolist()
except FileNotFoundError:
    pass

# se inicia la pagina teniendo a Jairo como la persona principal cuando
# inicia la conversacion
if 'persona_actual' not in st.session_state:
    st.session_state.persona_actual = "Jairo"


# textfield texto_actual
texto_actual = st.text_input(f"{st.session_state.persona_actual}:", key="text_input")

# Botón para que se envie el mensaje y se convierta a ascii
if st.button("Enviar"):
    if texto_actual:
        # almacena el codigo ascii
        mensaje_ascii = []
        for char in texto_actual:
            # conversion el valor ascii a cadena de texto
            mensaje_ascii.append(str(ord(char)))
        # une los numeros
        mensaje = f"{st.session_state.persona_actual} dice: {''.join(mensaje_ascii)}"
        # agrega el mensaje a la conversacion
        conversacion.append(mensaje)
        #escribe el mensaje en la conversacion
        st.write(mensaje)
        # cambio de persona: De Jairo a Axel y de Axel a Jairo
        if st.session_state.persona_actual == "Jairo":
            st.session_state.persona_actual = "Axel"
        else:
            st.session_state.persona_actual = "Jairo"
        # actualiza la conversacion con el mensaje reciente
        df = pd.DataFrame({"Conversacion": conversacion})
        df.to_csv("conversacion.csv", index=False)
        
# se muestra toda la conversacion
st.markdown("**Conversación:**")
for mensaje in conversacion:
    st.text(mensaje)