import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lz186=w9n8taby(0@#ncba80)40rnz4+#pbj$pmf*==9#*ap(t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

TABLE_PREFIX = 'easydo_'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    "django_apscheduler",
    'article',
    'common',
    'system',
    'user',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.ApiLoggingMiddleware',
]
ROOT_URLCONF = 'EasyDo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'EasyDo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'easy_do',
        'USER': 'easy_do',
        'PASSWORD': 'S5237ysfh2Y5hXKx',
        'HOST': '127.0.0.1',
        'POST': 3306,
    }
}
# ************** redis配置 ************** #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6380/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

AUTH_USER_MODEL = 'user.Users'
USERNAME_FIELD = 'username'
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    'DATE_FORMAT': "%Y-%m-%d",
    'DEFAULT_FILTER_BACKENDS': (
        # 'django_filters.rest_framework.DjangoFilterBackend',
        # 'dvadmin.utils.filters.CustomDjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'dvadmin.utils.pagination.CustomPagination',  # 自定义分页
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 只有经过身份认证确定用户身份才能访问
        # 'rest_framework.permissions.IsAdminUser', # is_staff=True才能访问 —— 管理员(员工)权限
        # 'rest_framework.permissions.AllowAny', # 允许所有
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly', # 有身份 或者 只读访问(self.list,self.retrieve)
    ],
    'EXCEPTION_HANDLER': 'utils.exception.CustomExceptionHandler',  # 自定义的异常处理
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = 'media'  # 项目下的目录
MEDIA_URL = "/media/"  # 跟STATIC_URL类似，指定用户可以通过这个url找到文件

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================================================= #
# ******************* 跨域的配置 ******************* #
# ================================================= #

# 全部允许配置
CORS_ORIGIN_ALLOW_ALL = True
# 允许cookie
CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作



# ================================================= #
# ********************* 日志配置 ******************* #
# ================================================= #

# log 配置部分BEGIN #
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))

# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,  # 最多备份5个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 3,  # 最多备份3个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'scripts': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'django.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}


# ================================================= #
# ****************** simplejwt配置 ***************** #
# ================================================= #
from datetime import timedelta

SIMPLE_JWT = {
    # token有效时长
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    # token刷新后的有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 设置前缀
    # 'AUTH_HEADER_TYPES': ('JWT',),
    'ROTATE_REFRESH_TOKENS': True,
}

# ================================================= #
# ******************** 登录方式配置 ******************** #
# ================================================= #

AUTHENTICATION_BACKENDS = [
    'utils.backends.CustomBackend'
]
