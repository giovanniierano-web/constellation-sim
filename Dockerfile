# Usiamo un'immagine ufficiale di Python leggera
FROM python:3.11-slim

# Impostiamo la directory di lavoro nel container
WORKDIR /app

# Aggiorniamo il sistema e installiamo git (utile se vuoi fare commit direttamente dal container)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiamo i requirements e installiamo le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il resto del codice sorgente nel container
COPY . .

# Comando di default all'avvio del container
CMD ["python", "simulator.py"]