# coding=utf-8
from django.contrib import auth
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from account.decorator import login_required
from account.models import Account


def login(request):
    # for user in User.objects.all():
    #   user.set_password(user.password)
    # user.date_joined = time.localtime(time.time())
    #   user.save()
    #   for account in Account.objects.all():
    #      account.save()
    if request.method != 'POST':
        return render(request, 'login.html', locals())

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 第一次使用学号登录，先在表中创建该user
    #    if username == password and password.isdigit() and len(password) == 12 and not User.objects.filter(
    #           username=username).exists():
    #      user = User(username=username)
    #     user.set_password(password)
    #    user.save()

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
    user = request.user
    account = Account.objects.get(user=request.user)
    if account.completed is True:
        return HttpResponseRedirect('/index/')
    if request.method != 'POST':
        return render(request, 'home.html', locals())
    password = request.POST.get('password', '')
    re_password = request.POST.get('re_password', '')
    telephone = request.POST.get('re_telephone', '')
    email = request.POST.get('re_email', '')
    grade = request.POST.get('re_grade', '')
    major = request.POST.get('re_major', '')
    if password != re_password:
        msg = '两次输入密码不一致'
        return render(request, 'home.html', locals())
    if len(password) < 6 or len(password) > 16:
        msg = '密码长度不符'
    if telephone == '' or email == '' or grade == '' or major == '':
        msg = '检查信息是否填写完整'
        return render(request, 'home.html', locals())
    msg = '信息修改成功！'
    account = Account.objects.get(user=user)
    #    account.question = question
    #    account.answer = answer
    user.set_password(password)
    user.save()
    account.telephone = telephone
    account.email = email
    account.grade = grade
    account.major = major
    account.completed = True
    account.save()
    django_login(request, user)
    return HttpResponseRedirect('/index/')


def forget(request):
    # if request.is_anonymous():
    #   return render(request, 'forget.html', locals())

    if request.method != 'POST':
        return render(request, 'forget.html', locals())
    ID = request.POST.get('ID', '')
    telephone = request.POST.get('telephone', '')
    user = User.objects.get(username=ID)
    account = Account.objects.get(user=user)
    if account.telephone != telephone:
        msg = u'用户不存在或用户名与电话不匹配'
        flag = 0
        return render(request, 'forget.html', locals())
    user = account.user
    account.completed = False
    user.set_password(user.username)
    user.save()
    msg = user.first_name + u'的账户已被重置，请使用初始密码重新登录'
    flag = 1
    return render(request, 'forget.html', locals())


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
    password = request.POST.get('password', '')
    re_password = request.POST.get('re_password', '')
    telephone = request.POST.get('re_telephone', '')
    email = request.POST.get('re_email', '')
    grade = request.POST.get('re_grade', '')
    major = request.POST.get('re_major', '')
    if password != re_password:
        msg = '两次输入密码不一致'
        return render(request, 'personal_info.html', locals())
    if len(password) < 6 or len(password) > 16:
        msg = '密码长度不符'
        return render(request, 'personal_info.html', locals())
    if telephone == '' or email == '' or grade == '' or major == '':
        msg = '检查信息是否填写完整'
        return render(request, 'personal_info.html', locals())
    msg = '信息修改成功！'
    account = Account.objects.get(user=user)
    #    account.question = question
    #    account.answer = answer
    user.set_password(password)
    user.save()
    account.telephone = telephone
    account.email = email
    account.grade = grade
    account.major = major
    account.completed = True
    account.save()
    django_login(request, user)
    return render(request, 'personal_info.html', locals())


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')
