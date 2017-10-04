# coding=utf-8
from django.contrib.auth import login as django_login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Account.models import Account
from django.contrib.auth.models import User


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html', locals())

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 第一次使用学号登录，先在表中创建该user
    if username == password and password.isdigit() and len(password) == 12 and not User.objects.filter(
            username=username).exists():
        user = User(username=username)
        user.set_password(password)
        user.save()

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if not user.check_password(raw_password=password):  # 不能直接user.password == password
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
        return HttpResponseRedirect('/')
    # 仅有user 没有account
    if not Account.objects.filter(user=user).exists():
        return HttpResponseRedirect('/complete_info/')
    account = Account.objects.get(user=user)
    return render(request, 'home.html', locals())


def complete_info(request):
    user = request.user
    if request.method != 'POST':
        return render(request, 'complete_info.html', locals())
    question = request.POST.get('question', '')
    answer = request.POST.get('answer', '')
    email = request.POST.get('email', '')
    user.email = email
    user.save()
    account = Account(user=user)
    account.question = question
    account.answer = answer
    account.completed = True
    account.save()
    return HttpResponseRedirect('/home/')


def forget(request):
    if request.method != 'POST':
        return render(request, 'forget.html', locals())
    email = request.POST.get('email', '')
    if not User.objects.filter(email=email).exists():
        msg = u'该用户不存在'
        return render(request, 'forget.html', locals())
    user = User.objects.get(email=email)
    user.set_password(user.username)
    user.save()
    return HttpResponseRedirect('/')


def change_info(request):
    user = request.user
    if request.method != 'POST':
        return render(request, 'change_info.html', locals())
    question = request.POST.get('question', '')
    answer = request.POST.get('answer', '')
    password = request.POST.get('password', '')
    user.set_password(password)
    user.save()
    account = Account.objects.get(user=user)
    account.question = question
    account.answer = answer
    account.completed = True
    account.save()
    return HttpResponseRedirect('/home/')
