# coding=utf-8

from account.decorator import login_required
import datetime
from django.contrib.auth import login as django_login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appointment.models import Appointment
from django.contrib.auth.models import User
from account.models import Account
from classroom.models import Classroom


# Create your views here.
# 应该用ajax
@login_required
def choose_classroom(request):
    user = request.user
    if request.method == 'POST':
        classroom_choice = request.POST.get('classroom', '')
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)
        classroom = Classroom.objects.get(name=classroom_choice)
        appointments = Appointment.objects.filter(classroom=classroom,
                                                   date__gte=today,
                                                   date__lte=endday)
        my_appointments = appointments.filter(custom__user=User.objects.get(id= user.id))
        return render(request, 'main_appointment.html', locals())


@login_required
def main_appoint(request):
    return render(request, 'main_appointment.html', locals())


@login_required
def post_appointment(request):
    user = request.user
    if request.method == 'POST':
        duration_choice = request.POST.get('duration', '')
        data_choice = request.POST.get('date', '')
        reason_reason = request.POST.get('reason', '')
        classroom_choice = request.POST.get('classroom', '')
        appointment = Appointment()
        appointment.duration = duration_choice
        appointment.classroom = Classroom.objects.get(name=classroom_choice)
        appointment.custom = Account.objects.get(user=request.user)
        appointment.date = data_choice
        appointment.reason = reason_reason
        appointment.save()
        return render(request, 'main_appointment.html', locals())

    # def delete_myappointment(request):
    # if request.method == 'POST':
