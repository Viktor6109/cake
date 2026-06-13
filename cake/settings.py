"""
Django settings for cake project.
"""

from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECURITY
# ==============================================================================

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())


# ==============================================================================
# APPLICATIONS
# ==============================================================================

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "core",
    "catalog",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cake.urls"

WSGI_APPLICATION = "cake.wsgi.application"


# ==============================================================================
# TEMPLATES
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "ru"  # Русский — основной язык сайта (Прага)

TIME_ZONE = "Europe/Prague"

USE_I18N = True

USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)  # Используется при деплое: python manage.py collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# SECURITY HEADERS (активны только в продакшне, т.е. когда DEBUG=False)
# ==============================================================================

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 год — включить HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True  # Редирект HTTP → HTTPS
    SESSION_COOKIE_SECURE = True  # Cookie только по HTTPS
    CSRF_COOKIE_SECURE = True  # CSRF-токен только по HTTPS
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
