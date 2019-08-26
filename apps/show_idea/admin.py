from django.contrib import admin, messages
from show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme

admin.site.disable_action('delete_selected')


class BaseAdmin(admin.ModelAdmin):
    ordering = ('-last_edit_timestamp',)
    actions = ['delete_selected', ]

    # 增加批量删除动作
    def delete_selected(self, request, queryset):
        count = len(queryset)
        if request.user.is_superuser:
            for i in queryset:
                i.delete()
            self.message_user(request, '{}-条记录删除成功！！'.format(count), messages.SUCCESS)
        else:
            self.message_user(request, "您不是超级管理员，不可以执行批量删除", messages.WARNING)

    # 重写admin保存方法
    def save_model(self, request, obj, form, change):
        # # 当对象是大类主题且设置隐藏时     2--隐藏
        if isinstance(obj, BigClassTheme):
            SubClassTheme.objects.filter(bct_id=obj.t_id).update(is_show=obj.is_show)
            QuestionCalssTheme.objects.filter(bct_id=obj.t_id).update(is_show=obj.is_show)

        elif isinstance(obj, SubClassTheme):
            bct_obj = BigClassTheme.objects.get(t_id=obj.bct_id_id)
            # 如果大类主题是隐藏，那么子主题与问题类全部是隐藏
            if bct_obj.is_show == 2:  # 隐藏
                obj.is_show = bct_obj.is_show
                self.message_user(request,
                                  '保存成功，WARNING：大类主题<{}>为 <隐藏> 状态，子类和问题默认隐藏且无法修改为显示！！'.format(bct_obj.bct_name),
                                  messages.WARNING)
            QuestionCalssTheme.objects.filter(sct_id=obj.t_id).update(is_show=obj.is_show, bct_id=obj.bct_id)

        elif isinstance(obj, QuestionCalssTheme):
            sct_obj = SubClassTheme.objects.get(t_id=obj.sct_id_id)
            # 如果子类主题是隐藏，那么问题类全部是隐藏
            if sct_obj.is_show == 2:  # 隐藏
                obj.is_show = sct_obj.is_show
                self.message_user(request, '保存成功，WARNING：子类主题<{}>为 <隐藏> 状态，问题默认隐藏且无法修改为显示！！'.format(sct_obj.sct_name),
                                  messages.WARNING)
            # 设置问题的外键bct_id 的值
            obj.bct_id = SubClassTheme.objects.get(t_id=obj.sct_id_id).bct_id

        if not obj.creator:
            obj.creator = request.user.username
        obj.updator = request.user.username
        super().save_model(request, obj, form, change)

    delete_selected.short_description = '删除所选(仅限超级管理员)'


@admin.register(BigClassTheme)
class BigClassThemeAdmin(BaseAdmin):
    list_display = (
        'bct_name', 'creator', 'updator', "is_show", 'is_popular', 'is_priority', 'last_edit_timestamp',
        'create_timestamp')
    list_filter = ("is_show", 'creator', 'updator')
    list_editable = ["is_show", 'is_popular', 'is_priority']

    search_fields = ("bct_name", "creator", "bct_describe")
    fields = ['bct_name', "bct_describe", 'is_show', "is_popular", 'is_priority']


@admin.register(SubClassTheme)
class SubClassThemeAdmin(BaseAdmin):
    list_display = (
        'sct_name', 'creator', 'updator', 'bct_id', "is_show", 'is_popular', 'is_priority', 'last_edit_timestamp',
        'create_timestamp')
    list_filter = ("is_show", 'creator', 'updator', 'bct_id')
    list_editable = ['bct_id', "is_show", 'is_popular', 'is_priority']

    search_fields = ("sct_name", "creator", "sct_describe")
    fields = ['bct_id', 'sct_name', "sct_describe", 'is_show', "is_popular", 'is_priority']


@admin.register(QuestionCalssTheme)
class QuestionCalssThemeAdmin(BaseAdmin):
    list_display = (
        'qct_name', 'creator', 'updator', 'bct_id', 'sct_id', "is_show", 'is_popular', 'is_priority',
        'last_edit_timestamp', 'create_timestamp')
    list_filter = ("is_show", 'creator', 'updator', 'bct_id', 'sct_id')
    list_editable = ['sct_id', "is_show", 'is_popular', 'is_priority']

    search_fields = ("qct_name", "creator", "qct_method")
    fields = ['sct_id', 'qct_name', "qct_method", 'is_show', "is_popular", 'is_priority', 'qct_comment']


admin.site.site_header = '亚博知识库系统'
admin.site.site_title = '亚博知识库'
