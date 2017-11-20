# coding=utf-8
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from account.decorator import login_required
from account.models import Account


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


@login_required
def home(request):
    account = Account.objects.get(user=request.user)
    if account.completed is False:
        return HttpResponseRedirect('/person_info/')
    return render(request, 'home.html', locals())


@login_required
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


@login_required
def change_info(request):
    user = request.user
    if request.method != 'POST':
        return render(request, 'personal_info.html', locals())
    # question = request.POST.get('question', '')
    #    answer = request.POST.get('answer', '')
    #    password = request.POST.get('password', '')
    #    user.set_password(password)
    #    user.save()
    telephone = request.POST.get('re_telephone', '')
    email = request.POST.get('re_mail', '')
    grade = request.POST.get('re_grade', '')
    major = request.POST.get('re_major', '')

    account = Account.objects.get(user=user)
    account.telephone = telephone
    account.email = email
    account.grade = grade
    account.major = major
    account.completed = True
    account.save()
    return HttpResponseRedirect('/index/')


@login_required
def personal_info(request):
    account = Account.objects.get(user=request.user)
    user = request.user
    if request.method != 'POST':
        return render(request, 'personal_info.html', locals())
        #    question = request.POST.get('question', '')
        #    answer = request.POST.get('answer', '')
        #    password = request.POST.get('password', '')
        #    user.set_password(password)
        #    user.save()
    telephone = request.POST.get('re_telephone', '')
    email = request.POST.get('re_email', '')
    grade = request.POST.get('re_grade', '')
    major = request.POST.get('re_major', '')

    account = Account.objects.get(user=user)
    #    account.question = question
    #    account.answer = answer
    account.telephone = telephone
    account.email = email
    account.grade = grade
    account.major = major
    account.completed = True
    account.save()
    return render(request, 'personal_info.html', locals())
