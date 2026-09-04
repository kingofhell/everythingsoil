#!/usr/bin/env bash
set -e

# Define project path & settings
PROJECT_DIR="/data/everythingsoil"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
VENV_PIP="$PROJECT_DIR/venv/bin/pip"
SETTINGS_MODULE="ets.settings.prod"

echo "=================================================="
echo " Starting deployment for Everything Soil"
echo " Time: $(date)"
echo "=================================================="

cd "$PROJECT_DIR"

# 1. Pull latest code from git repository
echo "--> Pulling latest code from Git..."
git pull origin main

# 2. Update Python dependencies if requirements.txt changed
echo "--> Installing/updating Python dependencies..."
$VENV_PIP install -r requirements.txt --quiet

# 3. Apply database migrations
echo "--> Running Django database migrations..."
$VENV_PYTHON manage.py migrate --settings=$SETTINGS_MODULE --noinput

# 4. Collect static files
echo "--> Collecting static files..."
$VENV_PYTHON manage.py collectstatic --settings=$SETTINGS_MODULE --noinput

# 5. Check Django system checks
echo "--> Running Django system checks..."
$VENV_PYTHON manage.py check --settings=$SETTINGS_MODULE

# 6. Backup latest Let's Encrypt SSL certs & Nginx config if updated
echo "--> Backing up SSL certs and Nginx configs..."
if [ -d "/etc/letsencrypt/live/everythingsoil.com" ]; then
    mkdir -p "$PROJECT_DIR/ssl" "$PROJECT_DIR/letsencrypt_backup"
    cp -L /etc/letsencrypt/live/everythingsoil.com/fullchain.pem "$PROJECT_DIR/ssl/" 2>/dev/null || true
    cp -L /etc/letsencrypt/live/everythingsoil.com/privkey.pem "$PROJECT_DIR/ssl/" 2>/dev/null || true
    cp -a /etc/letsencrypt/* "$PROJECT_DIR/letsencrypt_backup/" 2>/dev/null || true
fi
if [ -f "/etc/nginx/sites-available/everythingsoil.com" ]; then
    mkdir -p "$PROJECT_DIR/nginx"
    cp /etc/nginx/sites-available/everythingsoil.com "$PROJECT_DIR/nginx/everythingsoil.nginx.conf" 2>/dev/null || true
fi

# 7. Restart uWSGI & Reload Nginx
echo "--> Restarting uWSGI service..."
systemctl restart uwsgi-everythingsoil

echo "--> Reloading Nginx service..."
systemctl reload nginx

echo "=================================================="
echo " Deployment successful! Site live at https://everythingsoil.com"
echo "=================================================="
