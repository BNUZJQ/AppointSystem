# coding=utf-8

from django.shortcuts import render
from django.views.decorators.http import require_POST

from account.decorator import login_required
from account.models import Account
from appointment.models import Appointment
from classroom.models import Classroom


@login_required
def index(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'index.html', locals())


@login_required
def myappointment(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'myappointment.html', locals())

@require_POST
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
