import os
from pathlib import Path

import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "les2peresnoel"

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "5vxou4in7%f+p$x2a0kzhk379$#1q-0+646v*_((k%s-$+7=go"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)
# DEBUG = True
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=False)
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
# Application definition
DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "les2peresnoel.core.apps.CoreConfig",
    "les2peresnoel.marketplace.apps.MarketplaceConfig",
    "les2peresnoel.users.apps.UsersConfig",
    "les2peresnoel.stores.apps.StoresConfig",
    "les2peresnoel.providers.apps.ProvidersConfig",
    "les2peresnoel.payments.apps.PaymentsConfig",
    "les2peresnoel.accounting.apps.AccountingConfig",
    "les2peresnoel.licences.apps.LicencesConfig",
]

THIRD_PARTY_APPS = [
    "ckeditor",
    "ckeditor_uploader",
    "sweetify",
    "allauth",
    "allauth.account",
    "allauth.socialaccount.providers.google",
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_htmx",
    "corsheaders",
    # "django_paypal",
    "paypal.standard.ipn",
    "mail_templated",
    "compressor",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

USE_I18N = True
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "dj_shop_cart.context_processors.cart",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

LANGUAGES = [
    ("fr", "French"),
    ("en", "English"),
]

CURRENT_LANGUAGE = "fr"

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///l2pn")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Password validation

# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/statics/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

VENV_PATH = os.path.dirname(BASE_DIR)
# STATIC_ROOT = os.path.join("static_root")


MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"

# COMPRESS_STORAGE = STATICFILES_STORAGE
# COMPRESS_OFFLINE_MANIFEST_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL


# print(MEDIA_ROOT)
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
STATICFILES_DIRS = [os.path.join(BASE_DIR, "statics")]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# STORAGES = {
# "default": {
#     "BACKEND": "django.core.files.storage.FileSystemStorage",
# },
# "staticfiles": {
#     "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
# },
# }


CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_UPLOAD_MAX_SIZE = "12MB"
DATA_UPLOAD_MAX_MEMORY_SIZE = 12582912  # 12 MB

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        # 'skin': 'office2013',
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "custom_toolbar": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "about", "items": ["About"]},
            "/",  # put this to force next toolbar on new line
            {
                "name": "yourcustomtools",
                "items": [
                    # put the name of your editor.ui.addButton here
                    "Preview",
                    "Maximize",
                ],
            },
        ],
        "toolbar": "custom_toolbar",  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                # 'devtools',
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
            ]
        ),
    }
}
SWEETIFY_SWEETALERT_LIBRARY = "sweetalert2"

SWEETIFY_TOAST_TIMER = 3000

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {"client_id": "123", "secret": "456", "key": ""}
    }
}

AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

LOGIN_REDIRECT_URL = "marketplace:home"

DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USERNAME_REQUIRED = False
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://docs.allauth.org/en/latest/account/configuration.html
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "les2peresnoel.users.adapters.AccountAdapter"
# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "les2peresnoel.users.forms.UserSignupForm"}
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "les2peresnoel.users.adapters.SocialAccountAdapter"
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "les2peresnoel.users.forms.UserSocialSignupForm"}

MARKETPLACE_DEFAULT = {
    "category_cover": "/static/images/default.jpg",
    "product_cover": "/static/images/default.jpg",
}


SHIPPING_FEES = 0


BASE_ACCOUNT_CODE_MAP = {
    "CUSTOMER_ACCOUNTS_RECEIVABLE": "411000",
    "BANK": "512000",
    "BORROWINGS_FROM_CREDIT_INSTITUTIONS": "164000",
    "INTEREST_CHARGES": "661000",
    "SALES_COMMISSIONS": "622200",
    "CAPITAL": "101000",
    "RAW_MATERIALS_PURCHASES": "601000",
    "INDUSTRIAL_EQUIPMENT": "215400",
    "SALES_OF_FINISHED_PRODUCTS": "701000",
    "SUPPLIER_DEBT": "401000",
}

TVA_RATE = 5.5

LINK_TRANSACTION_TO_JOURNAL_ENTRY = True

# PAYPAL INTEGRATION
PAYPAL_RECEIVER_EMAIL = env("PAYPAL_RECEIVER_EMAIL")
PAYPAL_TEST = True


PAYPAL_CLIENT_ID = ""
PAYPAL_CLIENT_SECRET = ""


FROM_EMAIL = "contact@mperesbonheur.com"
LICENCE_EXPIRATION_DAYS = 365

# Configuration CORS
# CORS_ALLOWED_ORIGINS = ["https://antelope-driven-utterly.ngrok-free.app"]

CORS_ALLOW_CREDENTIALS = True


# CSRF_TRUSTED_ORIGINS = ["https://antelope-driven-utterly.ngrok-free.app"]


# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': [
#             'redis://127.0.0.1:26379/0',
#             'redis://127.0.0.1:26380/0',
#             'redis://127.0.0.1:26381/0',
#         ],
#         # 'LOCATION': env('REDIS_URL'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.SentinelClient',
#             'SENTINEL_KWARGS': {
#                 'socket_timeout': 0.1,
#             },
#             'CONNECTION_POOL_KWARGS': {
#                 'max_connections': 100,
#                 'retry_on_timeout': True,
#             }
#         }
#     }
# }


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),  # Use the appropriate Redis server URL
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# Unfolf settings

UNFOLD = {
    "SITE_TITLE": "ADMINISTRATION",
    "SITE_HEADER": "PERES BONHEUR",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    # "ENVIRONMENT": "sample_app.environment_callback",
    # "DASHBOARD_CALLBACK": "sample_app.dashboard_callback",
    # "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
        lambda request: static("unfold/css/font.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "255 235 235",  # Lightest shade of #d71515
            "100": "255 204 204",
            "200": "255 153 153",
            "300": "255 102 102",
            "400": "255 51 51",
            "500": "215 21 21",  # #d71515
            "600": "194 19 19",
            "700": "173 17 17",
            "800": "153 15 15",
            "900": "133 13 13",
            "950": "102 10 10",  # Darkest shade of #d71515
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        # "navigation": [
        #     {
        #         "title": _("Navigation"),
        #         "separator": True,  # Top border
        #         "collapsible": True,  # Collapsible group of links
        #         "items": [
        #             {
        #                 "title": _("Dashboard"),
        #                 "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
        #                 "link": reverse_lazy("admin:index"),
        #                 # "badge": "sample_app.badge_callback",
        #                 "permission": lambda request: request.user.is_superuser,
        #             },
        #             {
        #                 "title": _("Users"),
        #                 "icon": "people",
        #                 "link": reverse_lazy("admin:users_user_changelist"),
        #             },
        #         ],
        #     },
        # ],
    },
    # "TABS": [
    #     {
    #         "models": [
    #             "app_label.model_name_in_lowercase",
    #         ],
    #         # "items": [
    #         #     {
    #         #         "title": _("Your custom title"),
    #         #         "link": reverse_lazy("admin:app_label_model_name_changelist"),
    #         #         "permission": "sample_app.permission_callback",
    #         #     },
    #         # ],
    #     },
    # ],
}
