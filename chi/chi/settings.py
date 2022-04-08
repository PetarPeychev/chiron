import io
import os
from urllib.parse import urlparse
from pathlib import Path

import environ
import google.auth
from google.cloud import secretmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEV = True # TODO: Set to false.

if DEV:
    DEBUG = True
    SECRET_KEY = "&ie=^3_^r5v(=#ju4fj*q#jpa_(4rpw)dykaev@y(&t^7&h7t*"
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'debug_database',
        }
    }
    BASE_DIR = Path(__file__).resolve().parent.parent
    STATICFILES_DIRS = [
        BASE_DIR / "chi/static",
    ]
    STATIC_URL = 'static/'
else:
    # SECURITY WARNING: don't run with debug turned on in production!
    # Change this to "False" when you are ready for production
    env = environ.Env(DEBUG=(bool, True))
    env_file = os.path.join(BASE_DIR, ".env")

    try:
        _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        pass

    if os.path.isfile(env_file):
        env.read_env(env_file)

    elif os.getenv("TRAMPOLINE_CI", None):
        placeholder = (
            f"SECRET_KEY=a\n"
            "GS_BUCKET_NAME=None\n"
            f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
        )
        env.read_env(io.StringIO(placeholder))
    elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "chi_settings")
        name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

        env.read_env(io.StringIO(payload))
    else:
        raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
    SECRET_KEY = env("SECRET_KEY")

    DEBUG = env("DEBUG")
    
    CLOUD_RUN_SERVICE_URL = env("CLOUD_RUN_SERVICE_URL", default=None)
    if CLOUD_RUN_SERVICE_URL:
        ALLOWED_HOSTS = [urlparse(CLOUD_RUN_SERVICE_URL).netloc]
        CSRF_TRUSTED_ORIGINS = [CLOUD_RUN_SERVICE_URL]
        # SECURE_SSL_REDIRECT = True
    else:
        ALLOWED_HOSTS = ["*"]
        
    DATABASES = {"default": env.db()}

    if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
        DATABASES["default"]["HOST"] = "127.0.0.1"
        DATABASES["default"]["PORT"] = 5433

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "chi/static")
    ]
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    STATIC_URL = "/static/"
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
    GS_OBJECT_PARAMETERS = {
        "cache_control": "no-cache"
    }

INSTALLED_APPS = [
    "materializecssform",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chi",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware"
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "chi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "chi/templates")],
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
WSGI_APPLICATION = "chi.wsgi.application"

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'