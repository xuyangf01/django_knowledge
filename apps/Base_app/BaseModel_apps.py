from django.db import models


class BaseModelApps(models.Model):
    t_id = models.AutoField('ID', primary_key=True)
    creator = models.CharField("创建人", max_length=20, null=False)
    updator = models.CharField("修改人", max_length=20, default="not")
    create_timestamp = models.DateTimeField("创建时间", auto_now_add=True)
    last_edit_timestamp = models.DateTimeField("最后修改时间", auto_now=True)
    show_choice = (
        (1, '显示'),
        (2, '隐藏'),
    )
    is_show = models.SmallIntegerField("页面展示", choices=show_choice, default=1)

    class Meta:
        abstract = True

