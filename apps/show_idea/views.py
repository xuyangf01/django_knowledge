from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from django_redis import get_redis_connection
from django.core.paginator import Paginator
from show_idea.models import BigClassTheme, SubClassTheme, QuestionCalssTheme, QuestionComment
from datetime import datetime


# 密码修改
@method_decorator(login_required, name="dispatch")
class MyChangePwd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'new_showhtml/change_pwd.html')

    def post(self, request, *args, **kwargs):
        old_password = request.POST.get('old_password')
        if not request.user.check_password(old_password):
            return JsonResponse({'code': "原始密码错误"})
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 and password2:
            if len(password1) < 8:
                return JsonResponse({'code': "新密码长度少于8位！"})
            if password1 != password2:
                return JsonResponse({'code': "两次密码不匹配"})
        user = request.user
        user.set_password(password2)
        user.save()
        return JsonResponse({'code': "success"})


# 发表评论
@method_decorator(login_required, name="dispatch")
class CommentFunction(View):
    def get(self, request):
        comment_qset = QuestionComment.objects.filter(is_show=2)
        context = {
            "comment_qset": comment_qset
        }
        return render(request, 'new_showhtml/check_comment.html', context=context)

    def post(self, request, **kwargs):
        if request.method == "POST":
            user = request.user
            data = request.POST
            question_id = data.get("question_id")
            comment_content = data.get("comment_content")
            if all((question_id, comment_content)):
                que_comment = QuestionComment()
                try:
                    que_obj = QuestionCalssTheme.objects.get(t_id=int(question_id))
                except:
                    return render(request, 'base_html/404.html')
                que_comment.user_obj = user
                que_comment.question_obj = que_obj
                que_comment.comment_content = comment_content
                que_comment.is_show = 2   # 默认提交的评论都不显示， 管理员有权限审核并显示
                que_comment.save()
                return JsonResponse({"code": "comment_success"})
            else:
                return JsonResponse({'code': "comment_fail"})


# 搜索框自动补全
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


# 404页面
@login_required
def page_not_found(request, **kwargs):
    return render(request, 'base_html/404.html')


# 注销
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
        stc_qryset = sorted(stc_qryset, key=lambda x: len(x.sct_name))
        # 添加分页器
        stc_qryset_paginator = Paginator(stc_qryset, 10)
        page = request.GET.get("p", 1)
        # stc_qryset = stc_qryset_paginator.page(page)     # 当页数超出范围或者为其他字符串形式，则抛出异常
        stc_qryset = stc_qryset_paginator.get_page(page)  # django2.0版本新增功能 超出访问显示最后一页，字符串则显示第一页
        strat_number = (stc_qryset.number - 1) * 10  # 渲染前端展示序号

        # 不足10个对象数，前端填充空数据
        count = len(stc_qryset)
        add_empty_data = [strat_number + i for i in range(count + 1, count + 1 + (10 - count))] if count < 10 else None
        context = {
            "btc_obj_qset": btc_obj_qset,
            "stc_qryset": stc_qryset,
            "add_empty_data": add_empty_data,
            "strat_number": strat_number
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
        # 添加分页器
        qct_qryset_paginator = Paginator(qct_qyset, 10)
        page = request.GET.get("p", 1)
        # qct_qyset = qct_qryset_paginator.page(page)      # 当页数超出范围或者为其他字符串形式，则抛出异常
        qct_qyset = qct_qryset_paginator.get_page(page)  # django2.0版本新增功能 超出访问显示最后一页，字符串则显示第一页
        strat_number = (qct_qyset.number - 1) * 10  # 渲染前端展示序号

        # 不足10个对象数，前端填充空数据
        count = len(qct_qyset)
        add_empty_data = [strat_number + i for i in range(count + 1, count + 1 + (10 - count))] if count < 10 else None
        context = {
            "master_obj": qct_qyset[0].bct_id,
            "child_obj": qct_qyset[0].sct_id,
            "btc_obj_qset": btc_obj_qset,
            "qct_qyset": qct_qyset,
            "add_empty_data": add_empty_data,
            "strat_number": strat_number
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
        redis_conn = get_redis_connection(alias="my_redis_online_4")  # 线上redis数据库
        # redis_conn = get_redis_connection(alias="my_redis_test_3")                           # 测试redis数据库
        redis_conn.hset(qct_id, username, visit_time)

        # 获取文章id的哈希表所有键值对，以近期时间排序返回前端页面展示
        all_visits = redis_conn.hgetall(qct_id)
        # 进行时间排序，并取出前10条数据进行展示
        recent_visits = sorted(all_visits.items(), key=lambda tup: tup[1], reverse=True)[0:10]
        recent_visits = [(str(k, encoding='utf-8'), str(v, encoding='utf-8')) for k, v in recent_visits]

        # 获取文章评论
        comment_qset = QuestionComment.objects.filter(is_show=1, question_obj=qct_obj_qury[0]).order_by('is_priority').order_by('-is_popular').order_by('-create_timestamp')

        context = {
            "btc_obj_qset": btc_obj_qset,
            "qct_obj": qct_obj_qury[0],
            "recent_visits": recent_visits,
            "comment_qset": comment_qset,
        }
        resp = render(request, 'new_showhtml/q_detail_show.html', context=context)
        # 设置cookie，第一次颁发一个reading状态
        if request.COOKIES.get("question_{}".format(t_id)) != "reading":
            qct_obj_qury[0].visit_count += 1
            qct_obj_qury[0].save()
            # 设置失效时间600秒，10分钟计算一次访问量
            resp.set_cookie("question_{}".format(t_id), 'reading', max_age=600)
        return resp
