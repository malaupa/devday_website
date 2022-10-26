"""
Django settings for devday project.

Originally generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

Please keep this list of settings sorted alphabetically!

"""
import json
import mimetypes
import os
from email.utils import parseaddr as parse_email_address
from typing import Any, Callable

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


def gettext(s):
    return s


_setting_json = None
_vault_integration = None


def get_setting(var_name, value_type: Callable[[str], Any] = str, default_value=None):
    """
    Try to get a setting from Vault or the environment and fallback to
    default_value if it is defined.

    Variables are transformed to uppercase before they are looked up in the
    environment.

    If no default is defined and the variable cannot be found in either
    Vault or the environment an ImproperlyConfigured exception is raised.

    :param var_name: variable name
    :param value_type: result type
    :param default_value: default value
    :return: variable from Vault or the environment
    """
    global _setting_json, _vault_integration

    if _setting_json is None:
        if "VAULT_URL" in os.environ:
            from devday.vault_integration import vault_integration

            _vault_integration = vault_integration
            _setting_json = _vault_integration.get_settings_from_vault()
        else:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as settings_json:
                    _setting_json = json.load(settings_json)
            else:
                _setting_json = {}

    if var_name.lower() in _setting_json:
        return _setting_json[var_name.lower()]

    if var_name in os.environ:
        value = os.environ[var_name]
        try:
            return value_type(value)
        except ValueError:
            raise ImproperlyConfigured(
                "Cannot interpret value %s as %s", value, value_type.__name__
            )

    if default_value is None:
        if "VAULT_URL" in os.environ:
            error_msg = (
                "Define and set {} in Vault key at {} or set the"
                " environment variable {}"
            ).format(var_name.lower(), _vault_integration.secret_url, var_name)
        else:
            error_msg = (
                "Set VAULT_URL, VAULT_ROLE_ID and VAULT_SECRET_ID to use"
                " settings in HashiCorp Vault, define settings in a"
                " settings.json file or set the environment variable {}"
            ).format(var_name)
        raise ImproperlyConfigured(error_msg)
    else:
        return default_value


def split_emails(value: str):
    return [parse_email_address(address) for address in value.split(",")]


def split_list(value: str):
    return [s.strip() for s in value.split(",")]


mimetypes.add_type("image/svg+xml", ".svg", True)

DEBUG = get_setting("DEBUG", bool, default_value=False)

# settings for django-django_registration
# see: https://django-registration.readthedocs.io/en/2.1.1/index.html
ACCOUNT_ACTIVATION_DAYS = 14
ALLOWED_HOSTS = get_setting(
    "ALLOWED_HOSTS", split_list, default_value=["0.0.0.0", "127.0.0.1", "localhost"]
)
AUTH_USER_MODEL = "attendee.DevDayUser"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CMS_LANGUAGES = {
    1: [
        {
            "code": "de",
            "name": gettext("de"),
            "public": True,
            "hide_untranslated": False,
            "redirect_on_fallback": True,
        }
    ],
    "default": {
        "fallbacks": ["de"],
        "redirect_on_fallback": True,
        "public": True,
        "hide_untranslated": False,
    },
}
CMS_PLACEHOLDER_CONF = {}
DJANGOCMS_STYLE_CHOICES = ["row", "container", "col-xs-12", "col-md-12"]
DJANGOCMS_STYLE_TEMPLATES = [
    # styles for bootstrap grid model
    ("row", gettext("row")),
    ("container", gettext("container")),
    ("col-xs-12", gettext("col-xs-12")),
    ("col-md-12", gettext("col-md-12")),
]
DJANGOCMS_PICTURE_RESPONSIVE_IMAGES = False
DJANGOCMS_PICTURE_TEMPLATES = (
    ("carousel", _("Image in carousel")),
    ("carousel_first", _("First image in carousel")),
    ("gallery", _("Image in galery")),
)

CMS_TEMPLATES = (
    ("devday_no_cta.html", _("Dev Day Page")),
    ("devday.html", _("Dev Day Page with Call to Action area")),
    ("devday_index.html", _("Dev Day Home Page")),
    (
        "devday_all_static_placeholders.html",
        _("Page with all static placeholders not for menu"),
    ),
)
CMS_PERMISSION = True
CRISPY_TEMPLATE_PACK = "bootstrap3"

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": get_setting("DEVDAY_PG_DBNAME"),
        "USER": get_setting("DEVDAY_PG_USER"),
        "PASSWORD": get_setting("POSTGRESQL_PASSWORD"),
        "HOST": get_setting("DEVDAY_PG_HOST"),
        "PORT": get_setting("DEVDAY_PG_PORT"),
    }
}
DEVDAY_FACEBOOK_URL = "https://www.facebook.com/events/193156441425350/"
DEVDAY_TWITTER_URL = "https://twitter.com/devdaydresden"
DEVDAY_XING_URL = "https://www.xing.com/events/dev-day-2018-1897927"

DEFAULT_EMAIL_SENDER = "info-bounce@devday.de"

INSTALLED_APPS = [
    "ckeditor",
    "corsheaders",
    "djangocms_admin_style",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework.authtoken",
    "devday.apps.DevDayApp",
    "event.apps.EventsConfig",
    "attendee.apps.AttendeeConfig",
    "talk.apps.SessionsConfig",
    "sponsoring",
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    "easy_thumbnails",
    "filer",
    "djangocms_text_ckeditor",
    "djangocms_style",
    "djangocms_column",
    "djangocms_file",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_video",
    "crispy_forms",
    "django_file_form",
    "django_file_form.ajaxuploader",
    "twitterfeed.apps.TwitterFeedConfig",
    "speaker.apps.SpeakerConfig",
    "django.contrib.postgres",
    "psqlextra",
    "drf_spectacular",
]

LANGUAGE_CODE = "de"
LANGUAGES = (
    ("de", gettext("de")),
    # ('en', gettext('en')),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MIDDLEWARE = [
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
]
MIGRATION_MODULES = {}

CORS_ALLOWED_ORIGINS = get_setting(
    "CORS_ALLOWED_ORIGINS",
    split_list,
    default_value=["https://www.devday.de", "https://devday.de"],
)
CORS_URLS_REGEX = r"^/api/.*$"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "devday.urls"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_setting("SECRET_KEY")

SPONSORING_OPEN = get_setting("SPONSORING_OPEN", bool, False)
SPONSORING_FROM_EMAIL = get_setting(
    "SPONSORING_FROM_EMAIL", default_value="info@devday.de"
)
SPONSORING_RECIPIENTS = get_setting(
    "SPONSORING_RECIPIENTS", split_list, default_value=["info@devday.de"]
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_AGE = None

SITE_ID = 1
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "devday", "static"),)

TALK_RESERVATION_CONFIRMATION_DAYS = 5
CONFIRMATION_SALT = get_setting("CONFIRMATION_SALT")

TALK_PUBLIC_SPEAKER_IMAGE_HEIGHT = 960
TALK_PUBLIC_SPEAKER_IMAGE_WIDTH = 636
TALK_THUMBNAIL_HEIGHT = 320

# Feedback for talks is allowed when that many minutes passed since the talk started
TALK_FEEDBACK_ALLOWED_MINUTES = 30

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "devday", "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
                "cms.context_processors.cms_settings",
                "devday.contextprocessors.devdaysettings_contextprocessor",
                "talk.context_processors.committee_member_context_processor",
                "talk.context_processors.reservation_context_processor",
                "twitterfeed.contextprocessors.twitter_feed_context_processor",
                "event.contextprocessors.current_event_contextprocessor",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    # 'easy_thumbnails.processors.scale_and_crop',
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)
TIME_ZONE = "Europe/Berlin"
TWITTERFEED_PROXIES = {}
TWITTERFEED_PATHS = ["/"]
TWITTERFEED_INTERVAL = get_setting("TWITTERFEED_INTERVAL", int, 60)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s %(process)d"
                " %(thread)s %(message)s"
            )
        },
        "simple": {"format": "%(asctime)s %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        }
    },
    "loggers": {},
}

USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMINUSER_EMAIL = get_setting("DEVDAY_ADMINUSER_EMAIL", default_value="admin@devday.de")

DEFAULT_FROM_EMAIL = get_setting("DEFAULT_FROM_EMAIL", default_value="info@devday.de")

EMAIL_HOST = get_setting("EMAIL_HOST", default_value="mail")
EMAIL_SUBJECT_PREFIX = get_setting("EMAIL_SUBJECT_PREFIX", default_value="[Dev Day] ")

_local_log_names = [
    "django",
    "django.request",
    "cms",
    "devday",
    "attendee",
    "event",
    "speaker",
    "talk",
    "twitterfeed",
]

RUN_SCHEDULED_JOBS = get_setting(
    "RUN_SCHEDULED_JOBS", value_type=bool, default_value=False
)

if DEBUG:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "devday.extras.show_toolbar_callback"
    }

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    for log_name in _local_log_names:
        LOGGING["loggers"][log_name] = {
            "handlers": ["console"],
            "level": "INFO",
        }
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    TWITTERFEED_PROXIES = {
        "http": "",
        "https": "",
    }
else:
    ADMINS = get_setting("ADMINS", split_emails)
    LOGGING.update(
        {
            "filters": {
                "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
            },
            "loggers": {
                "django.request": {
                    "handlers": ["console", "mail_admins"],
                    "level": "ERROR",
                    "propagate": False,
                }
            },
        }
    )

    LOGGING["handlers"].update(
        {
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
                "filters": ["require_debug_false"],
            },
        }
    )

    for log_name in _local_log_names:
        LOGGING["loggers"][log_name] = {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        }

    TWITTERFEED_PROXIES = {
        "http": get_setting("http_proxy"),
        "https": get_setting("https_proxy"),
    }

SPECTACULAR_SETTINGS = {
    "SERVE_PUBLIC": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
}
