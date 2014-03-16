import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'hsty0lt%gi2mi58&6xa)(014iwsyl8re29z91*my-!urs86c@s'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'api',
    'website',
    'django_extensions',
    'courses',
    'south',
    'django_nose',
    'accounts',
    'bootstrap3',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    # Required by allauth template tags
    "django.core.context_processors.request",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "django.contrib.messages.context_processors.messages",
)

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'  # TODO change to the user's page in future
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    },
    'google': {
        'SCOPE': ['email', 'https://www.googleapis.com/auth/plus.login']
    }
}

# TODO localize Required by allauth, this is based on the id of the database row
SITE_ID = 3  # localhost

# Allauth tries to send a verification email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '../templates').replace('\\', '/'),
)

ROOT_URLCONF = 'courseowl_django.urls'
WSGI_APPLICATION = 'courseowl_django.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

AUTH_PROFILE_MODULE = "user_management.UserProfile"
