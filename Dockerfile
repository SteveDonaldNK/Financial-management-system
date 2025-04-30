FROM python:3.13-slim
 
WORKDIR /app
 
# Installer les dépendances système pour mysqlclient
RUN apt update \
 && apt install -y pkg-config default-libmysqlclient-dev build-essential \
 && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# Précollecte des statics
RUN python manage.py collectstatic --noinput
 
# Port exposé par Gunicorn
EXPOSE 8000
 
CMD ["gunicorn", "gestion_financiere.wsgi:application", "--bind", "0.0.0.0:8000"]
