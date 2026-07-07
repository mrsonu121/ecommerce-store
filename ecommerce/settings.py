"""
Django settings for ecommerce project.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-t7%*ikzvjc1u70sx-6s)qli1-j(u^2dnbn33sij*hiky_0^9&7"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]


# ===================================================
# INSTALLED APPS
# ===================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'products',
    'accounts',
    'cart',
    'orders',
    'wishlist',
    'reviews',
    'dashboard',
    'chat',
]


# ===================================================
# MIDDLEWARE
# ===================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


ROOT_URLCONF = 'ecommerce.urls'


# ===================================================
# TEMPLATES
# ===================================================

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [

            BASE_DIR / 'templates',

        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'context_processors.cart_count',

            ],

        },

    },

]


WSGI_APPLICATION = 'ecommerce.wsgi.application'


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

        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',

    },

]


# ===================================================
# INTERNATIONALIZATION
# ===================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ===================================================
# MEDIA FILES
# ===================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ===================================================
# DEFAULT AUTO FIELD
# ===================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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