"""
Django settings for knowledge_sys project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '23rnma#tz7s5-2tpw5(sp!*6ceqnuurfa18u()*x)xu)w=*soa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',            # haystack_whoosh 搜索引擎
    # 'show_idea.apps.ShowIdeaConfig',    # 应用app
    'show_idea',  # 应用app
    'celery_mytasks',
    'djcelery',  # 定时任务celery插件或开发异步框架
    'ckeditor',            # 富文本编辑器
    'ckeditor_uploader',   # 富文本上传功能


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'knowledge_sys.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.request",
# )

WSGI_APPLICATION = 'knowledge_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'knowledge_sys',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

###########################################################
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'my_static')
]

############################################################
DEFAULT_CHARSET = 'utf-8'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'my_static')


############## 添加搜索引擎 #################################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 每页显示搜索结果数目为10
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50
# 自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

############## 富文本编辑器 ################################
CKEDITOR_UPLOAD_PATH = "images/"
# CKEDITOR_JQUERY_URL ='js/jquery-3.2.1.min.js'
# CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'language': 'zh-cn',
        'toolbar_YourCustomToolbarConfig': [

            {'name': 'clipboard', 'items': ['Undo', 'Redo', '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-']},
            {'name': 'tools', 'items': ['Maximize']},
            '/',
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'paragraph',
             'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'document', 'items': ['Source']},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'width': '100%',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_BROWSE_SHOW_DIRS = True

################### celery 定时任务配置 #############################
import djcelery
from celery.schedules import timedelta, crontab

djcelery.setup_loader()  # 开始加载当前所有安装app中的task

# 使用redis代理来分发任务
BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_IMPORTS = ('show_idea.tasks')  # 导入任务，可以执行的异步任务
CELERY_TIMEZONE = 'Asia/Shanghai'  # 中国时区
CELERYD_CONCURRENCY = 3
# # 任务存入到数据库中
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYBEAT_SCHEDULE = {  # 定时器策略
    # 定时任务一：　每隔30s运行一次
    # 'test1': {
    #     "task": "celery_mytasks.tasks.hello_world",
    #     "schedule": timedelta(seconds=10),
    #     "args": (),
    # },
    u'检查活动是否结束': {
        "task": "show_idea.tasks.check_effective",
        "schedule": crontab(minute='*', hour='18-20'),
        # "schedule": timedelta(seconds=10),
        "args": (),
    },
}

