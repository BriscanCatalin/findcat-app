# Baza: Imagine oficială Python 3.10
FROM python:3.10-slim

# Setăm directorul de lucru în container
WORKDIR /app

# Copiem toate fișierele din proiect în container
COPY . /app

# Instalam dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Exponem portul 5000 (portul implicit al Flask)
EXPOSE 5000

# Rulăm aplicația Flask
CMD ["python", "findcat.py"]