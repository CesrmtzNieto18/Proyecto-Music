import os
import sys
import time
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox, ttk

# --- TRADUCCIÓN DIRECTA DE NOTAS A LILYPOND ---

def nota_a_lilypond_absoluta(token):
    """
    Traduce directamente cada nota de la caja de texto al modo absoluto de LilyPond.
    C4 = c' (Do central con una línea adicional abajo, exacto al ejemplo de tu compañero).
    """
    token = token.strip().upper()
    if len(token) < 2:
        raise ValueError(f"Formato de nota inválido: '{token}'")
    
    letra = token[0].lower()
    try:
        octava = int(token[1:])
    except ValueError:
        raise ValueError(f"Octava inválida en la nota: '{token}'")
    
    if letra not in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
        raise ValueError(f"Nota musical desconocida: '{letra}'")
    
    # Mapeo absoluto exacto y predecible:
    # Octava 4 = c' (1 comilla = 1 línea adicional abajo)
    # Octava 3 = c  (sin comillas = más grave)
    # Octava 5 = c'' (2 comillas = dentro del pentagrama)
    if octava == 4:
        marcas = "'"
    elif octava == 3:
        marcas = ""
    elif octava > 4:
        marcas = "'" * (octava - 3)
    else:
        marcas = "," * (4 - octava)
        
    return f"{letra}{marcas}4"



def version_lilypond():
    try:
        salida = subprocess.run(["lilypond", "--version"], capture_output=True, text=True).stdout
        import re
        return re.search(r"(\d+\.\d+\.\d+)", salida).group(1)
    except (OSError, AttributeError):
        return "2.20.0"

def texto_lilypond_desde_tokens(tokens_notas, tempo=120):
    notas_ly = [nota_a_lilypond_absoluta(t) for t in tokens_notas]
    renglones = [" ".join(notas_ly[i:i + 8]) for i in range(0, len(notas_ly), 8)]
    cuerpo = "\n  ".join(" " + r for r in renglones)
    return (f'\\version "{version_lilypond()}"\n'
            f'\\score {{\n'
            f'  \\absolute {{\n'
            f'    \\tempo 4 = {tempo}\n'
            f'    \\stemDown\n'  # <-- Esto fuerza los palitos hacia abajo
            f'    \\f\n'
            f'    {cuerpo}\n'
            f'  }}\n'
            f'  \\layout {{}}\n'
            f'  \\midi {{}}\n'
            f'}}\n')



def generar_salida_directa(tokens_notas, base, solo_ly=False, aviso=print):
    ruta_ly = base + ".ly"
    contenido_ly = texto_lilypond_desde_tokens(tokens_notas)
    with open(ruta_ly, "w", encoding="utf-8") as f:
        f.write(contenido_ly)
        
    generados = [ruta_ly]
    if solo_ly:
        return generados

    def correr(cmd, descripcion):
        if shutil.which(cmd[0]) is None:
            aviso(f"Aviso: no se encontró «{cmd[0]}», no se generó {descripcion}.")
            return False
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            detalle = r.stderr.strip()[-400:]
            aviso(f"Aviso: falló {cmd[0]} al generar {descripcion}:\n{detalle}")
            return False
        return True

    pasos = [
        (["lilypond", "-o", base, ruta_ly], "el PDF y el MIDI", [".pdf", ".midi"]),
        # Volumen amplificado con -A200 para Timidity
        (["timidity", "-Ow", "-o", base + ".wav", "-A200", base + ".midi"], "el WAV", [".wav"]),
        (["ffmpeg", "-y", "-loglevel", "error", "-i", base + ".wav",
          "-codec:a", "libmp3lame", "-qscale:a", "2", base + ".mp3"], "el MP3", [".mp3"]),
    ]

    for cmd, descripcion, extensiones in pasos:
        if not correr(cmd, descripcion):
            break
        generados += [base + e for e in extensiones]
    return generados

# --- INTERFAZ GRÁFICA ---

ultimo_wav_generado = None

def reproducir_audio(ruta_archivo):
    """Reproduce el WAV usando el servidor de audio de Linux (PipeWire/PulseAudio)."""
    if not ruta_archivo or not os.path.exists(ruta_archivo):
        messagebox.showwarning("Aviso", "No hay ningún audio generado para reproducir.")
        return
    try:
        if sys.platform.startswith("linux"):
            if subprocess.run(["which", "paplay"], capture_output=True).returncode == 0:
                subprocess.Popen(["paplay", ruta_archivo])
            elif subprocess.run(["which", "aplay"], capture_output=True).returncode == 0:
                subprocess.Popen(["aplay", ruta_archivo], stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(["xdg-open", ruta_archivo])
        elif os.name == "nt":
            import winsound
            winsound.PlaySound(ruta_archivo, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        messagebox.showerror("Error de Reproducción", f"No se pudo reproducir el archivo: {e}")

def generar_archivos():
    global ultimo_wav_generado
    texto = entry_texto.get().strip()

    if not texto:
        messagebox.showwarning("Campo Vacío", "Por favor, escribe las notas musicales (ej. C4 D4 E4).")
        return

    # Separa las notas por espacios, comas o guiones
    tokens = [t for t in texto.replace(",", " ").replace("-", " ").split() if t]

    if not tokens:
        lbl_estado.config(text="No se ingresaron notas.", fg="#f38ba8")
        return

    try:
        # Validar y mostrar los tokens tal cual los ingresó el usuario
        detalles = [f"{t.upper()}" for t in tokens]
    except Exception as e:
        messagebox.showerror("Error de Formato", f"Revisa tus notas:\n{e}")
        lbl_estado.config(text="Error en las notas.", fg="#f38ba8")
        return

    lbl_notas.config(text="Notas leídas: " + " | ".join(detalles))
    lbl_estado.config(text="Generando partitura y audio...", fg="#f9e2af")
    ventana.update()

    timestamp = time.strftime("%H%M%S")
    nombre_base = f"partitura_notas_{timestamp}"

    try:
        archivos_generados = generar_salida_directa(tokens, nombre_base, solo_ly=False)
        ultimo_wav_generado = next((a for a in archivos_generados if a.endswith(".wav")), None)
        lista_archivos = "\n".join([f"• {os.path.basename(a)}" for a in archivos_generados])

        lbl_estado.config(text="¡Partitura y audios generados con éxito!", fg="#a6e3a1")
        
        if ultimo_wav_generado:
            btn_reproducir.config(state=tk.NORMAL)
            reproducir_audio(ultimo_wav_generado)

        messagebox.showinfo("Generación Completa", f"Archivos guardados:\n\n{lista_archivos}")
    except Exception as e:
        lbl_estado.config(text="Error al compilar.", fg="#f38ba8")
        messagebox.showerror("Error", str(e))

# --- VENTANA TKINTER ---
ventana = tk.Tk()
ventana.title("Generador Musical Directo")
ventana.geometry("540x440")
ventana.config(bg="#1e1e2e")

lbl_titulo = tk.Label(ventana, text="🎼 Editor de Notas Musicales Directas", font=("Segoe UI", 14, "bold"), bg="#1e1e2e", fg="#cba6f7")
lbl_titulo.pack(pady=(20, 5))

lbl_sub = tk.Label(ventana, text="Escribe las notas tal cual (Ej: C4 D4 E4 C4 B3):", font=("Segoe UI", 10), bg="#1e1e2e", fg="#cdd6f4")
lbl_sub.pack(pady=5)

entry_texto = tk.Entry(ventana, font=("Segoe UI", 14), width=32, bg="#313244", fg="#cdd6f4", justify="center")
entry_texto.pack(pady=10)
entry_texto.focus()

frame_botones = tk.Frame(ventana, bg="#1e1e2e")
frame_botones.pack(pady=10)

btn_generar = tk.Button(frame_botones, text="Generar y Reproducir", font=("Segoe UI", 11, "bold"), bg="#cba6f7", fg="#11111b", command=generar_archivos)
btn_generar.pack(side=tk.LEFT, padx=5)

btn_reproducir = tk.Button(frame_botones, text="▶ Reproducir", font=("Segoe UI", 11, "bold"), bg="#a6e3a1", fg="#11111b", state=tk.DISABLED, command=lambda: reproducir_audio(ultimo_wav_generado))
btn_reproducir.pack(side=tk.LEFT, padx=5)

lbl_notas = tk.Label(ventana, text="", font=("Consolas", 10), bg="#181825", fg="#89b4fa", wraplength=480, justify="center")
lbl_notas.pack(pady=10, fill=tk.X, padx=20)

lbl_estado = tk.Label(ventana, text="", font=("Segoe UI", 9, "bold"), bg="#1e1e2e", fg="#a6e3a1")
lbl_estado.pack(pady=5)

ventana.bind("<Return>", lambda event: generar_archivos())

if __name__ == "__main__":
    ventana.mainloop()