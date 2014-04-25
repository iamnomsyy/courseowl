DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['.courseowl.com', '.courseowl.com.']
STATIC_ROOT = "/var/www/courseowl_static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'owl',
        'USER': 'owl',
        'PASSWORD': 'qwerty123',
        'HOST': '10.128.233.5'
    }
}
