import subprocess
import os
from flask import Flask, render_template_string, request, send_file
from antlr4 import *
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser

app = Flask(__name__)

# Plantilla HTML con el diseño oscuro exacto de tu app de escritorio
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Editor de Notas Musicales Directas</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background-color: #2b2b2b; 
            color: #ffffff; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
        }
        .container { 
            background: #3c3f41; 
            padding: 35px; 
            border-radius: 8px; 
            box-shadow: 0px 4px 15px rgba(0,0,0,0.6); 
            width: 480px; 
            text-align: center; 
        }
        h2 { 
            color: #ffffff; 
            font-size: 18px; 
            margin-bottom: 20px; 
        }
        label { 
            display: block; 
            text-align: left; 
            font-size: 13px; 
            margin-bottom: 8px; 
            color: #cccccc; 
            font-weight: bold;
        }
        textarea { 
            width: 100%; 
            height: 90px; 
            padding: 10px; 
            font-size: 14px; 
            border-radius: 4px; 
            border: 1px solid #555; 
            background: #2b2b2b; 
            color: #fff; 
            box-sizing: border-box; 
            resize: none; 
        }
        button { 
            background: #f0f0f0; 
            color: #333333; 
            border: none; 
            padding: 10px 20px; 
            font-size: 14px; 
            font-weight: bold; 
            border-radius: 4px; 
            cursor: pointer; 
            margin-top: 15px; 
            width: 100%; 
        }
        button:hover { 
            background: #e0e0e0; 
        }
        .success { 
            color: #a3be8c; 
            margin-top: 15px; 
            font-weight: bold; 
            font-size: 14px;
        }
        a { 
            display: inline-block; 
            margin-top: 12px; 
            text-decoration: none; 
            background: #28a745; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 4px; 
            font-size: 14px; 
            font-weight: bold;
        }
        a:hover { 
            background: #218838; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎵 Editor de Notas Musicales Directas</h2>
        <form method="POST">
            <label>Escribe las notas tal cual (Ej: C4 D4 E4 C4 B3):</label>
            <textarea name="codigo_musical" placeholder="C4 D4 E4...">{{ codigo | default('') }}</textarea>
            <button type="submit">Generar y Reproducir</button>
        </form>
        {% if generado %}
            <div class="success">¡Partitura generada con éxito!</div>
            <a href="/download">Descargar Partitura en PDF</a>
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
            
            # Estructura para LilyPond
            contenido_ly = f"""
            \\version "2.24.0"
            \\absolute {{
                \\stemDown
                {codigo}
            }}
            """
            
            with open("partitura.ly", "w") as f:
                f.write(contenido_ly)
                
            # Compilar con LilyPond en Render
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