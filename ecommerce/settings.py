"""
Django settings for ecommerce project.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# ===================================================
# SECURITY
# ===================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]


# ===================================================
# INSTALLED APPS
# ===================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Apps
    "products",
    "accounts",
    "cart",
    "orders",
    "wishlist",
    "reviews",
    "dashboard",
    "chat",
]


# ===================================================
# MIDDLEWARE
# ===================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "ecommerce.urls"


# ===================================================
# TEMPLATES
# ===================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "context_processors.cart_count",
                "context_processors.chat_notifications",
            ],
        },
    },
]


WSGI_APPLICATION = "ecommerce.wsgi.application"


# ===================================================
# DATABASE
# ===================================================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}


# ===================================================
# PASSWORD VALIDATION
# ===================================================

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


# ===================================================
# INTERNATIONALIZATION
# ===================================================

LANGUAGE_CODE = "en-us"

# Use local timezone for correct order times (e.g., India)
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ===================================================
# STATIC FILES
# ===================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

if DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ===================================================
# MEDIA FILES
# ===================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ===================================================
# CLOUDINARY
# ===================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

CLOUDINARY_ENABLED = all(
    [
        CLOUDINARY_STORAGE["CLOUD_NAME"],
        CLOUDINARY_STORAGE["API_KEY"],
        CLOUDINARY_STORAGE["API_SECRET"],
    ]
)


# ===================================================
# DJANGO 6 STORAGES
# ===================================================

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if CLOUDINARY_ENABLED
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ===================================================
# DEFAULT AUTO FIELD
# ===================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===================================================
# EMAIL
# ===================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Render / production settings
if os.environ.get("RENDER"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    CSRF_TRUSTED_ORIGINS = [
        os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/"),
    ]
    if not CSRF_TRUSTED_ORIGINS[0]:
        CSRF_TRUSTED_ORIGINS = []