# coding=utf-8
from django.contrib.auth import login as django_login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Account.models import Account
from django.contrib.auth.models import User
import ipdb


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html', locals())

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 第一次使用学号登录，先在表中创建该user
    if username == password and password.isdigit() and len(password) == 12:
        user = User(username=username, password=password)
        user.save()

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user = authenticate(username=user.username, password=password)
        if user is None:
            login_errors = u'密码错误'
            return render(request, 'login.html', locals())
    else:
        login_errors = u'该账号或邮箱不存在'
        return render(request, 'login.html', locals())

    django_login(request, user)
    return HttpResponseRedirect('/home/')


def home(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('login/')
    account = Account.objects.get(user=user)
    # 账户信息尚未补全
    if not account.completed:
        return HttpResponseRedirect('/complete_info/')
    return render(request, 'home.html', locals())


def complete_info(request):
    account = Account.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'complete_info.html', locals())
    question = request.POST.get('question', '')
    answer = request.POST.get('answer', '')
    account.question = question
    account.answer = answer
    account.completed = True
    account.save()
    return HttpResponseRedirect('/home/')
