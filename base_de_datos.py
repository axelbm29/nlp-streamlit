import sqlite3


# Clase para representar los datos NLP
class NLP:
    def __init__(self, mensajeNLP, mensajeASCII, mensajeBinario, tiempoEjecucion):
        self.mensajeNLP = mensajeNLP
        self.mensajeASCII = mensajeASCII
        self.mensajeBinario = mensajeBinario
        self.tiempoEjecucion = tiempoEjecucion


# Función para crear la tabla en la base de datos
def crear_tabla():
    conn = sqlite3.connect("database/nlp_db.db")  # Conecta o crea la base de datos
    cursor = conn.cursor()

    # Crea la tabla si no existe
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nlp_data (
            id INTEGER PRIMARY KEY,
            mensajeNLP TEXT,
            mensajeASCII TEXT,
            mensajeBinario TEXT,
            tiempoEjecucion REAL
        )
    """
    )

    conn.commit()
    conn.close()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear la tabla si no existe
    crear_tabla()
