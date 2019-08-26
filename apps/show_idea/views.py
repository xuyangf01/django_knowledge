from django.shortcuts import render
from django.views import View
from show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme


def page_not_found(request, **kwargs):
    return render(request, 'base_html/404.html')


class Index(View):
    def get(self, request):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_qyset = QuestionCalssTheme.objects.filter(is_show=1, is_popular=2).order_by('is_priority')
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset,
        }
        return render(request, 'new_showhtml/index.html', context=context)


class SctListShow(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        stc_qryset = SubClassTheme.objects.filter(is_show=1, bct_id=t_id).order_by('is_priority')
        if not len(stc_qryset):
            return render(request, 'base_html/404.html')
        context = {
            "btc_obj_qset": btc_obj_qset,
            "stc_qryset": stc_qryset,
        }
        return render(request, 'new_showhtml/s_list_show.html', context=context)


class QctListShow(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_qyset = QuestionCalssTheme.objects.filter(is_show=1, sct_id_id=t_id).order_by('is_priority')
        if not len(qct_qyset):
            return render(request, 'base_html/404.html')
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset
        }
        return render(request, 'new_showhtml/q_list_show.html', context=context)


class QctObjectDetail(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_obj = QuestionCalssTheme.objects.filter(pk=t_id, is_show=1)
        if not len(qct_obj):
            return render(request, 'base_html/404.html')
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_obj": qct_obj[0]
        }
        return render(request, 'new_showhtml/q_detail_show.html', context=context)


