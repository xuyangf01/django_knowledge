from django.shortcuts import render
from django.views import View
from apps.show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme


def page_not_found(request, **kwargs):
    return render(request, 'base_html/404.html')


class Index(View):
    def get(self, request):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=True)
        stc_qryset = SubClassTheme.objects.filter(is_show=True, bct_id=btc_obj_qset[0].pk)
        context = {
            "btc_obj_qset": btc_obj_qset,
            "stc_qryset": stc_qryset,
        }
        return render(request, 'new_showhtml/index.html', context=context)


class SctListShow(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=True)
        stc_qryset = SubClassTheme.objects.filter(is_show=True, bct_id=t_id)
        context = {
            "btc_obj_qset": btc_obj_qset,
            "stc_qryset": stc_qryset,
        }
        return render(request, 'new_showhtml/s_list_show.html', context=context)


class QctListShow(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=True)
        qct_qyset = QuestionCalssTheme.objects.filter(is_show=True, sct_id_id=t_id)
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset
        }
        return render(request, 'new_showhtml/q_list_show.html', context=context)


class QctObjectDetail(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=True)
        qct_obj = QuestionCalssTheme.objects.get(pk=t_id, is_show=True)
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_obj": qct_obj
        }
        return render(request, 'new_showhtml/q_detail_show.html', context=context)
