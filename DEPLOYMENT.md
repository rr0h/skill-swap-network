# 🚀 Deployment Guide - Skill Swap Network

Complete guide for deploying Skill Swap Network to production.

## 📋 Pre-Deployment Checklist

- [ ] All features tested locally
- [ ] Database migrations completed
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Security settings reviewed
- [ ] Backup strategy in place
- [ ] Domain name registered
- [ ] SSL certificate ready

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for Beginners)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Install Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL Database**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Configure Environment Variables**
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
```

6. **Update requirements.txt**
```bash
# Add these to requirements.txt
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

7. **Create Procfile**
```
web: gunicorn skillswap.wsgi --log-file -
```

8. **Update settings.py for Production**
```python
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Middleware (add WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]
```

9. **Deploy**
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

10. **Run Migrations**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

11. **Open App**
```bash
heroku open
```

---

### Option 2: DigitalOcean / AWS / VPS

#### Prerequisites
- VPS server (Ubuntu 20.04+ recommended)
- Domain name
- SSH access

#### Steps

1. **Connect to Server**
```bash
ssh root@your-server-ip
```

2. **Update System**
```bash
apt update && apt upgrade -y
```

3. **Install Dependencies**
```bash
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

4. **Create Database**
```bash
sudo -u postgres psql

CREATE DATABASE skillswap_db;
CREATE USER skillswap_user WITH PASSWORD 'your-password';
ALTER ROLE skillswap_user SET client_encoding TO 'utf8';
ALTER ROLE skillswap_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE skillswap_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skillswap_db TO skillswap_user;
\q
```

5. **Clone Repository**
```bash
cd /var/www
git clone https://github.com/rr0h/skill-swap-network.git
cd skill-swap-network
```

6. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

7. **Configure Environment**
```bash
nano .env
```

Add:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://skillswap_user:your-password@localhost/skillswap_db
```

8. **Update settings.py**
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
```

9. **Run Migrations**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

10. **Create Gunicorn Service**
```bash
nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon for Skill Swap Network
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/skill-swap-network
ExecStart=/var/www/skill-swap-network/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/skill-swap-network/skillswap.sock \
          skillswap.wsgi:application

[Install]
WantedBy=multi-user.target
```

11. **Start Gunicorn**
```bash
systemctl start gunicorn
systemctl enable gunicorn
```

12. **Configure Nginx**
```bash
nano /etc/nginx/sites-available/skillswap
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/skill-swap-network;
    }
    
    location /media/ {
        root /var/www/skill-swap-network;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/skill-swap-network/skillswap.sock;
    }
}
```

13. **Enable Site**
```bash
ln -s /etc/nginx/sites-available/skillswap /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
```

14. **Setup SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### Option 3: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "skillswap.wsgi:application"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=skillswap_db
      - POSTGRES_USER=skillswap_user
      - POSTGRES_PASSWORD=your-password

  web:
    build: .
    command: gunicorn skillswap.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### Deploy with Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔒 Production Security Settings

### Update settings.py

```python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## 📧 Email Configuration

### Gmail SMTP

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Skill Swap Network <noreply@yourdomain.com>'
```

### SendGrid

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

---

## 💾 Backup Strategy

### Database Backup

```bash
# PostgreSQL
pg_dump skillswap_db > backup_$(date +%Y%m%d).sql

# Automated daily backup
crontab -e
0 2 * * * pg_dump skillswap_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Media Files Backup

```bash
# Sync to S3
aws s3 sync /var/www/skill-swap-network/media s3://your-bucket/media
```

---

## 📊 Monitoring

### Setup Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/skillswap/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitor with Sentry

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/skill-swap-network
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            systemctl restart gunicorn
```

---

## ✅ Post-Deployment Checklist

- [ ] SSL certificate installed and working
- [ ] Database backups configured
- [ ] Email sending working
- [ ] Static files serving correctly
- [ ] Media uploads working
- [ ] Admin panel accessible
- [ ] User registration working
- [ ] Password reset working
- [ ] All features tested
- [ ] Error logging configured
- [ ] Monitoring setup
- [ ] Performance optimized
- [ ] Security headers configured

---

## 🆘 Troubleshooting

### 502 Bad Gateway
- Check Gunicorn is running: `systemctl status gunicorn`
- Check Nginx configuration: `nginx -t`
- Check logs: `journalctl -u gunicorn`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check Nginx static file configuration
- Verify file permissions

### Database Connection Errors
- Check PostgreSQL is running
- Verify database credentials
- Check firewall rules

---

**Deployment Complete!** 🎉

Your Skill Swap Network is now live and ready for users!
