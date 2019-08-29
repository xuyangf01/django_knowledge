# encoding: utf-8
from __future__ import absolute_import  # 避免就近原则

import os
from celery import Celery
from django.conf import settings

# 设置项目运行的环境变量DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "knowledge_sys.settings")  # DAdmin为settings所在的文件（模块）

# 创建celery应用
app = Celery('my_tasks')

# Celery加载配置
app.config_from_object('django.conf:settings')

# 如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。
# 比如你添加了一个任务，在django中会实时地检索出来。
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

