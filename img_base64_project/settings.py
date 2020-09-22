import os
import dj_database_url
import django_heroku

DATA_UPLOAD_MAX_MEMORY_SIZE = os.environ['DATA_UPLOAD_MAX_MEMORY_SIZE']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework', 
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'drf_yasg',
    'rest_auth',
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount', 
    'rest_auth.registration', 
    'main.apps.MainConfig',
    'api.apps.ApiConfig',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
SITE_ID = 1 


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
           'rest_framework.authentication.SessionAuthentication',
       ],
    "DEFAULT_SCHEMA_CLASS":"rest_framework.schemas.coreapi.AutoSchema"
}

DOMAIN_NAME =  "https://image2base64.herokuapp.com"

API_URL =  u'{0}/{1}'.format(DOMAIN_NAME,"api/v1/")



SWAGGER_SETTINGS = {
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'DEFAULT_API_URL': API_URL,
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'main.middleware.RequestDataTooBigMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ORIGIN_WHITELIST = (
  'https://image2base64.herokuapp.com'
)



ROOT_URLCONF = 'img_base64_project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.contextprocessors.landing',
                'main.contextprocessors.update',
                'main.contextprocessors.contact_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'img_base64_project.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


SITE_NAME  = "Image2base64"



CSRF_FAILURE_VIEW = "main.views.csrf_byepass"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

FILE_URL ='/file/'
FILE_ROOT = os.path.join(BASE_DIR, 'file/')

PASTE_URL ='/paste/'
PASTE_ROOT = os.path.join(BASE_DIR, 'paste/')

LINK_URL = '/link/'
LINK_ROOT = os.path.join(BASE_DIR, 'link/')

ENCODE_URL = '/encode_link/'
ENCODE_ROOT = os.path.join(BASE_DIR, 'encode_link/')

FRONTEND_URL = '/front-end/'
FRONTEND_ROOT = os.path.join(BASE_DIR, 'front-end/')