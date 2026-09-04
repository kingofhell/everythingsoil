"""
Production settings for ets project.
"""

import dj_database_url
from .base import *

DEBUG = False

# Production Allowed Hosts and CSRF Origins
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['everythingsoil.com', 'www.everythingsoil.com'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['https://everythingsoil.com', 'https://www.everythingsoil.com'])

# Database configuration via DATABASE_URL or DB_* environment variables
db_url = env('DATABASE_URL', default=None)
if not db_url and env('DB_NAME', default=None) and env('DB_HOST', default=None):
    db_user = env('DB_USER', default='root')
    db_password = env('DB_PASSWORD', default='')
    db_host = env('DB_HOST')
    db_port = env('DB_PORT', default='3306')
    db_name = env('DB_NAME')
    db_url = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

DATABASES = {
    'default': dj_database_url.config(
        default=db_url or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False
    )
}

# HTTPS and security settings behind Nginx reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)

# Static and media files configuration for Nginx
STATIC_ROOT = env('STATIC_ROOT', default=BASE_DIR / 'staticfiles')
MEDIA_ROOT = env('MEDIA_ROOT', default=BASE_DIR / 'media')
