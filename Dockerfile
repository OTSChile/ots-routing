# Utilizar una imagen base de Python
FROM python:3.8-slim

MAINTAINER Eduardo Molina

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos primero para aprovechar la caché de capas de Docker
COPY src/requirements.txt .

# Instalar las dependencias del proyecto
COPY src/requirements.txt /app/
RUN pip install -r requirements.txt

# Copiar el resto de los archivos del proyecto al contenedor
COPY src/ /app/

# Expone el puerto que Flask utilizará
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
