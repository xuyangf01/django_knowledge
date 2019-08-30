from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme


@login_required
def ajax_complete_content(request, **kwargs):
    # ajax获取输入框的值
    search_q = request.GET.get("q")
    if search_q is not None:
        qct_name_list = []
        qct_qyset = QuestionCalssTheme.objects.values_list('qct_name').filter(is_show=1, qct_name__contains=search_q)
        for qct_name_tuple in qct_qyset:
            qct_name_list.append(qct_name_tuple[0])
        if qct_name_list:
            return JsonResponse({"array": qct_name_list})
    return JsonResponse({"array": ["无类似问题名字，请点击按钮直接搜内容"]})


@login_required
def page_not_found(request, **kwargs):
    return render(request, 'base_html/404.html')


@login_required
def account_logout(request, **kwargs):
    logout(request)  # 注销
    return redirect(reverse("login"))


# 登录界面
class LoginKnowledge(View):
    def get(self, request):
        # 如果用户已登录，重定向首页
        if request.user.is_authenticated:
            return redirect(reverse("site_index"))
        return render(request, 'new_showhtml/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:  # 如果用户对象存在
            login(request, user)  # 用户登陆
            return redirect(reverse("show_idea:index"))
        else:
            context = {
                "error": "用户名或者密码错误！！！"
            }
            return render(request, 'new_showhtml/login.html', context=context)


# 首页视图
@method_decorator(login_required, name="dispatch")
class Index(View):
    def get(self, request):
        # 获取大类主题
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_qyset = QuestionCalssTheme.objects.filter(is_show=1, is_popular=2).order_by('is_priority')[:5]
        qct_visit_qyset = QuestionCalssTheme.objects.filter(is_show=1, is_popular=1).order_by('-visit_count')[:5]

        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset,
            "qct_visit_qyset": qct_visit_qyset,
        }
        return render(request, 'new_showhtml/index.html', context=context)


# 展示二级标题
@method_decorator(login_required, name="dispatch")
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


# 展示问题列表
@method_decorator(login_required, name="dispatch")
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


# 展示问题详情
@method_decorator(login_required, name="dispatch")
class QctObjectDetail(View):
    def get(self, request, t_id):
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_obj_qury = QuestionCalssTheme.objects.filter(pk=t_id, is_show=1)
        # 没有获取到对象
        if not len(qct_obj_qury):
            return render(request, 'base_html/404.html')
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_obj": qct_obj_qury[0]
        }
        resp = render(request, 'new_showhtml/q_detail_show.html', context=context)
        # 设置cookie，第一次颁发一个reading状态
        if request.COOKIES.get("question_{}".format(t_id)) != "reading":
            qct_obj_qury[0].visit_count += 1
            qct_obj_qury[0].save()
            # 设置失效时间60秒
            resp.set_cookie("question_{}".format(t_id), 'reading', max_age=600)
        return resp
