# -*- coding: utf-8 -*-
from __future__ import absolute_import  # 避免就近原则
import django
django.setup()
from knowledge_sys.celery import app
from show_idea.models import QuestionCalssTheme
from datetime import datetime


@app.task
def check_effective():
    now_time = datetime.now()
    print("当前时间：{}".format(now_time))
    # 如果活动结束时间小于当前时间，就更改状态为 2 ：已失效
    res = QuestionCalssTheme.objects.filter(active_endtime__lt=now_time, is_effective=1).update(is_effective=2)
    return "本次检查活动失效个数新增-{}-个".format(res)
