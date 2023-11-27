# Utiliser une image de base Python
FROM python:3.8-slim

# Répertoire de travail
WORKDIR /app

# Installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application dans le conteneur
COPY app.py /app/
COPY templates/index.html /app/templates/

# Exposer le port 5001
EXPOSE 5001

# Commande pour exécuter l'application
CMD ["python", "app.py"]
