from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from django_redis import get_redis_connection
from show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme
from datetime import datetime


@method_decorator(login_required, name="dispatch")
class MyPasswordChangeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'new_showhtml/change_pwd.html')

    def post(self, request, *args, **kwargs):
        my_error_messages = []
        old_password = request.POST.get('old_password')
        if not request.user.check_password(old_password):
            my_error_messages.append("原始密码错误")
            context = {
                "my_error_messages": my_error_messages,
            }
            return render(request, 'new_showhtml/change_pwd.html', context=context)
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 and password2:
            if len(password1) < 8:
                my_error_messages.append("新密码长度少于8位！")
                context = {
                    "my_error_messages": my_error_messages,
                }
                return render(request, 'new_showhtml/change_pwd.html', context=context)
            if password1 != password2:
                my_error_messages.append("两次密码不匹配")
                context = {
                    "my_error_messages": my_error_messages,
                }
                return render(request, 'new_showhtml/change_pwd.html', context=context)
        user = request.user
        user.set_password(password2)
        user.save()
        return redirect(reverse("logout"))


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
        stc_qryset = sorted(stc_qryset, key=lambda x: len(x.sct_name))
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
        qct_qyset = sorted(qct_qyset, key=lambda x: len(x.qct_name))
        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset
        }
        return render(request, 'new_showhtml/q_list_show.html', context=context)


# 展示问题详情
@method_decorator(login_required, name="dispatch")
class QctObjectDetail(View):
    def get(self, request, t_id):
        # 获取一级主题
        btc_obj_qset = BigClassTheme.objects.filter(is_show=1).order_by('is_priority')
        if not len(btc_obj_qset):
            return render(request, 'base_html/首页无数据.html')
        qct_obj_qury = QuestionCalssTheme.objects.filter(pk=t_id, is_show=1)
        # 没有获取到对象
        if not len(qct_obj_qury):
            return render(request, 'base_html/404.html')

        # 创建redis连接，将该文章的最近访问人添加进redis列表
        qct_id = "qct_{}".format(t_id)
        username = request.user.username
        visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        redis_conn = get_redis_connection(alias="my_redis_online_4")                       # 线上redis数据库
        # redis_conn = get_redis_connection(alias="my_redis_test_3")                           # 测试redis数据库
        redis_conn.hset(qct_id, username, visit_time)

        # 获取文章id的哈希表所有键值对，以近期时间排序返回前端页面展示
        all_visits = redis_conn.hgetall(qct_id)
        visit_count = redis_conn.hget(qct_id, "visit_count")
        if visit_count is not None:
            # 删除访问量，避免循环渲染到最近访问记录里面
            all_visits.pop(b'visit_count')

        # 进行时间排序，并取出前10条数据进行展示
        recent_visits = sorted(all_visits.items(), key=lambda tup: tup[1], reverse=True)[0:10]
        recent_visits = [(str(k, encoding='utf-8'), str(v, encoding='utf-8')) for k, v in recent_visits]

        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_obj": qct_obj_qury[0],
            "recent_visits": recent_visits,
            "visit_count": int(visit_count) if visit_count else 0,
        }
        resp = render(request, 'new_showhtml/q_detail_show.html', context=context)
        # 设置cookie，第一次颁发一个reading状态
        if request.COOKIES.get("question_{}".format(t_id)) != "reading":
            redis_conn.hincrby(qct_id, "visit_count", amount=1)
            # 设置失效时间600秒，10分钟计算一次访问量
            resp.set_cookie("question_{}".format(t_id), 'reading', max_age=600)
        return resp
