from django.db import models
from Base_app.BaseModel_apps import BaseModelApps
from ckeditor_uploader.fields import RichTextUploadingField


# 大类主题
class BigClassTheme(BaseModelApps):
    bct_name = models.CharField("大类主题名", max_length=32, null=False)
    bct_describe = models.TextField("主题描述", max_length=500, default="此大类主题暂无描述")

    def __str__(self):
        return "大类主题名：{}".format(self.bct_name)

    class Meta:
        verbose_name = "1-大类主题"
        verbose_name_plural = verbose_name


# 子类主题
class SubClassTheme(BaseModelApps):
    bct_id = models.ForeignKey(to="BigClassTheme", on_delete=models.CASCADE, to_field="t_id",
                               verbose_name="对应的大类主题ID")
    sct_name = models.CharField("子类主题名", max_length=32, null=False)
    sct_describe = models.TextField("子主题描述", max_length=500, default="此子类主题暂无描述")

    def __str__(self):
        return "子类主题名：{}".format(self.sct_name)

    class Meta:
        verbose_name = "2-子类主题"
        verbose_name_plural = verbose_name


# 咨询问题
class QuestionCalssTheme(BaseModelApps):
    bct_id = models.ForeignKey(to="BigClassTheme", on_delete=models.CASCADE, to_field="t_id",
                               verbose_name="对应的大类主题ID")
    sct_id = models.ForeignKey(to="SubClassTheme", on_delete=models.CASCADE, to_field="t_id",
                               verbose_name="对应的子类主题ID")
    qct_name = models.CharField("求助问题", max_length=128, null=False)
    qct_method = RichTextUploadingField(null=True, blank=True, verbose_name="内容描述", default="暂无内容")
    qct_comment = RichTextUploadingField(verbose_name="内部评语指导", null=True, blank=True, default="暂无内容")

    def __str__(self):
        return "问题名：{}".format(self.qct_name)

    class Meta:
        verbose_name = "3-咨询问题"
        verbose_name_plural = verbose_name
