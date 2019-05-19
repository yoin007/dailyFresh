# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from hashlib import sha1


def temp(request):
    return render(request, 'df_user/temp.html')


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收用户收入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    # 创建用户对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，跳转登录页面
    return redirect('/user/login')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname, 'title': '用户登录', 'error_name': 0, 'error_pwd': 0}
    return render(request, 'df_user/login.html', context)


def login_check(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def info(request):
    uname = request.session.get('user_name')
    print(uname)
    if uname:
        email = UserInfo.objects.get(id=request.session.get('user_id')).uemail
        return render(request, 'df_user/user_center_info.html', {'uname': uname, 'email': email})
    else:
        return redirect('/user/login')


def order(request):
    return render(request, 'df_user/user_center_order.html')


def site(request):
    return render(request, 'df_user/user_center_site.html')





