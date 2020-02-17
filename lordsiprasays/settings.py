import os
# import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG:
    # To avoid transmitting the CSRF cookie over HTTP accidentally
    CSRF_COOKIE_SECURE = True
    # To avoid transmitting the session cookie over HTTP accidentally
    SESSION_COOKIE_SECURE = True
    # To redirect all HTTP requests to HTTPS
    SECURE_SSL_REDIRECT = True

# Assign a session key to anyone accessing the website
SESSION_SAVE_EVERY_REQUEST = True
# Ensures user is logged out as soon as browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Ensures user is logged out after 24 hours
SESSION_COOKIE_AGE = 86400

ALLOWED_HOSTS = ['lordsiprasays.pythonanywhere.com', 'lordsiprasays.herokuapp.com', '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    # Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party Apps
    'crispy_forms',
    'admin_honeypot',

    # User Apps
    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.OneSessionPerUserMiddleware',  # Added
]

# Required for Django Debug Toolbar
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',  # Added
    ]

    INTERNAL_IPS = [
        '127.0.0.1',
    ]

ROOT_URLCONF = 'lordsiprasays.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lordsiprasays.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Useful to trigger notification emails
ADMINS = [
    ("", os.environ.get('PERSONAL_EMAIL')),
]

# Change the built in User model to CustomUser model
AUTH_USER_MODEL = 'users.CustomUser'  # <app>.<model>

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Defining directory to store static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'

# Required for Heroku deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Adding static file compression and caching support in deployment
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Defining directory to store media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Defining which page to redirect to once user logs in
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'users-login'

# Required to access location of user using geoip2
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# Set the default front end to use for Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Setup email backend for gmail and google apps
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('PERSONAL_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True

# Enable logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'LordSipraSays_logs.log',
        },

        'console': {
            'class': 'logging.StreamHandler',
        },

    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Activate Django-Heroku.
# django_heroku.settings(locals(), logging=False)
