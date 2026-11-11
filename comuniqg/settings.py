from pathlib import Path

from decouple import config
from django.conf.locale.pt_BR import formats as br_formats

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [host.strip() for host in config("ALLOWED_HOSTS").split(",")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # my apps
    "account",
    "clientes",
    "core",
    "dashboard",
    "databaseold",
    "faturamento",
    "produtos",
    "servicos",
    "tabelas",
    # other apps
    "rolepermissions",
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

ROOT_URLCONF = "comuniqg.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "comuniqg.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "USER": config("USER"),
        "PASSWORD": config("PASSWORD"),
        "HOST": config("HOST"),
        "PORT": config("PORT"),
        "NAME": config("NAME"),
    }
}

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

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

br_formats.DATE_FORMAT = "d/m/Y"

ROLEPERMISSIONS_MODULE = "comuniqg.roles"
# Sem a permissão, 403 em vez de mandar para o login: o login devolve quem
# já está logado para a tela pedida e isso virava um loop de redirecionamento
ROLEPERMISSIONS_REDIRECT_TO_LOGIN = False

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index_servico"
LOGOUT_REDIRECT_URL = "index_core"

STATIC_URL = "static/"
STATIC_ROOT = config("STATIC_ROOT_CONFIG")

MEDIA_URL = "media/"
MEDIA_ROOT = config("MEDIA_ROOT_CONFIG")


# Account Model
AUTH_USER_MODEL = "account.Account"
