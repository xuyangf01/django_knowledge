from django.db import models
from Base_app.BaseModel_apps import BaseModelApps
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from datetime import datetime


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
    effective_choice = (
        (1, "生效中"),
        (2, "已失效")
    )
    is_effective = models.SmallIntegerField(verbose_name="当前状态", choices=effective_choice, default=1)
    visit_count = models.BigIntegerField(verbose_name="文章访问量", default=0)
    active_endtime = models.DateTimeField(verbose_name="结束时间", default=datetime(2021, 1, 1, 00, 00, 00))

    def __str__(self):
        return "问题名：{}".format(self.qct_name)

    class Meta:
        verbose_name = "3-咨询问题"
        verbose_name_plural = verbose_name


# 用户评论模型
class QuestionComment(BaseModelApps):
    user_obj = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field="id",
                                 verbose_name="评论用户")
    comment_content = RichTextUploadingField(verbose_name="评论内容", null=True, blank=True, max_length=2048)
    question_obj = models.ForeignKey(to="QuestionCalssTheme", on_delete=models.CASCADE, to_field="t_id",
                                     verbose_name="评论文章")
    reply_question_comment = models.ForeignKey(to="QuestionComment", on_delete=models.CASCADE, to_field="t_id",
                                               verbose_name="上级评论", null=True)

    def __str__(self):
        if self.reply_question_comment is None:
            return '此为管理员回复的评论'
        return "此为用户一级评论"

    class Meta:
        verbose_name = "评论内容"
        verbose_name_plural = verbose_name
