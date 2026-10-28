# Usamos una imagen oficial de Python
FROM python:3.10-slim

# Instalamos LilyPond y dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    lilypond \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos e instalamos los requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de tu proyecto al contenedor
COPY . .

# Comando para iniciar la aplicación web usando Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT app:app