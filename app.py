import subprocess
import os
import streamlit as st
from antlr4 import *
# Importa tus clases generadas por ANTLR y tu módulo de música
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser
from Musica import tu_funcion_de_conversion # Reemplaza con el nombre real de tu función en Musica.py

st.title("Generador de Partituras Musicales 🎵")
st.write("Escribe tu notación musical para generar la partitura y escuchar el resultado.")

# Entrada de texto en la web
codigo_musical = st.text_area("Introduce tu secuencia de notas:", "C4 D4 E4")

if st.button("Generar Partitura"):
    try:
        # 1. Procesar el texto del usuario usando ANTLR
        input_stream = InputStream(codigo_musical)
        lexer = BazilioLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = BazilioParser(stream)
        tree = parser.prog() # O la regla inicial de tu gramática
        
        # 2. Aplicar tu lógica de conversión a LilyPond (usando absolute y stemDown como definimos antes)
        # Aquí llamas a tu función que traduce el árbol o el texto a formato LilyPond
        resultado_lilypond = tu_funcion_de_conversion(tree) 

        # Estructura final para LilyPond con las correcciones de formato
        contenido_ly = f"""
        \\version "2.24.0"
        \\absolute {{
            \\stemDown
            {resultado_lilypond}
        }}
        """
        
        with open("partitura.ly", "w") as f:
            f.write(contenido_ly)
            
        # 3. Compilar con LilyPond en el servidor de Streamlit
        subprocess.run(["lilypond", "-dno-point-and-click", "partitura.ly"], check=True)
        
        st.success("¡Partitura generada con éxito!")
        
        # 4. Ofrecer el archivo PDF para descargar en la web
        with open("partitura.pdf", "rb") as pdf_file:
            st.download_button(
                label="Descargar Partitura en PDF",
                data=pdf_file,
                file_name="partitura.pdf",
                mime="application/pdf"
            )
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar la música: {e}")