# Imagen base de python
FROM python:3.10-slim

# directorios de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# copiar todo el código al contenedor
COPY . .

# Exponemos el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
