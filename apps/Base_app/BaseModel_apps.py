from django.db import models
from django.utils import timezone


class BaseModelApps(models.Model):
    t_id = models.AutoField('ID', primary_key=True)
    creator = models.CharField("创建人", max_length=20, null=False)
    updator = models.CharField("修改人", max_length=20, default="not")
    create_timestamp = models.DateTimeField("创建时间", auto_now_add=True)
    # last_edit_timestamp = models.DateTimeField("最后修改时间", auto_now=True)
    last_edit_timestamp = models.DateTimeField("最后修改时间", default=timezone.now())
    show_choice = (
        (1, '显示'),
        (2, '隐藏'),
    )
    is_show = models.SmallIntegerField("页面展示", choices=show_choice, default=1)

    popular_choice = (
        (1, '一般问题'),
        (2, '热门问题'),
    )
    is_popular = models.SmallIntegerField("是否热门问题", choices=popular_choice, default=1)

    priority_choice = (
        (1, '1级优先（最高）'),
        (2, '2级优先'),
        (3, '3级优先（一般）'),
        (4, '4级优先'),
        (5, '5级优先（最低）'),
    )

    is_priority = models.SmallIntegerField("排序优先级", choices=priority_choice, default=3)

    class Meta:
        abstract = True
