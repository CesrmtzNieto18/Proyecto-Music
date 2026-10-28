import subprocess
import os
from flask import Flask, render_template_string, request, send_file
from antlr4 import *
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser

app = Flask(__name__)

# HTML sencillo con una caja de texto y botón
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Generador de Partituras</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f9; color: #333; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 150px; padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ccc; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0056b3; }
        a { display: inline-block; margin-top: 15px; text-decoration: none; background: #28a745; color: white; padding: 10px 20px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Generador de Partituras Musicales 🎵</h2>
        <form method="POST">
            <textarea name="codigo_musical" placeholder="Escribe tus notas aquí...">{{ codigo | default('c4 d4 e4') }}</textarea><br>
            <button type="submit">Generar Partitura</button>
        </form>
        {% if generado %}
            <h3 style="color: green;">¡Partitura generada con éxito!</h3>
            <a href="/download">Descargar PDF</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    generado = False
    codigo = ""
    if request.method == "POST":
        codigo = request.form.get("codigo_musical")
        try:
            # Procesamiento con ANTLR
            input_stream = InputStream(codigo)
            lexer = BazilioLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = BazilioParser(stream)
            tree = parser.prog()
            
            # Aquí puedes integrar tu lógica de conversión al resultado de LilyPond
            # Por ahora usamos el texto o la estructura base:
            contenido_ly = f"""
            \\version "2.24.0"
            \\absolute {{
                \\stemDown
                {codigo}
            }}
            """
            
            with open("partitura.ly", "w") as f:
                f.write(contenido_ly)
                
            # Compilar con LilyPond en el servidor de Render
            subprocess.run(["lilypond", "-dno-point-and-click", "partitura.ly"], check=True)
            generado = True
        except Exception as e:
            print(f"Error: {e}")
            
    return render_template_string(HTML_TEMPLATE, generado=generado, codigo=codigo)

@app.route("/download")
def download():
    return send_file("partitura.pdf", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)