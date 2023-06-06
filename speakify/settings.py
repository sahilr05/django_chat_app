import os
from distutils.util import strtobool

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.getenv(name)
        try:
            return bool(strtobool(value))
        except ValueError as e:
            error_msg = "{} is an invalid value for {}".format(value, name)
            raise ImproperlyConfigured(error_msg) from e
    return default_value


def get_env_variable_or_default(name, default_value):
    if name in os.environ:
        return os.getenv(name)
    else:
        if type(default_value) == "int":
            return int(default_value)
        else:
            return default_value


def get_env_variable(var_name):
    try:
        return os.getenv(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


def generate_secret_key(filename):
    f = open(filename, "w")
    f.write(f"SECRET_KEY={get_random_secret_key()}")
    f.close()


DEBUG = get_bool_from_env("DEBUG", True)

try:
    from secret_key import SECRET_KEY  # NOQA
except ImportError:
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    generate_secret_key(os.path.join(SETTINGS_DIR, "secret_key.py"))
    from secret_key import SECRET_KEY  # NOQA

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "speakify"]


INSTALLED_APPS = [
    'chat_app',
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom
    "accounts",
    # Third-party
    "widget_tweaks",
    "django_extensions",
    "channels",
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

ROOT_URLCONF = "speakify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# DATABASES = {
#     "default": {
#         "ENGINE": get_env_variable_or_default(
#             "SQL_ENGINE", "django.db.backends.postgresql"
#         ),
#         "NAME": get_env_variable_or_default("SQL_DATABASE", "speakify"),
#         "USER": get_env_variable_or_default("SQL_USER", "postgres"),
#         "PASSWORD": get_env_variable_or_default("SQL_PASSWORD", "password"),
#         "HOST": get_env_variable_or_default("SQL_HOST", "localhost"),
#         "PORT": get_env_variable_or_default("SQL_PORT", 5432),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR + "/" + "db.sqlite3",
    }
}


WSGI_APPLICATION = "speakify.wsgi.application"
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGOUT_REDIRECT_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:add_interest"
LOGIN_URL = "accounts:login"

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Daphne
ASGI_APPLICATION = "speakify.asgi.application"

CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "channels.layers.InMemoryChannelLayer"
	}
}
