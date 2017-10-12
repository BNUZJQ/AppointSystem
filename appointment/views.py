# coding=utf-8
from django.shortcuts import render
import datetime
from django.contrib.auth import login as django_login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appointment.models import Appointment
from django.contrib.auth.models import User
from account.models import Account
from classroom.models import Classroom


# Create your views here.

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


def main_appoint(request):
    if request.method == 'POST':
        # return render(request, 'main_appoint.html', locals())
        classroom_choice = request.POST.get('classroom', '')
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)
        appoint_array = Appointment.objects.filter(classroom=classroom_choice,
                                                   date__gte=today,
                                                   date__lte=endday)
        my_appoint = appoint_array.filter(custom=request.user)
        date_array = []
        for appoint in appoint_array:
            date_array.append(appoint.data)
        if Classroom.objects.filter(name=classroom_choice).exists():  # and time.strftime('%Y-%m-%d',time.localtime(time.time()))
            appoint_array = Appointment.Objects.filter()
            return render(request, 'main_appoint.html', locals())
        else:
            error_code = u'无记录'
            return render(request, 'main_appoint.html', locals())

    duration_choice = request.POST.get('duration', '')
    data_choice = request.POST.get('date', '')
