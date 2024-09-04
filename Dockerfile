# Utiliser une image Python officielle comme base
FROM python:3.9-slim-buster

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 8000

# Définir les variables d'environnement
ENV DJANGO_SETTINGS_MODULE=les2peresnoel.settings
ENV PORT=8000

# Exécuter les migrations et démarrer l'application
CMD python manage.py migrate && gunicorn les2peresnoel.wsgi:application --bind 0.0.0.0:$PORT
