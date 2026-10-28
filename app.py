import subprocess
import os
import re
from flask import Flask, render_template_string, request, send_file
from antlr4 import *
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser

app = Flask(__name__)

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
        h2 { color: #ffffff; font-size: 18px; margin-bottom: 20px; }
        label { display: block; text-align: left; font-size: 13px; margin-bottom: 8px; color: #cccccc; font-weight: bold; }
        textarea { 
            width: 100%; height: 90px; padding: 10px; font-size: 14px; 
            border-radius: 4px; border: 1px solid #555; background: #2b2b2b; color: #fff; 
            box-sizing: border-box; resize: none; 
        }
        button { 
            background: #f0f0f0; color: #333333; border: none; padding: 10px 20px; 
            font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer; margin-top: 15px; width: 100%; 
        }
        button:hover { background: #e0e0e0; }
        .success { color: #a3be8c; margin-top: 15px; font-weight: bold; font-size: 14px; }
        .error { color: #bf616a; margin-top: 15px; font-weight: bold; font-size: 13px; text-align: left; background: #2b2b2b; padding: 10px; border-radius: 4px; word-break: break-all; }
        audio { margin-top: 15px; width: 100%; }
        .btn-pdf { 
            display: inline-block; margin-top: 12px; text-decoration: none; 
            background: #007bff; color: white; padding: 10px 16px; 
            border-radius: 4px; font-size: 14px; font-weight: bold; width: 100%; box-sizing: border-box; 
        }
        .btn-pdf:hover { background: #0056b3; }
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
        
        {% if error_msg %}
            <div class="error"><b>Error detectado:</b> {{ error_msg }}</div>
        {% endif %}

        {% if generado %}
            <div class="success">¡Partitura y audio generados con éxito!</div>
            <audio controls autoplay>
                <source src="/audio" type="audio/wav">
                Tu navegador no soporta el reproductor de audio.
            </audio>
            <a href="/download-pdf" class="btn-pdf">Descargar Partitura en PDF</a>
        {% endif %}
    </div>
</body>
</html>
"""

def traducir_a_lilypond(texto_usuario):
    """Convierte notas tipo C4, D4, B3 a formato válido de LilyPond"""
    tokens = texto_usuario.strip().split()
    notas_lily = []
    for token in tokens:
        match = re.match(r'([A-Ga-g])(\d+)', token)
        if match:
            letra = match.group(1).lower()
            octava = int(match.group(2))
            
            # Mapeo de octavas para LilyPond absolute
            if octava == 4:
                apostrofes = "'"
            elif octava == 5:
                apostrofes = "''"
            elif octava == 3:
                apostrofes = ""
            elif octava < 3:
                apostrofes = "," * (3 - octava)
            else:
                apostrofes = "'" * (octava - 3)
                
            notas_lily.append(f"{letra}{apostrofes}4")
        else:
            notas_lily.append(token)
    return " ".join(notas_lily)

@app.route("/", methods=["GET", "POST"])
def index():
    generado = False
    error_msg = None
    codigo = ""
    if request.method == "POST":
        codigo = request.form.get("codigo_musical")
        try:
            # 1. Procesamiento con ANTLR
            input_stream = InputStream(codigo)
            lexer = BazilioLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = BazilioParser(stream)
            tree = parser.programa()
            
            # 2. Traducir notas al formato que entiende LilyPond
            notas_traducidas = traducir_a_lilypond(codigo)
            
            # 3. Estructura para LilyPond con diseño y MIDI
            contenido_ly = f"""
            \\version "2.24.0"
            \\score {{
                \\absolute {{
                    \\stemDown
                    {notas_traducidas}
                }}
                \\layout {{}}
                \\midi {{}}
            }}
            """
            
            with open("partitura.ly", "w") as f:
                f.write(contenido_ly)
                
            # 4. Compilar partitura y audio
            subprocess.run(["lilypond", "-dno-point-and-click", "partitura.ly"], check=True)
            subprocess.run(["timidity", "partitura.midi", "-Ow", "-o", "partitura.wav"], check=True)
            
            generado = True
        except Exception as e:
            error_msg = str(e)
            print(f"Error detallado: {e}")
            
    return render_template_string(HTML_TEMPLATE, generado=generado, error_msg=error_msg, codigo=codigo)

@app.route("/audio")
def audio():
    if os.path.exists("partitura.wav"):
        return send_file("partitura.wav", mimetype="audio/wav")
    return "Audio no encontrado", 404

@app.route("/download-pdf")
def download_pdf():
    if os.path.exists("partitura.pdf"):
        return send_file("partitura.pdf", as_attachment=True, mimetype="application/pdf")
    return "PDF no encontrado", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)