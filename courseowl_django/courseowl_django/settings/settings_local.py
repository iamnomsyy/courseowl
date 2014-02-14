DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
PREDICTIONIO_IP = "107.170.20.8"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'owl',
        'USER': 'owl',
        'PASSWORD': 'qwerty123',
        'HOST': 'localhost'
    }
}
